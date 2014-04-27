from rest_framework import permissions

class ReadOnlyPermission(permissions.BasePermission):
    """
    Allows read-only operations from both authenticated and anonymous users
    """

    authenticated_users_only = False

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)
