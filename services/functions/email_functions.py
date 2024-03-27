
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from services.models import (
    Solicitation,
    MessageForm,
    Form
)

def send_email(subject, text, user_email):
    msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [user_email])

    msg.attach_alternative(text, 'text/html')
    msg.content_subtype = 'html'

    msg.mixed_subtype = 'related'
    msg.send()
    

def send_email_add_message(message_id):
    message = MessageForm.objects.get(
        co_message_form=message_id
    )
    solicitation = message.co_solicitation
    message_text = message.ds_message
    user_email = solicitation.co_user.ds_email
    formated_data = ''
    if solicitation.dt_created_at is not None:
        formated_data = solicitation.dt_created_at.strftime('%d/%m/%Y')

    email_subject = 'Sua solicitação possui uma nova mensagem'
    email_text = f'''

        Sua solicitação feita na data {formated_data} teve uma nova atualização:

        Uma nova mensagem foi adicionada:
        '{message_text}'

    '''
    try:
        send_email(email_subject, email_text, user_email)
        return True
    except:
        return False
    

def send_email_new_status(solicitation_id):
    solicitation = Solicitation.objects.get(
        pk=solicitation_id
    )
    user_email = solicitation.co_user.ds_email
    formated_data = solicitation.dt_created_at.strftime('%d/%m/%Y')

    status = [
        "Recebimento",
        "Análise",
        "Em aprovação",
        "Concluído"
      ]

    curr_status = status[solicitation.co_status]

    email_subject = 'Sua solicitação teve uma atualização de status'
    email_text = f'''

        Sua solicitação feita na data {formated_data} teve uma atualização de status:
        O status atual é: {curr_status}

    '''
    try:
        send_email(email_subject, email_text, user_email)
        return True
    except:
        return False