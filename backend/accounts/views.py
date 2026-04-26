#accounts/views.py 
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.permissions import IsAdminOrManager, IsAdminRole
from core.pagination import StandardResultsPagination
from core.responses import success_response, error_response
from .models import User, Role
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    RoleSerializer,
    AuditLogSerializer,
)
from .services import UserService




# ─────────────────────────────────────────────────────────────────
# User ViewSet
# ─────────────────────────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(summary='List all users', tags=['Users']),
    create=extend_schema(summary='Create new user', tags=['Users']),
    retrieve=extend_schema(summary='Get user details', tags=['Users']),
    partial_update=extend_schema(summary='Update user', tags=['Users']),
    destroy=extend_schema(summary='Deactivate user', tags=['Users']),
)
class UserViewSet(ModelViewSet):
    queryset           = User.objects.select_related('role').filter(is_active=True)
    pagination_class   = StandardResultsPagination
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    http_method_names  = ['get', 'post', 'patch', 'delete']


    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action in ['partial_update', 'update']:
            return UpdateUserSerializer
        return UserSerializer


    def create(self, request):
        serializer = CreateUserSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user(
            validated_data=serializer.validated_data,
            created_by=request.user,
        )
        return success_response(
            data=UserSerializer(user).data,
            message='User created successfully.',
            status=201,
        )


    def partial_update(self, request, pk=None):
        user       = self.get_object()
        serializer = UpdateUserSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        updated = UserService.update_user(
            user=user,
            validated_data=serializer.validated_data,
            updated_by=request.user,
        )
        return success_response(
            data=UserSerializer(updated).data,
            message='User updated successfully.',
        )


    def destroy(self, request, pk=None):
        user = self.get_object()
        UserService.deactivate_user(user=user, deactivated_by=request.user)
        return success_response(message='User deactivated successfully.')


    # ── Custom actions ───────────────────────────────────────────


    @extend_schema(summary='Deactivate a user', tags=['Users'])
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        user = self.get_object()
        UserService.deactivate_user(user=user, deactivated_by=request.user)
        return success_response(message='User deactivated.')


    @extend_schema(summary='Restore a deactivated user', tags=['Users'])
    @action(
        detail=True,
        methods=['post'],
        url_path='restore',
        permission_classes=[IsAuthenticated, IsAdminRole],
    )
    def restore(self, request, pk=None):
        # Include inactive users for this action
        user = User.objects.get(pk=pk)
        UserService.restore_user(user=user, restored_by=request.user)
        return success_response(message='User restored.')


    @extend_schema(summary='View audit logs', tags=['Users'])
    @action(
        detail=False,
        methods=['get'],
        url_path='activity-logs',
        permission_classes=[IsAuthenticated, IsAdminRole],
    )
    def activity_logs(self, request):
        filters = {
            'action':    request.query_params.get('action'),
            'user_id':   request.query_params.get('user_id'),
            'date_from': request.query_params.get('date_from'),
            'date_to':   request.query_params.get('date_to'),
        }
        logs       = UserService.get_activity_logs(filters=filters)
        serializer = AuditLogSerializer(logs, many=True)
        return success_response(data=serializer.data)




# ─────────────────────────────────────────────────────────────────
# Role ViewSet — read only
# ─────────────────────────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(summary='List all roles', tags=['Roles']),
    retrieve=extend_schema(summary='Get role details', tags=['Roles']),
)
class RoleViewSet(ReadOnlyModelViewSet):
    queryset           = Role.objects.all()
    serializer_class   = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

