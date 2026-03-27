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
    user_tasks = Task.objects.filter(user=request.user)
    total = user_tasks.count()
    completed = user_tasks.filter(completed=True).count()
    uncompleted = user_tasks.filter(completed=False).count()
    low = user_tasks.filter(priority='low')
    medium = user_tasks.filter(priority='medium')
    high = user_tasks.filter(priority='high')
    return Response(
            {   
                "total": total,
                "completed": completed,
                "pending": uncompleted,
                "low": low,
                "medium": medium,
                "high": high
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
