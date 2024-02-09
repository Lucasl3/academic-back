from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import Notification


class NotificationSerializer(FactorySerializer):
    class Meta:
        model = Notification
        fields = '__all__'
