from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import Tutorial


class TutorialSerializer(FactorySerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'
