"""
URL configuration for wallet_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from user.views import UserListCreateView, UserDetailView, LogoutView
from wallet.views import WalletListCreateView, WalletDetailView
from transaction.views import (
    TransactionListCreateView,
    TransactionDetailView,
    UserTransactionListAPIView,
    WalletTransactionListAPIView,
)

from .yasg import urlpatterns as doc_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", UserListCreateView.as_view(), name="User-create"),
    path("user/<str:id>", UserDetailView.as_view(), name="User-detail"),
    path("wallet/", WalletListCreateView.as_view(), name="wallet-list-create"),
    path("wallet/<str:name>", WalletDetailView.as_view(), name="wallet-detail"),
    path(
        "wallet/transaction/",
        TransactionListCreateView.as_view(),
        name="transaction-list-create",
    ),
    path(
        "wallet/transaction/<int:pk>",
        TransactionDetailView.as_view(),
        name="transaction-id",
    ),
    path(
        "wallet/transaction/user",
        UserTransactionListAPIView.as_view(),
        name="transaction-name",
    ),
    path(
        "wallet/transactions/<str:wallet_name>",
        WalletTransactionListAPIView.as_view(),
        name="wallet-transaction-name",
    ),
    path("token/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/logout/", LogoutView.as_view(), name="token_refresh"),
]

urlpatterns += doc_urls
