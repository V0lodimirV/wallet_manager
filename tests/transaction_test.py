from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from transaction.models import Transaction
from user.models import User
from wallet.models import Wallet
from wallet.models.wallet import generate_wallet_name


client = APIClient()


@pytest.fixture
def create_user():
    def _create_user(username, password):
        return User.objects.create_user(username=username, password=password)

    return _create_user


@pytest.fixture
def create_wallet():
    def _create_wallet(name, user, currency, balance):
        return Wallet.objects.create(
            name=name, user=user, currency=currency, balance=balance
        )

    return _create_wallet


@pytest.mark.django_db
def test_create_transaction(client, create_user, create_wallet):
    # "создание транзакции"
    user = create_user(username="test_user", password="test_password")
    sender_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=100.00
    )
    receiver_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=0.00
    )

    url = reverse("transaction-list-create")
    data = {
        "sender": sender_wallet.name,
        "receiver": receiver_wallet.name,
        "transfer_amount": "50.00",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.count() == 1
    transaction = Transaction.objects.first()
    assert transaction.sender == sender_wallet
    assert transaction.receiver == receiver_wallet
    assert transaction.transfer_amount == Decimal("50.00")
    assert transaction.commission == Decimal("0.00")
    assert transaction.status == "PAID"
    assert transaction.timestamp is not None


@pytest.mark.django_db
def test_create_transaction_insufficient_balance():
    # Создаем два кошелька с разной валютой для проведения транзакции
    sender_wallet = Wallet.objects.create(
        name=generate_wallet_name(), type="Visa", currency="USD"
    )
    receiver_wallet = Wallet.objects.create(
        name=generate_wallet_name(), type="Visa", currency="EUR"
    )

    # Подготавливаем данные для транзакции
    data = {
        "sender": sender_wallet.name,
        "receiver": receiver_wallet.name,
        "transfer_amount": "100.00",
    }

    # Выполняем POST-запрос для создания транзакции
    client = APIClient()
    url = "/wallet/transaction/"
    response = client.post(url, data, format="json")

    # Проверяем, что транзакция не была создана из-за недостаточного баланса
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_create_transaction_with_insufficient_funds(client, create_user, create_wallet):
    user = create_user(username="test_user", password="test_password")
    sender_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=30.00
    )
    receiver_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=0.00
    )

    url = reverse("transaction-list-create")
    data = {
        "sender": sender_wallet.name,
        "receiver": receiver_wallet.name,
        "transfer_amount": "50.00",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Недостаточно средств для перевода" in response.data


@pytest.mark.django_db
def test_create_transaction_with_different_currencies(
    client, create_user, create_wallet
):
    user = create_user(username="test_user", password="test_password")
    sender_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=100.00
    )
    receiver_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="EUR", balance=0.00
    )

    url = reverse("transaction-list-create")
    data = {
        "sender": sender_wallet.name,
        "receiver": receiver_wallet.name,
        "transfer_amount": "50.00",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Пожалуйста, выберите кошельки с одинаковой валютой" in response.data


@pytest.mark.django_db
def test_create_transaction_with_negative_amount(client, create_user, create_wallet):
    user = create_user(username="test_user", password="test_password")
    sender_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=100.00
    )
    receiver_wallet = create_wallet(
        name=generate_wallet_name(), user=user, currency="USD", balance=0.00
    )

    url = reverse("transaction-list-create")
    data = {
        "sender": sender_wallet.name,
        "receiver": receiver_wallet.name,
        "transfer_amount": "-50.00",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "сумма должна быть больше 0" in response.data
