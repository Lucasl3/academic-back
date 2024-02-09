from services.helpers.factories import FactorySerializer
from services.models import Form


class FormSerializer(FactorySerializer):
    class Meta:
        model = Form
        fields = '__all__'
