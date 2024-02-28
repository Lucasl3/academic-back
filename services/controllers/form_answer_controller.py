from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import APIView, Response

from services.models import AnswerForm
from services.serializers import AnswerFormSerializer


@dataclass()
class AnswerFormAPIView(APIView):
    def get(self, request):
        answer_forms = AnswerForm.objects.all()
        serializer = AnswerFormSerializer(answer_forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
        # Implementar função que gerencie a criação de uma resposta de formulário
        # Implementar permissões para criação da resposta de formulário
 
        serializer = AnswerFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):

        # Implementar função que gerencie a atualização de uma resposta de formulário
        # Implementar permissões para atualização da resposta de formulário

        answer_form = AnswerForm.objects.get(pk=pk)
        serializer = AnswerFormSerializer(answer_form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        # Implementar função que gerencie a exclusão de uma resposta de formulário
        # Implementar permissões para exclusão da resposta de formulário

        answer_form = AnswerForm.objects.get(pk=pk)
        answer_form.delete()
        return Response(status=HTTP_204_NO_CONTENT)
