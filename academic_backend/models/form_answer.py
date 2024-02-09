from django.db import models

from academic_backend.helpers.factory import Factory
from academic_backend.models import User, Form

class AnswerForm(Factory):
    co_answer_form = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_resposta_formulario'
    )

    co_status = models.IntegerField(
        blank=False, null=False,
        db_column='co_status'
    )

    co_form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE, null=False, blank=False,
        db_column='co_formulario'
    )

    co_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, null=False, blank=False,
        db_column='co_usuario'
    )

    class Meta:
        db_table = 'tb_resposta_formulario'


class MessageForm(Factory):
    co_message_form = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_mensagem_formulario'
    )

    co_answer_form = models.ForeignKey(
        AnswerForm,
        on_delete=models.CASCADE, null=False, blank=False,
        db_column='co_resposta_formulario'
    )

    ds_message = models.TextField(
        blank=False, null=False,
        db_column='ds_conteudo_mensagem'
    )

    class Meta:
        db_table = 'tb_mensagem_formulario'