from django.db import models

from accounts.models import CustomUser

class ChatMessage(models.Model):
    sender = models.IntegerField(default=None)
    message = models.TextField(blank=False, null=False)
    thread_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    timestamp =  models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Message of <{self.thread_name} sent at {self.timestamp}>'

class ChatNotification(models.Model):
    chat = models.ForeignKey(to=ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Notification for < user: {self.user.username} - seen : {self.is_seen}>'