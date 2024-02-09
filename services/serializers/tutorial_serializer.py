from services.helpers.factories import FactorySerializer
from services.models import Tutorial


class TutorialSerializer(FactorySerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'
