from django.db import models
from base.utils import h_encode, h_decode

class ChatMessage(models.Model):
    class Meta:
        ordering = ['timestamp']

    sender = models.IntegerField(default=None)
    receiver = models.IntegerField(default=None, null=True, blank=True)
    message = models.TextField(blank=False, null=False)
    thread_name = models.CharField(
        max_length=50, default=None, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_hashid(self):
        return h_encode(self.id)

    def __str__(self) -> str:
        return f'Message of <{self.thread_name} sent at {self.timestamp}>'
