from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import Form


class FormSerializer(FactorySerializer):
    class Meta:
        model = Form
        fields = '__all__'
