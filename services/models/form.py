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

    nco_question = ArrayField(
        models.IntegerField(),
        blank=False, null=False,
        db_column='nco_pergunta_formulario'
    )
    
    class Meta:
        db_table = 'tb_formulario'

