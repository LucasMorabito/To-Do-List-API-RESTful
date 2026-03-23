import pytest
from Lists.models import Task
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_task():
    client = APIClient()
    user = User.objects.create_user(username='tester', password='test123')
    client.force_authenticate(user=user)
    response = client.post('/api/tasks/', {'title':'task1', 'description':'desc1'})
    assert response.status_code == 201
    assert Task.objects.count() == 1

@pytest.mark.django_db   
def test_task_is_isolated_per_user():
    # create user 1
    client1 = APIClient()
    user1 = User.objects.create_user(username='tester1', password='test123')
    client1.force_authenticate(user=user1)
    # create user 2
    client2 = APIClient()
    user2 = User.objects.create_user(username='tester2', password='test123')
    client2.force_authenticate(user=user2)
    # create task user 1
    client1.post('/api/tasks/', {'title':'task1', 'description':'desc1'})
    response = client2.get('/api/tasks/')
    # verification
    assert response.data['count'] == 0

@pytest.mark.django_db 
def test_user_can_update_task():
    client = APIClient()
    user = User.objects.create_user(username='tester', password='test123')
    client.force_authenticate(user=user)
    response_post = client.post('/api/tasks/', {'title':'task1', 'description':'desc1'})
    task_id = response_post.data['id']
    response = client.patch(f'/api/tasks/{task_id}/', {'title':'different title'})
    assert response.status_code == 200
