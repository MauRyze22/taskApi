from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Project, Team

# Create your tests here.

class TaskApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.team = Team.objects.create(
            numero = '1',
            jefe = self.user
        )

        self.team.integrantes.add(self.user)
    
        self.project = Project.objects.create(
            name = 'Primer proyecto',
            tutor=self.user,
            equipo = self.team,
            tipo = 'personal'
        )

    # Test de listar tares sin autorizacion -> tiene q dar 401 
    def test_listar_tareas_sin_token(self):
        response = self.client.get('/api-tasks/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # Test para probar JWT con acces y refresh -> tiene q dar 200 
    def test_obtener_token_correcto(self):
        response = self.client.post('/api/token/',{
            'username':'testuser',
            'password':'testpassword'
        })

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para probar si las credenciales son correctas -> tiene q dar 401
    def test_token_credenciales_correctas(self):
        response = self.client.post('/api/token/', {
            'username':'testuser',
            'password':'passwordincorrect'
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    
    # Test para listar tareas con token -> tiene q dar 200
    def test_listar_tareas_con_token(self):
        login_response = self.client.post('/api/token/',{
            'username':'testuser',
            'password':'testpassword'
        })

        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+ token)
        response = self.client.get('/api-tasks/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para crear tarea -> tiene q dar 201
    def test_crear_tarea(self):
        login_response = self.client.post('/api/token/', {
            'username':'testuser',
            'password':'testpassword'
        })

        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        response = self.client.post('/api-tasks/tasks/',{
            'contenido':'Hello mi primero proyecto por test',
            'estado':'completada',
            'proyecto':int(self.project.id),
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        