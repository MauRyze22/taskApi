from django.contrib.auth.models import User
from .serializers import *
from .models import Profile
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user':user.username,
            'access':str(refresh.access_token),
            'refresh':str(refresh),
            'message':'Usuario registrado exitosamente',
        }, status=status.HTTP_201_CREATED)
    
        