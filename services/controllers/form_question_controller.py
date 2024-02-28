from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.views import APIView, Response

from services.models import FormQuestion, FormItem
from services.serializers import FormQuestionSerializer, FormItemSerializer

@dataclass()
class FormQuestionAPIView(APIView):
    def get(self, request):
        form_questions = FormQuestion.objects.all()
        serializer = FormQuestionSerializer(form_questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

@dataclass()
class FormItemAPIView(APIView):
    def get(self, request):
        form_items = FormItem.objects.all()
        serializer = FormItemSerializer(form_items, many=True)
        return Response(serializer.data, status=HTTP_200_OK)