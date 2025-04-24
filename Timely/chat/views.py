from multiprocessing.connection import answer_challenge

from django.shortcuts import render
from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from chat.models import ChatMessage

# Create your views here.

client = OpenAI(api_key=settings.OPEN_AI_API_KEY, organization=settings.OPENAI_ORG_ID)
def index(request):
    return render(request, 'index.html')

def response(request):
    if request.method == 'POST':
        message = request.POST.get("message", "")
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        answer = completion.choices[0].message.content
        chat_message = ChatMessage(message=message, response=answer)
        chat_message.save()
        return JsonResponse({'response': answer}, status=200)

    return JsonResponse({'response', 'Invalid Request'}, status=400)
