from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from rest_framework.decorators import action

# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class=TeamSerializer
    permission_classes = [permissions.IsAuthenticated] 
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Team.objects.all()
        return Team.objects.filter(Q(jefe=user)|
                                   Q(integrantes=user)).select_related('jefe').prefetch_related('integrantes').distinct()


    def perform_create(self, serializer):
        team = serializer.save()
        
        if not team.integrantes.filter(id=team.jefe.id):
            team.integrantes.add(team.jefe)

        
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class=ProjectSerializer          
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(Q(tutor=user)|
                                      Q(equipo__jefe=user)|
                                      Q(equipo__integrantes=user)
                                      ).select_related('tutor', 'equipo__jefe'
                                      ).prefetch_related('equipo__integrantes').distinct()
                                      
    
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class=TaskSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(Q(asignado_a=user)|
                                   Q(proyecto__tutor=user)|
                                   Q(proyecto__equipo__jefe=user)|
                                   Q(proyecto__equipo__integrantes=user)).select_related(
                                    'asignado_a', 'proyecto__tutor', 'proyecto__equipo__jefe',
                                    ).prefetch_related('proyecto__equipo__integrantes').distinct()
                                   
    
    @action(detail = True, methods=['post'])
    def completar(self, request, pk=None):
        task = self.get_object()
        task.estado = 'completada'
        task.save()
        
        serializer = self.get_serializer(task)
        return Response({'message':'Tarea completada correctamente', 'task':serializer.data})
    
    
    @action(detail = False, methods=['get'])
    def pendientes(self, request):
        tasks = self.get_queryset().filter(estado = 'pendiente')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class=CommentSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(Q(user=user)|
                                      Q(tarea__asignado_a=user)|
                                      Q(tarea__proyecto__tutor=user)|
                                      Q(tarea__proyecto__equipo__jefe=user)|
                                      Q(tarea__proyecto__equipo__integrantes=user)).select_related(
                                        'user', 'tarea__asignado_a', 'tarea__proyecto__tutor',
                                        'tarea__proyecto__equipo__jefe',
                                      ).prefetch_related('tarea__proyecto__equipo__integrantes').distinct()
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

