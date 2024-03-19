from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from services.models import FormQuestion, FormItem
from services.serializers import FormQuestionSerializer, FormItemSerializer

@dataclass()
class FormQuestionModelViewSet(ModelViewSet):
    queryset = FormQuestion.objects.all()
    serializer_class = FormQuestionSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)
        
    def get(self, request):
        form_questions = FormQuestion.objects.all()
        serializer = FormQuestionSerializer(form_questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

@dataclass()
class FormItemModelViewSet(ModelViewSet):
    queryset = FormItem.objects.all()
    serializer_class = FormItemSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)
        
    def get(self, request):
        form_items = FormItem.objects.all()
        serializer = FormItemSerializer(form_items, many=True)
        return Response(serializer.data, status=HTTP_200_OK)