from django.urls import path, include
from rest_framework import routers
from .api import TaskViewSet, stats

router = routers.DefaultRouter()

router.register('tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('stats/', stats),
    path('', include(router.urls))
]