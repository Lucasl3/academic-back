from services.helpers.factories import FactorySerializer
from services.models import User


class UserSerializer(FactorySerializer):
    class Meta:
        model = User
        fields = '__all__'
