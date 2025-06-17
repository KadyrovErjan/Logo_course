from django.db import models
from logo_app.models import UserProfile

class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    date = models.DateField(auto_now_add=True)



class Message(models.Model):
    chats = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image_chat = models.ImageField(upload_to='chats_image/', null=True, blank=True)
    video_chat = models.FileField(upload_to='videos/', null=True, blank=True)
    crated_data = models.DateTimeField(auto_now_add=True)
