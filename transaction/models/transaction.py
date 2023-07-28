from django.utils import timezone
from django.db import models

from user.models import User
from wallet.models import Wallet


class Transaction(models.Model):
    STATUS_CHOISES = (("PAID", "PAID"), ("NOT_APPROVED", "NOT_APPROVED"))
    sender = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="receiver_transactions"
    )
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOISES)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
