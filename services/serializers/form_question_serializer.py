from services.helpers.factories import FactorySerializer
from services.models import FormQuestion, FormItem, FormStep


class FormStepSerializer(FactorySerializer):
    class Meta:
        model = FormStep
        fields = '__all__'

class FormQuestionSerializer(FactorySerializer):
    class Meta:
        model = FormQuestion
        fields = '__all__'

class FormItemSerializer(FactorySerializer):
    class Meta:
        model = FormItem
        fields = '__all__'