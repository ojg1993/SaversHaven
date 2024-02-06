from rest_framework import permissions


class IsSellerOrAdminElseReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Check permissions for read-only request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check permissions for write request
        else:
            return obj.seller == request.user or request.user.is_staff
