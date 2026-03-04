"""
URL configuration for taskApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion de taskApi",
      default_version='v1',
      description="Documentacion API de manager task",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="amaurymperez22@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name = 'token_obtain'),
    path('api-tasks/', include('tasks.urls')),
    path('accounts/', include('accounts.urls')),
]
    