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
        fields = ['id', 'numero', 'jefe_username', 'jefe', 'integrantes_usernames', 'integrantes', 'created', 'updated']
        read_only_fields = ['created', 'updated']
        extra_kwargs = {
            'jefe':{'write_only':True},
            'integrantes':{'write_only':True}
        }

    def get_integrantes_usernames(self, obj):
        return [user.username for user in obj.integrantes.all()]

class ProjectSerializer(serializers.ModelSerializer):
    tutor_username = serializers.CharField(source='tutor.username', read_only=True)
    equipo_numero = serializers.CharField(source='equipo.numero', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'tipo', 'tutor_username', 'tutor', 'equipo_numero', 'equipo', 'created', 'updated']
        read_only_fields = ['created', 'updated']
        extra_kwargs ={
            'tutor':{'write_only':True},
            'equipo':{'write_only':True}
        }

class TaskSerializer(serializers.ModelSerializer):
    proyecto_name = serializers.CharField(source='proyecto.name', read_only=True)
    asignado_a_username = serializers.CharField(source='asignado_a.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'contenido', 'proyecto_name', 'proyecto', 'estado', 
            'asignado_a_username', 'asignado_a', 'fecha_limite', 
            'created', 'updated'
        ]
        read_only_fields = ['created', 'updated']
        extra_kwargs = {
            'proyecto': {'write_only': True}, 
            'asignado_a': {'write_only': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    tarea_contenido = serializers.CharField(source='tarea.contenido', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'tarea_contenido', 'tarea', 'user_username', 'user', 'cuerpo', 'created', 'updated']
        read_only_fields = ['created', 'updated']
        extra_kwargs = {
            'tarea':{'write_only':True},
            'user':{'write_only':True}
        }
