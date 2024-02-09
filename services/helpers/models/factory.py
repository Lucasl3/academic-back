from datetime import datetime
from typing import Any

from django.db import models


class ManageFactory(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Factory(models.Model):
    dt_created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    dt_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    dt_deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    objects = ManageFactory()
    all_objects = models.Manager()

    def hard_delete(
        self, using: Any = ..., keep_parents: bool = ...
    ) -> tuple[int, dict[str, int]]:
        return super().delete(using, keep_parents)

    def delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    def rollback(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True
