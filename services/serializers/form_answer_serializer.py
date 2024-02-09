from services.helpers.factories import FactorySerializer
from services.models import AnswerForm, MessageForm


class AnswerFormSerializer(FactorySerializer):
    class Meta:
        model = AnswerForm
        fields = '__all__'

class MessageFormSerializer(FactorySerializer):
    class Meta:
        model = MessageForm
        fields = '__all__'