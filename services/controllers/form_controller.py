from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import APIView, Response

from services.models import Form
from services.serializers import FormSerializer

@dataclass()
class FormAPIView(APIView):
    def get(self, request):
        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
        # Implementar função que gerencie a criação de um formulário
        # Implementar permissões para criação de formulários
 
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):

        # Implementar função que gerencie a atualização de um formulário
        # Implementar permissões para atualização de formulários

        form = Form.objects.get(pk=pk)
        serializer = FormSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        # Implementar função que gerencie a exclusão de um formulário
        # Implementar permissões para exclusão de formulários

        form = Form.objects.get(pk=pk)
        form.delete()
        return Response(status=HTTP_204_NO_CONTENT)