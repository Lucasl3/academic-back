from rest_framework import serializers


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['dt_created_at', 'dt_updated_at', 'dt_deleted_at', 'is_deleted']
