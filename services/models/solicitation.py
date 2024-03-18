from django.db import models

from django.contrib.postgres.fields import ArrayField
from services.helpers.factories import Factory
from services.models import User, Form

class Solicitation(Factory):
    co_solicitation = models.AutoField(
        primary_key=True, 
        db_column='co_solicitacao'
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

    nco_answer_form_question = ArrayField(
        models.IntegerField(),
        blank=True, null=True,
        db_column='nco_resposta_questao_formulario'
    )

    class Meta:
        db_table = 'tb_solicitacao'


class AnswerFormQuestion(Factory):
    from services.models.form_question import FormQuestion

    co_answer_form_question = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_pergunta_resposta_formulario'
    )

    co_solicitation = models.ForeignKey(
        Solicitation,
        on_delete=models.CASCADE, null=False, blank=False,
        db_column='co_solicitacao'
    )

    co_form_question = models.ForeignKey(
        FormQuestion,
        on_delete=models.CASCADE, null=False, blank=False,
        db_column='co_pergunta_formulario'
    )

    nds_answer_question_item = ArrayField(
        models.IntegerField(),
        blank=True, null=True,
        db_column='ds_resposta_questao_item'
    )

    nds_answer_question_str = ArrayField(
        models.TextField(),
        blank=True, null=True,
        db_column='ds_resposta_questao_str'
    )
    

    class Meta:
        db_table = 'tb_pergunta_resposta_formulario'


class MessageForm(Factory):
    co_message_form = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_mensagem_formulario'
    )

    co_solicitation = models.ForeignKey(
        Solicitation,
        on_delete=models.CASCADE, null=False, blank=False,
        db_column='co_solicitacao'
    )

    ds_message = models.TextField(
        blank=False, null=False,
        db_column='ds_conteudo_mensagem'
    )

    class Meta:
        db_table = 'tb_mensagem_formulario'