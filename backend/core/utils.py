# core/utils.py
from django.utils import timezone
from django.db import models


class SoftDeleteMixin(models.Model):
    is_active  = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    def soft_delete(self):
        self.is_active  = False
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_active', 'deleted_at'])


    def restore(self):
        self.is_active  = True
        self.deleted_at = None
        self.save(update_fields=['is_active', 'deleted_at'])


    class Meta:
        abstract = True
