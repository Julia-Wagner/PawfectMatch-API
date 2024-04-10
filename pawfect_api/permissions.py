from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsShelter(permissions.BasePermission):
    """
    Custom permission to only allow shelters to create, edit, or delete dogs.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            return request.user.profile.type == 'shelter'
        return False
