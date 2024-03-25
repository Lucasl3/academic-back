from django.db import models

from services.helpers.factories import Factory


class Tutorial(Factory):
    co_tutorial = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_tutorial'
    )

    no_tutorial = models.CharField(
        max_length=255, blank=False, null=False,
        db_column='no_titulo_tutorial'
    )

    ds_tutorial = models.TextField(
        blank=False, null=False,
        db_column='ds_tutorial'
    )

    content_tutorial = models.TextField(
        blank=False, null=False,
        db_column='content_tutorial',
        default=''
    )

    co_status = models.BooleanField(
        blank=False, null=False,
        db_column="co_status",
        default=True
    )
    
    class Meta:
        db_table = 'tb_tutorial'