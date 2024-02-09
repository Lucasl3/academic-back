from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import FormQuestion, FormItem


class FormQuestionSerializer(FactorySerializer):
    class Meta:
        model = FormQuestion
        fields = '__all__'

class FormItemSerializer(FactorySerializer):
    class Meta:
        model = FormItem
        fields = '__all__'