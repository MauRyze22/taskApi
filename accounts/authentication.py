from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class CustomTokenAuthentication(TokenAuthentication):
    
    def token_expirado(self, token):
        tiempo_de_uso = timezone.now() - token.created
        tiempo_restante = timedelta(seconds=settings.EXPIRING_TOKEN_DURATION) - tiempo_de_uso
        
        expirado = tiempo_restante < timedelta(seconds=0)
        
        return expirado
            
    
    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed("Token invalido")
        
        if not token.user.is_active:
            raise AuthenticationFailed('Usuario no activo')
        
        is_expired = self.token_expirado(token)
        
        if is_expired:
            raise AuthenticationFailed('Token vencido')
        
        return (token.user, token)
       