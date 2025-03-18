from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task


class TaskAPITestCase(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword'
        )
        
        self.another_user = User.objects.create_user(
            username='another',
            email='another@example.com',
            password='anotherpassword'
        )
        
        # Create test tasks
        self.admin_task = Task.objects.create(
            title='Admin Task',
            description='Task created by admin',
            owner=self.admin_user
        )
        
        self.user_task = Task.objects.create(
            title='User Task',
            description='Task created by regular user',
            owner=self.regular_user
        )
        
        # Setup API client
        self.client = APIClient()
    
    def test_list_tasks_admin(self):
        """Test that admin users can see all tasks"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Admin sees all tasks
    
    def test_list_tasks_regular_user(self):
        """Test that regular users can only see their own tasks"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('task-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Regular user only sees their own tasks
    
    def test_create_task(self):
        """Test creating a new task"""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'completed': False
        }
        
        response = self.client.post(reverse('task-list'), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data['owner'], self.regular_user.username)
    
    def test_update_own_task(self):
        """Test that a user can update their own task"""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'completed': True
        }
        
        response = self.client.put(
            reverse('task-detail', kwargs={'pk': self.user_task.id}),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user_task.refresh_from_db()
        self.assertEqual(self.user_task.title, 'Updated Task')
        self.assertEqual(self.user_task.completed, True)
    
    def test_update_other_user_task(self):
        """Test that a user cannot update another user's task"""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'title': 'Trying to update admin task',
            'description': 'This should fail',
            'completed': True
        }
        
        response = self.client.put(
            reverse('task-detail', kwargs={'pk': self.admin_task.id}),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.admin_task.refresh_from_db()
        self.assertNotEqual(self.admin_task.title, 'Trying to update admin task')
    
    def test_delete_own_task(self):
        """Test that a user can delete their own task"""
        self.client.force_authenticate(user=self.regular_user)
        
        response = self.client.delete(
            reverse('task-detail', kwargs={'pk': self.user_task.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=self.user_task.id).count(), 0)
    
    def test_delete_other_user_task(self):
        """Test that a user cannot delete another user's task"""
        self.client.force_authenticate(user=self.regular_user)
        
        response = self.client.delete(
            reverse('task-detail', kwargs={'pk': self.admin_task.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.filter(id=self.admin_task.id).count(), 1)
    
    def test_filter_by_completed(self):
        """Test filtering tasks by completed status"""
        # Create a completed task
        Task.objects.create(
            title='Completed Task',
            description='This task is completed',
            completed=True,
            owner=self.regular_user
        )
        
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('task-list') + '?completed=true')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Completed Task')
    
    def test_filter_by_created_after(self):
        """Test filtering tasks by created_after date"""
        # This test would be more complex in a real scenario
        # as it would require manipulating dates
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('task-list') + '?created_after=2000-01-01')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # All tasks should be created after 2000-01-01
        self.assertEqual(len(response.data['results']), 1)
