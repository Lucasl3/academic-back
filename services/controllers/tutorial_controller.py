from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from services.models import Tutorial
from services.serializers import TutorialSerializer

@dataclass()
class TutorialModelViewSet(ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def list(self, request, co_tutorial=None):
        if co_tutorial is not None:
            form = Tutorial.objects.get(pk=co_tutorial)
            serializer = TutorialSerializer(form)
            return Response(serializer.data, status=HTTP_200_OK)
        
        forms = Tutorial.objects.all()
        serializer = TutorialSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        item = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    
    def create(self, request):
        
        # Implementar função que gerencie a criação de um tutorial
        # Implementar permissões para criação de tutoriais
 
        serializer = TutorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request):

        co_tutorial = request.data.get('co_tutorial')
        if not co_tutorial:
            return Response(status=HTTP_400_BAD_REQUEST)

        form = Tutorial.objects.get(pk=co_tutorial)
        serializer = TutorialSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):

        pk = request.data.get('co_tutorial')

        # Implementar função que gerencie a exclusão de um tutorial
        # Implementar permissões para exclusão de tutoriais

        form = Tutorial.objects.get(pk=pk)
        form.delete()

        return Response(TutorialSerializer(form).data, status=HTTP_200_OK)