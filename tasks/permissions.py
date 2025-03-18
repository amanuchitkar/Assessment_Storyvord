from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the task
        return obj.owner == request.user


class IsAdminUserForList(permissions.BasePermission):
    """
    Custom permission to only allow admin users to view the full list of all users' tasks.
    Non-admin users can only see their own tasks.
    """
    def has_permission(self, request, view):
        # For list view
        if request.method == 'GET' and not view.kwargs.get('pk'):
            # If user is not admin, filter will apply in the view
            return True
        
        # For other methods and detail view
        return True 