from django.urls import path
from chat.views import index, response

urlpatterns = [
    path('',index, name="index"),
    path('response', response, name="response")
]