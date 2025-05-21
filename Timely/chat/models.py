from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField, TextField  # Import for JSONField

# Create your models here.
class ChatMessage(models.Model):
    class Meta:
        db_table = 'chat_message'
    message = models.TextField()
    response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CalendarEvent(models.Model):
    class Meta:
        db_table = 'calendar_events'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_data = JSONField()  # Stores the full Google Calendar event JSON
    event_start = models.DateTimeField()  # Timestamp for the event's start time
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(default="")
    embedding = ArrayField(models.FloatField(), blank=True, null=True)
    def __str__(self):
        return f"Event for {self.user.username} at {self.event_start}"