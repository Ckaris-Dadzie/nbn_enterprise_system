
#accounts/service.py 
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError, PermissionDenied
from core.audit import log_action
from .models import User, Role, AuditLog



class UserService:

    # Create User
    @staticmethod
    @transaction.atomic
    def create_user(validated_data: dict, created_by: User) -> User:
        """
        Creates a new user account.
        Enforces role hierarchy: only Admin can create Admin users.
        Password is hashed via Argon2 (set_password).
        """
        role = validated_data.get('role')


        # Role hierarchy enforcement
        if role and role.name == 'Admin' and created_by.role_name != 'Admin':
            raise PermissionDenied('Only Admin users can create Admin accounts.')


        password = validated_data.pop('password')


        user = User(**validated_data)
        user.set_password(password)   # Argon2 hashing
        user.created_by = created_by
        user.save()


        log_action(
            user=created_by,
            action='USER_CREATED',
            resource='users',
            resource_id=str(user.id),
            details={'email': user.email, 'role': role.name if role else None},
        )


        return user


    # Update User
    @staticmethod
    @transaction.atomic
    def update_user(user: User, validated_data: dict, updated_by: User) -> User:
        """
        Partially updates a user record.
        Enforces role hierarchy on role changes.
        """
        new_role = validated_data.get('role')
        if new_role and new_role.name == 'Admin' and updated_by.role_name != 'Admin':
            raise PermissionDenied('Only Admin users can assign the Admin role.')


        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()


        log_action(
            user=updated_by,
            action='USER_UPDATED',
            resource='users',
            resource_id=str(user.id),
            details={'updated_fields': list(validated_data.keys())},
        )


        return user


    # Deactivate User (Soft Delete)
    @staticmethod
    @transaction.atomic
    def deactivate_user(user: User, deactivated_by: User) -> User:
        """
        Soft deletes a user — sets is_active=False.
        Only Admin can deactivate another Admin.
        """
        if user.role_name == 'Admin' and deactivated_by.role_name != 'Admin':
            raise PermissionDenied('Only Admin users can deactivate Admin accounts.')


        if user.id == deactivated_by.id:
            raise ValidationError('You cannot deactivate your own account.')


        user.soft_delete()


        log_action(
            user=deactivated_by,
            action='USER_DEACTIVATED',
            resource='users',
            resource_id=str(user.id),
            details={'email': user.email},
        )


        return user


    # Restore User
    @staticmethod
    @transaction.atomic
    def restore_user(user: User, restored_by: User) -> User:
        """
        Restores a previously deactivated user.
        Admin only.
        """
        if restored_by.role_name != 'Admin':
            raise PermissionDenied('Only Admin users can restore accounts.')


        user.restore()


        log_action(
            user=restored_by,
            action='USER_RESTORED',
            resource='users',
            resource_id=str(user.id),
            details={'email': user.email},
        )


        return user


    # Change Password
    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> bool:
        """
        Validates old password and sets the new one.
        Argon2 hashing is applied via set_password().
        """
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Incorrect password.'})
        user.set_password(new_password)
        user.save(update_fields=['password'])


        log_action(
            user=user,
            action='PASSWORD_CHANGED',
            resource='users',
            resource_id=str(user.id),
        )
        return True


    # Get Activity Logs
    @staticmethod
    def get_activity_logs(filters: dict = None):
        """
        Returns filtered AuditLog queryset.
        Admin only.
        """
        qs = AuditLog.objects.select_related('user').all()
        if filters:
            if filters.get('action'):
                qs = qs.filter(action=filters['action'])
            if filters.get('user_id'):
                qs = qs.filter(user_id=filters['user_id'])
            if filters.get('date_from'):
                qs = qs.filter(timestamp__date__gte=filters['date_from'])
            if filters.get('date_to'):
                qs = qs.filter(timestamp__date__lte=filters['date_to'])
        return qs
