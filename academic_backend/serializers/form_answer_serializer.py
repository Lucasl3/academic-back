from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import AnswerForm, MessageForm


class AnswerFormSerializer(FactorySerializer):
    class Meta:
        model = AnswerForm
        fields = '__all__'

class MessageFormSerializer(FactorySerializer):
    class Meta:
        model = MessageForm
        fields = '__all__'