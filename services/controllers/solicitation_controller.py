from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from services.models import Solicitation
from services.serializers import SolicitationSerializer


@dataclass()
class SolicitationModelViewSet(ModelViewSet):
    queryset = Solicitation.objects.all()
    serializer_class = SolicitationSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def get(self, request):
        answer_forms = Solicitation.objects.all()
        serializer = SolicitationSerializer(answer_forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
        # Implementar função que gerencie a criação de uma resposta de formulário
        # Implementar permissões para criação da resposta de formulário
 
        serializer = SolicitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):

        # Implementar função que gerencie a atualização de uma resposta de formulário
        # Implementar permissões para atualização da resposta de formulário

        answer_form = Solicitation.objects.get(pk=pk)
        serializer = SolicitationSerializer(answer_form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        # Implementar função que gerencie a exclusão de uma resposta de formulário
        # Implementar permissões para exclusão da resposta de formulário

        answer_form = Solicitation.objects.get(pk=pk)
        answer_form.delete()
        return Response(status=HTTP_204_NO_CONTENT)
