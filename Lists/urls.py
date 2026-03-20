from django.urls import path
from rest_framework import routers
from .api import TaskViewSet, register

router = routers.DefaultRouter()

router.register('tasks', TaskViewSet, basename='task')

urlpatterns = router.urls
