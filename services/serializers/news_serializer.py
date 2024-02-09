from services.helpers.factories import FactorySerializer
from services.models import News


class NewsSerializer(FactorySerializer):
    class Meta:
        model = News
        fields = '__all__'
