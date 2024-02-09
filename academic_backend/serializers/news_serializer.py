from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import News


class NewsSerializer(FactorySerializer):
    class Meta:
        model = News
        fields = '__all__'
