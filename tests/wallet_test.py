import pytest
from django.urls import reverse
from rest_framework import status

from wallet.models import Wallet
from wallet.models.wallet import generate_wallet_name
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_generate_wallet_name():
    wallet_name = generate_wallet_name()
    assert isinstance(wallet_name, str)
    assert len(wallet_name) == 8


@pytest.mark.django_db
def test_generate_wallet_count():
    user_wallets_count = Wallet.objects.filter().count()
    assert isinstance(user_wallets_count, int)
    assert user_wallets_count <= 5


@pytest.mark.django_db
def test_wallet_str_method():
    wallet = Wallet(name="test_wallet", type="Visa", currency="USD")
    assert str(wallet) == "test_wallet"


@pytest.mark.django_db
def test_create_wallet():
    url = reverse("wallet-list-create")
    data = {"type": "Visa", "currency": "USD"}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Wallet.objects.count() == 1
    assert Wallet.objects.get().type == "Visa"
