# core/permissions.py
from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """Base class — override allowed_roles in each subclass."""
    allowed_roles = []


    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, 'role') and
            request.user.role is not None and
            request.user.role.name in self.allowed_roles
        )


class IsAdminRole(RolePermission):
    allowed_roles = ['Admin']


class IsAdminOrManager(RolePermission):
    allowed_roles = ['Admin', 'Manager']


class IsFrontDesk(RolePermission):
    allowed_roles = ['Admin', 'Manager', 'FrontDeskOfficer']


class IsCashier(RolePermission):
    allowed_roles = ['Admin', 'Manager', 'Cashier']


class IsFinanceOfficer(RolePermission):
    allowed_roles = ['Admin', 'Manager', 'FinanceOfficer']


class IsInventoryManager(RolePermission):
    allowed_roles = ['Admin', 'Manager', 'InventoryManager']


class IsProductManager(RolePermission):
    allowed_roles = ['Admin', 'Manager', 'ProductManager']


class IsProductionManager(RolePermission):
    allowed_roles = ['Admin', 'Manager', 'ProductionManager']


