from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from services.models import MessageForm
from services.serializers import MessageFormSerializer

from services.functions.solicitation_functions import send_email_add_message

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
    
    def create(self, request):
        serializer = MessageFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_email_add_message(serializer.data['co_message_form'])
        return Response(serializer.data, status=HTTP_200_OK)