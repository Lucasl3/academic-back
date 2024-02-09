from django.db import models

from academic_backend.helpers.factories import Factory


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