from django.contrib.postgres.fields import ArrayField
from django.db import models

from services.helpers.factories import Factory

class Form(Factory):
    co_form = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_formulario'
    )

    no_form = models.CharField(
        max_length=255, blank=False, null=False,
        db_column='no_formulario'
    )

    ds_form = models.TextField(
        blank=False, null=False,
        db_column='ds_formulario'
    )

    nco_step = ArrayField(
        models.IntegerField(),
        blank=False, null=False,
        db_column='nco_etapa_formulario'
    )

    nco_status = ArrayField(
        models.TextField(),
        blank=False, null=False,
        db_column='nco_status_formulario'
    )
    
    class Meta:
        db_table = 'tb_formulario'

