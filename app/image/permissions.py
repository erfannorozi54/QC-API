from rest_framework.permissions import BasePermission


class ConstantTokenPermission(BasePermission):
    """
    Custom permission that allows access only if the constant token authentication is successful.
    """

    def has_permission(self, request, view):
        # This will always allow the request if the ConstantTokenAuthentication is successful
        return True
