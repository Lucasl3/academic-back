from django.contrib.postgres.fields import ArrayField
from django.db import models

from services.helpers.factories import Factory


class Notification(Factory):
    co_notification = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_notificacao'
    )

    ds_notification = models.TextField(
        blank=False, null=False,
        db_column='ds_notificacao'
    )

    co_status = models.IntegerField(
        blank=False, null=False,
        db_column='co_status'
    )

    ds_link = models.TextField(
        blank=True, null=True,
        db_column='ds_link'
    )

    nco_user = ArrayField(
        models.IntegerField(),
        blank=False, null=False,
        db_column='nco_usuario'
    )

    class Meta:
        db_table = 'tb_notificacao'