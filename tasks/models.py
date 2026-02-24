from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import timezone, datetime

# Create your models here.

class Team(models.Model):
    numero = models.CharField(max_length = 10, unique = False)
    jefe = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    integrantes = models.ManyToManyField(User, related_name='equipos')   
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated','-created']    
    
    def __str__(self):
        return f"Equipo {self.numero} de {self.jefe.username}"

class Project(models.Model):
    Tipo = [
        ('personal', 'Personal'),
        ('trabajo', 'Trabajo')
    ]
    name = models.CharField(max_length=50)
    tutor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    equipo = models.ForeignKey(Team, on_delete=models.CASCADE) 
    tipo = models.CharField(max_length = 20, choices=Tipo)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated','-created']    
    
    def __str__(self):
        return self.name

class Task(models.Model):
    Estado = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En_progreso'),
        ('completada', 'Completada'),
        ('pausada', 'Pausada')   
    ]
    
    contenido = models.TextField()
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tareas')  
    estado = models.CharField(max_length=20, choices=Estado, default='pendiente')
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    fecha_limite = models.DateTimeField(blank = True, null =True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self):
        return self.contenido[:20]
    
    def esta_vencida(self):
        try:
            if not self.fecha_limite or self.estado == 'completada':
                return False
            
            hoy = datetime.now().date() 
            
            if isinstance(self.fecha_limite, datetime):
                fecha_lim = self.fecha_limite.date()
            else:
                fecha_lim = self.fecha_limite

            return fecha_lim < hoy
            
        except Exception:
            return False
        
    def dias_para_vencer(self):
        try:
            if not self.fecha_limite:
                return None

            if self.estado == 'completada':
                return None
            
            hoy = timezone.now().date()
            
            if isinstance(self.fecha_limite, datetime):
                fecha_lim = self.fecha_limite.date()
            else:
                fecha_lim = self.fecha_limite

            dias = (fecha_lim - hoy).days

            return dias
            
        except Exception as e:
           # print(f'El error es {e}')
            return None
        
            

class Comment(models.Model):
    tarea = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comentarios') 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.user.username}: {self.cuerpo[:20]}'
    
