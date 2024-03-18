from services.helpers.factories import FactorySerializer
from services.models import Solicitation, MessageForm


class SolicitationSerializer(FactorySerializer):
    class Meta:
        model = Solicitation
        fields = '__all__'

class MessageFormSerializer(FactorySerializer):
    class Meta:
        model = MessageForm
        fields = '__all__'