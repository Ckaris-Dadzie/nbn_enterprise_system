# accounts/serializers.py
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User, Role, AuditLog

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Role
        fields = ['id', 'name', 'description']



# User Serializer — used for read operations and Djoser me/ endpoint
class UserSerializer(BaseUserSerializer):
    role = RoleSerializer(read_only=True)


    class Meta(BaseUserSerializer.Meta):
        model  = User
        fields = ['id', 'email', 'username', 'full_name', 'role',
                  'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

# Create User Serializer — Admin/Manager creates new staff accounts
class CreateUserSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    role_id          = serializers.PrimaryKeyRelatedField(
                           queryset=Role.objects.all(),
                           source='role',
                       )


    class Meta:
        model  = User
        fields = [
            'email', 'username', 'full_name',
            'role_id', 'password', 'confirm_password',
        ]


    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match.'} 
                )
        return attrs


    def validate_role_id(self, role):
        """
        Enforce role hierarchy:
        - Only Admin can assign the Admin role.
        - Manager cannot create Admin users.
        """
        request = self.context.get('request')
        if role.name == 'Admin' and request.user.role_name != 'Admin':
            raise serializers.ValidationError(
                'Only Admin users can assign the Admin role.'
            )
        return role


# Update User Serializer — partial updates to an existing user
class UpdateUserSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
                  queryset=Role.objects.all(),
                  source='role',
                  required=False,
              )


    class Meta:
        model  = User
        fields = ['full_name', 'username', 'role_id']


    def validate_role_id(self, role):
        request = self.context.get('request')
        if role and role.name == 'Admin' and request.user.role_name != 'Admin':
            raise serializers.ValidationError(
                'Only Admin users can assign the Admin role.'
            )
        return role


# AuditLog Serializer — read-only
class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)


    class Meta:
        model  = AuditLog
        fields = [
            'id', 'user_name', 'action', 'resource',
            'resource_id', 'details', 'timestamp',
        ]
