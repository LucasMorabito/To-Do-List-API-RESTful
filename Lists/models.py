from django.db import models

# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('l', 'Low'),
        ('m', 'Medium'),
        ('h', 'High'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    priority =  models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='m'
    )
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)