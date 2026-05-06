from rest_framework import permissions
from .models import AllLog

class RolePermission(permissions.BasePermission):
    """
    Generic role-based permission
    """

    allowed_roles = []

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        try:
            alllog_user = AllLog.objects.get(id=user.id)
            return alllog_user.role in self.allowed_roles
        except AllLog.DoesNotExist:
            return False

class IsSupervisor(RolePermission):
    allowed_roles = ["supervisor"]

class IsAnganwadi(RolePermission):
    allowed_roles = ["anganwadi"]

class IsDPO(RolePermission):
    allowed_roles = ["dpo"]

class IsCDPO(RolePermission):
    allowed_roles = ["cdpo"]

class IsDirector(RolePermission):
    allowed_roles = ["director"]