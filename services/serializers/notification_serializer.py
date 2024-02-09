from services.helpers.factories import FactorySerializer
from services.models import Notification


class NotificationSerializer(FactorySerializer):
    class Meta:
        model = Notification
        fields = '__all__'
