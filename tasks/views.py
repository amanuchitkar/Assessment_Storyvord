from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminUserForList


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsAdminUserForList]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['completed']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user,
        unless the user is an admin, in which case it returns all tasks.
        """
        queryset = Task.objects.all()
        
        # If user is not admin, only show their own tasks
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        
        # Filter by created_after if provided
        created_after = self.request.query_params.get('created_after')
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)
        
        # Filter by updated_after if provided
        updated_after = self.request.query_params.get('updated_after')
        if updated_after:
            queryset = queryset.filter(updated_at__gte=updated_after)
            
        return queryset
    
    def perform_create(self, serializer):
        """Set the owner of the task to the current user."""
        serializer.save(owner=self.request.user)
