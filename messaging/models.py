from django.db import models
from users.models import UserInfo

class Message(models.Model):
    sender = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username} ({self.timestamp})"
