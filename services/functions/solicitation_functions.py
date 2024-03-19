
from decouple import config
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from services.models import (
    Solicitation,
    MessageForm,
)

def send_email_add_message(message_id):
    message = MessageForm.objects.get(
        co_message_form=message_id
    )
    solicitation = message.solicitation
    message_text = message.ds_message
    user_email = solicitation.user.ds_email
    formated_data = solicitation.dt_created_at.strftime('%d/%m/%Y')

    email_subject = 'Sua solicitação possui uma nova mensagem'
    email_text = f'''

        Sua solicitação feita na data {formated_data} teve uma nova atualização:

        Uma nova mensagem foi adicionada:
        '{message_text}'

    '''
    msg = EmailMultiAlternatives(email_subject, '', config('EMAIL_ADDRESS'), user_email)

    msg.attach_alternative(email_text, 'text/html')
    msg.content_subtype = 'html'

    # msg.mixed_subtype = 'related'
    msg.send()

    print(f'Email sent to {solicitation.user.email} with success!')

