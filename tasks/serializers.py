from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, Project, Task, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class TeamSerializer(serializers.ModelSerializer):
    jefe_username = serializers.CharField(source='jefe.username', read_only=True)
    integrantes_usernames = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'numero', 'jefe_username', 'integrantes_usernames', 'created', 'updated']
        read_only_fields = ['created', 'updated']
    
    def get_integrantes_usernames(self, obj):
        return [user.username for user in obj.integrantes.all()]

class ProjectSerializer(serializers.ModelSerializer):
    tutor_username = serializers.CharField(source='tutor.username', read_only=True)
    equipo_numero = serializers.CharField(source='equipo.numero', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'tipo', 'tutor_username', 'equipo_numero', 'created', 'updated']
        read_only_fields = ['created', 'updated']

class TaskSerializer(serializers.ModelSerializer):
    proyecto_name = serializers.CharField(source='proyecto.name', read_only=True)
    asignado_a_username = serializers.CharField(source='asignado_a.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'contenido', 'proyecto_name', 'estado', 
            'asignado_a_username', 'fecha_limite', 
            'created', 'updated'
        ]
        read_only_fields = ['created', 'updated']

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    tarea_contenido = serializers.CharField(source='tarea.contenido', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'tarea_contenido', 'user_username', 'cuerpo', 'created', 'updated']
        read_only_fields = ['created', 'updated']
