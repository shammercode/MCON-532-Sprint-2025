from django.db import models

# Create your models here.
class ChatMessage(models.Model):
    class Meta:
        db_table = 'chat_messages'
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)