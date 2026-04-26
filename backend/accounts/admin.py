#accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, AuditLog




@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display  = ['name', 'description', 'created_at']
    search_fields = ['name']




@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display   = ['email', 'full_name', 'role', 'is_active', 'created_at']
    list_filter    = ['role', 'is_active']
    search_fields  = ['email', 'full_name', 'username']
    ordering       = ['full_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']


    fieldsets = (
        ('Identity',    {'fields': ('id', 'email', 'username', 'full_name')}),
        ('Role',        {'fields': ('role',)}),
        ('Password',    {'fields': ('password',)}),
        ('Status',      {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Timestamps',  {'fields': ('created_at', 'updated_at', 'last_login')}),
        ('Created by',  {'fields': ('created_by',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'username', 'full_name', 'role', 'password1', 'password2'),
        }),
    )




@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display  = ['timestamp', 'user', 'action', 'resource', 'resource_id']
    list_filter   = ['action', 'resource']
    search_fields = ['action', 'resource_id', 'user__email']
    readonly_fields = ['user', 'action', 'resource', 'resource_id', 'details',
                       'ip_address', 'timestamp']


    def has_add_permission(self, request):    return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
