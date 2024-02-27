from django.db import models

from django.contrib.postgres.fields import ArrayField
from services.helpers.factories import Factory

class FormQuestion(Factory):
    co_form_question = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_pergunta_formulario'
    )

    no_question = models.CharField(
        max_length=255, blank=False, null=False,
        db_column='no_titulo_pergunta'
    )

    ds_question = models.TextField(
        blank=False, null=False,
        db_column='ds_pergunta'
    )

    co_type_question = models.IntegerField(
        blank=False, null=False,
        db_column='co_tipo_pergunta'
    )

    nco_form_item = ArrayField(
        models.IntegerField(),
        blank=True, null=True,
        db_column='nco_item_formulario'
    )

    class Meta:
        db_table = 'tb_pergunta_formulario'


class FormItem(Factory):
    co_form_item = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_item_formulario'
    )

    ds_item = models.TextField(
        blank=False, null=False,
        db_column='ds_item'
    )

    class Meta:
        db_table = 'tb_item_formulario'