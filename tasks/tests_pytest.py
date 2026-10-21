from django.contrib.auth.models import User
import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from .models import Project, Team

@pytest.fixture
def usuario():
    return User.objects.create_user(
        username = 'amaury',
        password='dragonball0522'
    )


@pytest.fixture
def equipo(usuario):
    return Team.objects.create(
        numero = '1',
        jefe = usuario
    )


@pytest.fixture
def proyecto(usuario, equipo):
    equipo.integrantes.set([usuario])
    return Project.objects.create(
        name = 'Primer proyecto',
        tutor=usuario,
        equipo = equipo,
        tipo = 'personal'        
    )
    

@pytest.mark.django_db
def test_usuario_creado(usuario):
    assert usuario.username == 'amaury'

@pytest.fixture
def api_client_autenticado(usuario):
    client = APIClient()
    client.force_authenticate(user=usuario)
    return client

@pytest.mark.django_db
@patch('tasks.signals.resend.Emails.send')
def test_verificar_que_email_se_llama(mock_enviar, api_client_autenticado, usuario, proyecto):
    response = api_client_autenticado.post('/api-tasks/tasks/',{
        'contenido':'Hello mi primera tarea por test',
        'estado':'completada',
        'proyecto':proyecto.id,
        'asignado_a':usuario.id
    })

    assert response.status_code == 201
    mock_enviar.assert_called_once()
