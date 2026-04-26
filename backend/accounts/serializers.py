# accounts/serializers.py
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Role
        fields = ['id', 'name', 'description']




class UserSerializer(BaseUserSerializer):
    role = RoleSerializer(read_only=True)


    class Meta(BaseUserSerializer.Meta):
        model  = User
        fields = ['id', 'email', 'username', 'full_name', 'role',
                  'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
