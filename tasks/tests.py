from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Project, Team, Task, Comment

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

        self.task = Task.objects.create(
            contenido='Hello mi primera tarea por test',
            estado='completada',
            proyecto=self.project,
        )

        self.comment = Comment.objects.create(
            tarea=self.task,
            user=self.user,
            cuerpo='Comentario de prueba'
        )


    # Metodo para reutilizar y q no sean repetitivos los tests
    def authenticate(self):
        login_response = self.client.post('/api/token/',{
            'username':'testuser',
            'password':'testpassword'
        })

        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)


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
        self.authenticate()
        response = self.client.get('/api-tasks/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para crear tarea -> tiene q dar 201
    def test_crear_tarea(self):
        self.authenticate()
        response = self.client.post('/api-tasks/tasks/',{
            'contenido':'Hello mi primera tarea por test',
            'estado':'completada',
            'proyecto':int(self.project.id),
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

    # Test para editar una tarea -> tiene q dar 200
    def test_editar_tarea(self):
        self.authenticate()
        response = self.client.put(f'/api-tasks/tasks/{int(self.task.id)}/',{
            'contenido':'Esta tarea esta actualizada',
            'estado':'pendiente',
            'proyecto':int(self.project.id)
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Test para eliminar tarea -> tiene q dar 204
    def test_eliminar_tarea(self):
        self.authenticate()
        response = self.client.delete(f'/api-tasks/tasks/{int(self.task.id)}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # Test para crear una tarea sin contenido -> tiene q dar 400
    def test_crear_tarea_sin_contenido(self):
        self.authenticate()

        response = self.client.post('/api-tasks/tasks/',{
            'proyecto':int(self.project.id),
            'estado':'pendiente'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    # Test para crear un tarea sin proyecto -> tiene q dar 400
    def test_crear_tarea_sin_proyecto(self):
        self.authenticate()

        response = self.client.post('/api-tasks/tasks/', {
            'contenido':'Mi segunda tarea',
            'estado':'completada'
        }) 

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # Test de permisos

    # Test para q probar si q un usuario no puede editar tarea de otro -> tiene q dar 403 o 404
    def test_usuario_no_puede_editar_tarea_de_otro(self):
        otro_user = User.objects.create_user(
            username = 'amaury',
            password = 'dragonball0522'
        )

        login_response = self.client.post('/api/token/',{
            'username': 'amaury',
            'password': 'dragonball022'
        })

        self.client.force_authenticate(user = otro_user)

        response = self.client.put(f'/api-tasks/{self.task.id}/', {
            'contenido': 'Hola no deberia poder editar esta tarea',
            'estado':'pendiente',
            'proyecto':int(self.project.id)
        })

        self.assertIn(response.status_code, [403, 404])


    # Test para ver si el estado de una tarea esat end default
    def test_task_default(self):
        new_task = Task.objects.create(
            contenido='Tercera tarea',
            proyecto=self.project
        )

        self.assertEqual(new_task.estado, 'pendiente')      


    # Tests para estadisticas
    def test_estadisticas_endpoint(self):
        self.authenticate()

        response = self.client.get('/api-tasks/tasks/details/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_tareas', response.data)
        self.assertIn('tareas_por_estado', response.data)


    # Test para listar team con token -> tiene q dar 200 OK
    def test_listar_teams_con_token(self):
        self.authenticate()
        response = self.client.get('/api-tasks/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para crear team -> tiene q dar 201
    def test_crear_team(self):
        self.authenticate()

        response = self.client.post('/api-tasks/teams/', {
            'numero': '3',
            'jefe': self.user.id,
            'integrantes':[self.user.id]
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # Test para listar proyectos con token -> tiene q dar 200
    def test_listar_projects_con_token(self):
        self.authenticate()
        response = self.client.get('/api-tasks/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para completar tarea -> tiene q dar 200
    def test_completar_tarea(self):
        self.authenticate()
        response = self.client.post(f'/api-tasks/tasks/{self.task.id}/completar/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para listar tareas_pendientes -> tiene q dar 200
    def test_listar_tareas_pendientes(self):
        self.authenticate()
        response = self.client.get('/api-tasks/tasks/pendientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    # Test para q el staff vea todas las tareas -> tiene q dar 200
    def test_staff_ve_todas_las_tareas(self):
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        
        response = self.client.get('/api-tasks/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Test para listar comments con token -> tiene q dar 200
    def test_listar_comments_con_token(self):
        self.authenticate()
        response = self.client.get('/api-tasks/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # Test para crear un comment -> tiene q dar 201
    def test_creaar_comment(self):
        self.authenticate()
        response = self.client.post('/api-tasks/comments/', {
            'tarea':self.task.id,
            'user':self.user.id,
            'cuerpo':'Hola mi primer comentario en test'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # Test para mmodelos con metodo str:


    # Test para probar el metodo str del modelo Task
    def test_str_task(self):
        self.assertEqual(str(self.task), 'Hello mi primera tar')

    
    # Test para probar el metodo str del modelo Project
    def test_str_project(self):
        self.assertEqual(str(self.project), 'Primer proyecto')


    # Test para probar el metodo str del modelo team
    def test_str_team(self):
        self.assertEqual(str(self.team), f'Equipo {self.team.numero} de {self.team.jefe.username}')

    
    # Test para probar el metodo str del modelo comment
    def test_str_comment(self):
        self.assertEqual(str(self.comment), f'{self.comment.user.username}: {self.comment.cuerpo[:20]}')

    
    # Test esta_vencida() — sin fecha limite -> False
    def test_esta_vencida_sin_fecha(self):
        self.assertFalse(self.task.esta_vencida())

    
    def test_esta_vencida_completada(self):
        self.task.estado = 'completado'
        self.task.save()
        self.assertFalse(self.task.esta_vencida()) 

    
    # Test esta_vencida() — con fecha pasada -> True
    def test_esta_vencida_con_fecha_pasada(self):
        from django.utils import timezone
        self.task.estado = 'pendiente'
        self.task.fecha_limite = timezone.make_aware(
            timezone.datetime(2020, 1, 1)
        )
        self.task.save()
        self.assertTrue(self.task.esta_vencida())

    # Test dias_para_vencer() — sin fecha -> None
    def test_dias_para_vencer_sin_fecha(self):
        self.assertIsNone(self.task.dias_para_vencer())

    # Test dias_para_vencer() — tarea completada -> None
    def test_dias_para_vencer_completada(self):
        self.task.estado = 'completada'
        self.task.save()
        self.assertIsNone(self.task.dias_para_vencer())
        
    # Test dias_para_vencer() — con fecha futura -> numero positivo
    def test_dias_para_vencer_con_fecha_futura(self):
        from django.utils import timezone
        self.task.estado = 'pendiente'
        self.task.fecha_limite = timezone.make_aware(
            timezone.datetime(2030, 1, 1)
        )
        self.task.save()
        resultado = self.task.dias_para_vencer()
        self.assertIsNotNone(resultado)
        self.assertGreater(resultado, 0)