from rest_framework import routers
from .api import TaskViewSet

router = routers.DefaultRouter()

router.register('tasks', TaskViewSet)

urlpatterns = router.urls