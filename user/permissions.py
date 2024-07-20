from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsHR(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'hr'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'