# core/audit.py
def log_action(user, action, resource, resource_id, details=None):
    from accounts.models import AuditLog
    AuditLog.objects.create(
        user        = user,
        action      = action,
        resource    = resource,
        resource_id = str(resource_id),
        details     = details or {},
    )
