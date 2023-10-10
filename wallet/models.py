from django.db import models
from users.models import UserInfo

class UserWalletDetails(models.Model):
    balance = models.CharField(max_length=500, null=True, blank=True, default=0)
    balance1 = models.CharField(max_length=500, null=True, blank=True, default=0)
    transactions = models.CharField(max_length=500, null=True, blank=True, default=0)
    total_sent = models.CharField(max_length=500, null=True, blank=True, default=0)
    total_sent1 = models.CharField(max_length=500, null=True, blank=True, default=0)
    total_received = models.CharField(max_length=500, null=True, blank=True, default=0)
    total_received1 = models.CharField(max_length=500, null=True, blank=True, default=0)
    private_key = models.CharField(max_length=500)
    public_key = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    live_bitcoin_price = models.CharField(max_length=500, null=True, blank=True, default=0)
    balance_usd = models.CharField(max_length=500, null=True, blank=True, default=0)
    total_sent_usd = models.CharField(max_length=500, null=True, blank=True, default=0)
    total_received_usd = models.CharField(max_length=500, null=True, blank=True, default=0)
    
class FormSubmission(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    message = models.TextField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.name