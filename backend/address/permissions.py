from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    message = 'Permission Denied.'

    def has_permission(self, request, view):
        # Check permissions for GET request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check permissions for other request
        else:
            return bool(request.user and request.user.is_staff)
