from academic_backend.helpers.factories import FactorySerializer
from academic_backend.models import User


class UserSerializer(FactorySerializer):
    class Meta:
        model = User
        fields = '__all__'
