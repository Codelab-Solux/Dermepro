from django.db import models
from accounts.models import CustomUser
from base.utils import h_encode, h_decode

class ChatThread(models.Model):
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='initiator')
    responder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='responder')
    timestamp = models.DateTimeField(auto_now_add=True)
    # thread_name = models.CharField(
    #     max_length=50, default=None, blank=True, null=True)
        
    def get_thread_name(self):
        return f'{self.initiator}_{self.responder}>'

    def get_hashid(self):
        return h_encode(self.id)

    def __str__(self) -> str:
        return f'From <{self.initiator} to {self.responder}>'

class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_hashid(self):
        return h_encode(self.id)

    def __str__(self) -> str:
        return f'Message from <{self.sender} to {self.receiver}>'
