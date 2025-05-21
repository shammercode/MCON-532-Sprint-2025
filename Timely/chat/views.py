import json
from datetime import datetime, timedelta

import numpy as np
import pytz
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.conf import settings

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

from chat.models import ChatMessage, CalendarEvent

from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials



# Initialize OpenAI client
# This client is used to interact with the OpenAI API for generating chat responses.
client = OpenAI(api_key=settings.OPEN_AI_API_KEY, organization=settings.OPENAI_ORG_ID)

def index(request):
    """
    Render the index page.
    """
    return render(request, 'index.html')


def response(request):
    """
    Handle POST requests to generate a response using OpenAI's API.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the AI-generated message or an error message.
    """
    if request.method == 'POST':
        # Retrieve the user's message from the POST request
        message = request.POST.get("message", "")
        if not message:
            return JsonResponse({'response': 'No message provided.'}, status=400)

        # Generate a response using OpenAI's chat completion API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        # Extract the AI's response
        answer = completion.choices[0].message.content

        # Save the message and response to the database
        ChatMessage.objects.create(message=message, response=answer)

        return JsonResponse({'response': answer}, status=200)

    # Return an error response for non-POST requests
    return JsonResponse({'response': 'Invalid Request'}, status=400)


# Define Google OAuth scopes
# These scopes determine the level of access the application has to the user's Google account.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]

def google_login(request):
    """
    Initiate the Google OAuth login process.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to Google's OAuth consent screen.
    """
    # Create a Flow object for managing the OAuth process
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline',
        include_granted_scopes=False
    )

    return redirect(auth_url)


def oauth2callback(request):
    """
    Handle the OAuth2 callback after the user authorizes the application.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the home page after successful login.
    """
    # Exchange the authorization code for credentials
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Retrieve user information from Google
    user_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_service.userinfo().get().execute()
    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')

    if not email:
        return HttpResponse("Unable to retrieve user email.", status=400)

    # Create or retrieve the user in the Django database
    user, _ = User.objects.get_or_create(
        username=email,
        first_name=first_name,
        last_name=last_name,
        defaults={'email': email}
    )
    # Log the user in
    login(request, user)

    # Save credentials in the session (for prototype purposes; use a database for production)
    request.session['google_token'] = credentials_to_dict(credentials)
    return redirect('/')


def list_events(request):
    """
    List the user's Google Calendar events for the next two weeks.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the events page with the list of events.
    """
    # Retrieve the stored Google token from the session
    token_info = request.session.get('google_token')
    if not token_info:
        return redirect('/calendar/google_login')

    # Recreate credentials from the token info
    creds = Credentials(**token_info)
    if creds.expired:
        if creds.refresh_token:
            # Refresh the credentials if they have expired
            creds.refresh(Request())
            request.session['google_token'] = credentials_to_dict(creds)
        else:
            return redirect('/calendar/google_login')

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Define the time window for events: now to two weeks from now
    now = datetime.now(pytz.utc)  # This is a datetime object
    two_weeks_from_now = now + timedelta(weeks=2)
    # date two weeks from now in ISO format
    two_weeks = (now + timedelta(weeks=2)).isoformat()
    # Fetch events from the user's primary calendar
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat(),
        timeMax=two_weeks_from_now.isoformat(),
        maxResults=50,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    # Extract the list of events
    events = events_result.get('items', [])

    #Clear existing events in this time range for this user
    CalendarEvent.objects.filter(
        user=request.user,
        event_start__gte=now,
        event_start__lte=two_weeks_from_now
    ).delete()

    event_instances = []
    for event in events:
        start_str = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
        summary = event.get("summary")
        if start_str:
            try:
                event_start = datetime.fromisoformat(start_str)
                if event_start.tzinfo is None:
                    event_start = pytz.utc.localize(event_start)
                else:
                    event_start = event_start.astimezone(pytz.utc)
            except ValueError as ex:
                continue   # skip if invalid format
            embedding = embed_text(json.dumps(event))
            event_instances.append(CalendarEvent(
                user=request.user,
                event_data=event,
                event_start=event_start,
                embedding=embedding,
                summary=summary
            ))
    if event_instances and len(event_instances) > 0:
        CalendarEvent.objects.bulk_create(event_instances)

    return render(request, 'events.html', {'events': events})

def logout_view(request):
    """
    Log the user out and redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the home page.
    """
    logout(request)
    return redirect('/')


def credentials_to_dict(credentials):
    """
    Convert Google OAuth credentials to a dictionary for storage.

    Args:
        credentials: The Google OAuth credentials object.

    Returns:
        dict: A dictionary representation of the credentials.
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': list(credentials.scopes),
    }
# Define Google OAuth scopes
# These scopes determine the level of access the application has to the user's Google account.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]

def google_login(request):
    """
    Initiate the Google OAuth login process.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to Google's OAuth consent screen.
    """
    # Create a Flow object for managing the OAuth process
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline',
        include_granted_scopes=False
    )

    return redirect(auth_url)


def oauth2callback(request):
    """
    Handle the OAuth2 callback after the user authorizes the application.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the home page after successful login.
    """
    # Exchange the authorization code for credentials
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Retrieve user information from Google
    user_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_service.userinfo().get().execute()
    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')

    if not email:
        return HttpResponse("Unable to retrieve user email.", status=400)

    # Create or retrieve the user in the Django database
    user, _ = User.objects.get_or_create(
        username=email,
        first_name=first_name,
        last_name=last_name,
        defaults={'email': email}
    )
    # Log the user in
    login(request, user)

    # Save credentials in the session (for prototype purposes; use a database for production)
    request.session['google_token'] = credentials_to_dict(credentials)
    return redirect('list/')



def logout_view(request):
    """
    Log the user out and redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the home page.
    """
    logout(request)
    return redirect('/')


def credentials_to_dict(credentials):
    """
    Convert Google OAuth credentials to a dictionary for storage.

    Args:
        credentials: The Google OAuth credentials object.

    Returns:
        dict: A dictionary representation of the credentials.
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': list(credentials.scopes),
    }

def get_combined_event_data_for_assistant(user):
    # Optional: limit to future 2 weeks
    events = CalendarEvent.objects.filter(
        user=user
    ).order_by('event_start')

    # Extract just the raw JSON content
    combined_events_data = [event.event_data for event in events]
    return json.dumps(combined_events_data, indent=2)

def response(request):
    """
    Handle POST requests to generate a response using OpenAI's API.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the AI-generated message or an error message.
    """
    if request.method == 'POST':
        # Retrieve the user's message from the POST request
        message = request.POST.get("message", "")
        if not message:
            return JsonResponse({'response': 'No message provided.'}, status=400)

        query_embedding = embed_text(message)
        user = request.user
        # Retrieve past events with embeddings
        relevant_context = get_relevant_events(user, query_embedding)
        upcoming_events = get_combined_event_data_for_assistant(
            request.user
        )
        #Retrieve last 5 ChatMessages for history
        history = ChatMessage.objects.filter(user=user).order_by('-created_at')[:5][::-1]
        history_prompt = "\n".join([f"User: {m.message}\nAI: {m.response}" for m in history])

        prompt = f"{history_prompt}\n\nContext:\n{relevant_context}\n\nUser: {message}\nAI:"

        # Generate a response using OpenAI's chat completion API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": "You are a helpful assistant. use my schedule to answer my questions."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"Here is my schedule: {relevant_context}"},

            ],
            top_p=0.7,
        )
        # Extract the AI's response
        answer = completion.choices[0].message.content

        # Save the message and response to the database
        ChatMessage.objects.create(message=message, response=answer, user=request.user)

        return JsonResponse({'response': answer}, status=200)

    # Return an error response for non-POST requests
    return JsonResponse({'response': 'Invalid Request'}, status=400)

def compute_cosine_similarities(query_vector, matrix):
    if not matrix:
        return []
    query_vec = np.array(query_vector).reshape(1, -1)
    matrix_np = np.array(matrix)
    similarities = cosine_similarity(query_vec, matrix_np)[0]
    return similarities

def embed_text(text):
    result = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return result.data[0].embedding

def get_relevant_events(user, query_embedding):
    # Step 2: Retrieve past events with embeddings
    # This function retrieves past events for the user and computes their cosine similarity with the query embedding.
    relevant_context = "No events found."
    events = CalendarEvent.objects.filter(user=user, embedding__isnull=False)
    if events:
        embeddings = [event.embedding for event in events]
        similarities = compute_cosine_similarities(query_embedding, embeddings)
        top_indices = np.argsort(similarities)[-3:][::-1]
        events_list = list(events)
        top_events = [events_list[i] for i in top_indices]
        relevant_context = "\n".join([json.dumps(event.event_data) for event in top_events])
        return relevant_context
    return relevant_context


