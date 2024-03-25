
from services.models import (
    Solicitation,
    User,
    Notification,
    Form
)

from services.serializers import (
    SolicitationSerializer,
    NotificationSerializer
)


def send_notification_solicitation(solicitation_instance, action='create'):

    users_secretaria = User.objects.filter(co_profile=1).values_list('co_user', flat=True)
    user_student_name = solicitation_instance.co_user.no_user
    form_title = solicitation_instance.co_form.no_form
    
    if action == 'create':
        descricao = f'Nova solicitação de {user_student_name} no formulário {form_title}'
    elif action == 'update':
        descricao = f'Solicitação de {user_student_name} no formulário {form_title} teve uma nova alteração'


    notification_data = {
        'ds_notification': descricao,
        'co_status': 0,
        'nco_user': list(users_secretaria)
    }
    serializer_notification = NotificationSerializer(data=notification_data)
    if serializer_notification.is_valid():
        serializer_notification.save()
    else:
        return False
    
    return True