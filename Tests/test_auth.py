import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_tasks():
    client = APIClient()
    response = client.get('/api/tasks/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_authenticated_user_can_see_own_tasks():
    user = User.objects.create_user(username='tester', password='test123')
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/tasks/')
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_user_cannot_see_other_users_tasks():
    # create 2 users
    user1 = User.objects.create_user(username='user1', password='test123')
    user2 = User.objects.create_user(username='user2', password='test123')
    
    client1 = APIClient()
    client1.force_authenticate(user=user1)
    client1.post('/api/tasks/', {
        'title': 'private task',
        'description': 'only user 1 can see it',
        'completed': False,
        'priority': 'medium'
    })

    client2 = APIClient()
    client2.force_authenticate(user=user2)
    response = client2.get('/api/tasks/')
    
    assert response.data['count'] == 0
    
# TEST ENDPOINTS (register and login)

@pytest.mark.django_db
def test_user_can_register_with_valid_data():
    client = APIClient()
    response = client.post('/api/register/', {'username':'tester','password':'12345'})
    assert response.status_code == 201
    
@pytest.mark.django_db
def test_registered_user_can_obtain_token():
    User.objects.create_user(username='tester',password='12345')
    client = APIClient()
    response = client.post('/api/login/', {'username':'tester','password':'12345'})
    assert response.status_code == 200