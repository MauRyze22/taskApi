from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    numero = models.CharField(max_length=50, blank = True, null =True, default='No registrado')
    email = models.EmailField()
    imagen = models.ImageField(upload_to = 'perfiles/',null = True, blank = True)
    pais = models.CharField(max_length = 20, null = True, blank = True, default='No registrado')
    rol = models.CharField(max_length = 50, default = 'usuario', null = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Perfil de: {self.user.username}'
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user = instance, email = instance.email)
            
    @receiver(post_save, sender = User)
    def save_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()