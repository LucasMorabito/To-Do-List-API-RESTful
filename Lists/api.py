from rest_framework import viewsets, permissions, status, filters
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Endpoint register
@api_view(['POST'])  
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'User created successfully'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stats(request):
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user,completed=True).count()
    uncompleted_tasks = Task.objects.filter(user=request.user,completed=False).count()
    low_priority = Task.objects.filter(user=request.user,priority='low').count()
    medium_priority = Task.objects.filter(user=request.user,priority='medium').count()
    high_priority = Task.objects.filter(user=request.user,priority='high').count()
    return Response(
            {   
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": uncompleted_tasks,
                "low": low_priority,
                "medium": medium_priority,
                "high": high_priority
            }
        )
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'priority']             # exact filter 
    search_fields = ['title', 'description']                 # partial text search
    ordering_fields = ['created_at', 'due_date', 'priority'] # sortable fields
    ordering = ['-created_at']                               # default order
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
