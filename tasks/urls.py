from rest_framework import routers
from django.urls import path
from .views import TeamViewSet, ProjectViewSet, TaskViewSet, CommentViewSet, TaskViewDb

router = routers.DefaultRouter()

router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('tasks/details/', TaskViewDb.as_view(), name = 'tasks_details')
    ]

urlpatterns += router.urls