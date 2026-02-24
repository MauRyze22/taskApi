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
    

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username = username, password = password)
        
        if user:
            token, created = Token.objects.get_or_create(user = user)
            
            if created:
                return Response({
                    'user':user.username,
                    'token':token.key,
                    'message':'Inicio de sesion exitoso',
                }, status=status.HTTP_200_OK)
            
            else:
                token.delete()
                
                token = Token.objects.create(user = user)
                
                return Response({
                    'user':user.username,
                    'token':token.key,
                    'message':'Inicio de sesion exitoso',
                }, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'No existen esas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        
        return Response({'message':'Cierre de sesion exitoso'})
        