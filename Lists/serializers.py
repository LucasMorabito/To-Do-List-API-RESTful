from rest_framework import serializers
from .models import Task

# Serializer at Task:
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'priority', 'due_date', 'created_at')
        read_only_fields = ('id', 'created_at', )