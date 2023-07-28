from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.DestroyAPIView):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    lookup_field = "id"


class LogoutView(APIView):
    def post(self, request):
        return Response({"detail": "Вы успешно вышли"})
