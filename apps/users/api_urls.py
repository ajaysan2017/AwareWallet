from django.urls import path
from rest_framework import generics, permissions
from .serializers import UserSerializer, UserRegisterSerializer


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


urlpatterns = [
    path('me/', MeView.as_view(), name='api-me'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
]
