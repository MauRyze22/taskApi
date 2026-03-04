from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from .models import Profile
from rest_framework import generics, permissions, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

# Create your views here.

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user = self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user':user.username,
            'token':token.key,
            'message':'Usuario registrado exitosamente',
        }, status=status.HTTP_201_CREATED)
    
        