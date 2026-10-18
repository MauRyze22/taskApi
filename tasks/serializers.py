from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, Project, Task, Comment
from django.utils.timezone import now
from django.db.models import Q
from django.db import transaction

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

    
    def create(self, validated_data):
        integrantes = validated_data.pop('integrantes', [])
        with transaction.atomic():
            team = Team.objects.create(**validated_data)
            if team.jefe not in integrantes:
                integrantes.append(team.jefe)
                
            team.integrantes.set(integrantes)
        return team

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        request = self.context.get('request')
        if request:
           user = request.user
           self.fields['equipo'].queryset = Team.objects.filter(
                Q(jefe = user)|
                Q(integrantes = user)
        )
           
    def validate(self, attrs):
        tutor = attrs.get('tutor', getattr(self.instance, 'tutor', None))
        equipo = attrs.get('equipo', getattr(self.instance, 'equipo', None))

        if tutor and equipo:
            if not equipo.integrantes.filter(id = tutor.id).exists():
                raise serializers.ValidationError({
                    'tutor':'Este usuario no es integrante del equipo'
                })

        return attrs

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        request = self.context.get('request')
        if request:
           user = request.user
           self.fields['proyecto'].queryset = Project.objects.filter(
                Q(tutor = user)|
                Q(equipo__integrantes = user)|
                Q(equipo__jefe = user)
           )

    def validate(self, attrs):
        asignado_a = attrs.get('asignado_a', getattr(self.instance, 'asignado_a', None))
        proyecto = attrs.get('proyecto', getattr(self.instance, 'proyecto', None))
    
        if asignado_a and proyecto:
            if not proyecto.equipo.integrantes.filter(id = asignado_a.id).exists():
                raise serializers.ValidationError({
                    'asignado_a': "El usuario no pertenece al equipo del proyecto"
                })
            
        return attrs

    def validate_fecha_limite(self, value):
        if value and value < now():
            raise serializers.ValidationError("La fecha limite de esta tarea no puede ser anterior al dia actual")
        return value

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            user = request.user
            self.fields['tarea'].queryset = Task.objects.filter(
                Q(asignado_a = user)|
                Q(proyecto__tutor = user)|
                Q(proyecto__equipo__jefe = user)|
                Q(proyecto__equipo__integrantes = user)
            )

