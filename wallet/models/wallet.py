import random
import string

from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Wallet(models.Model):
    TYPE_CHOICES = (
        ("Visa", "Visa"),
        ("Mastercard", "Mastercard"),
    )
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"

    CURRENCY_CHOICES = (
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("RUB", "RUB"),
    )
    name = models.CharField(max_length=8, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


def generate_wallet_name():
    characters = string.ascii_uppercase + string.digits
    wallet_name = "".join(random.choices(characters, k=8))
    return wallet_name
