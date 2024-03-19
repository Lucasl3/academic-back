from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from services.models import MessageForm
from services.serializers import MessageFormSerializer

@dataclass()
class FormMessageModelViewSet(ModelViewSet):
    queryset = MessageForm.objects.all()
    serializer_class = MessageFormSerializer

    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def list(self, request):
        form_questions = MessageForm.objects.all()
        serializer = MessageFormSerializer(form_questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def algumacoisa(self, request):
        return Response('alguma coisa', status=HTTP_200_OK)