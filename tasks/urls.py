from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = router.urls