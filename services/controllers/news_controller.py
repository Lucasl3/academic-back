from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from services.models import News
from services.serializers import NewsSerializer

@dataclass()
class NewsModelViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def list(self, request):
        forms = News.objects.all()
        serializer = NewsSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def create(self, request):
        
        # Implementar função que gerencie a criação de um news
        # Implementar permissões para criação de news
 
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):

        form = News.objects.get(pk=pk)
        serializer = NewsSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):

        pk = request.data.get('co_news')

        # Implementar função que gerencie a exclusão de um news
        # Implementar permissões para exclusão de news

        form = News.objects.get(pk=pk)
        form.hard_delete()

        return Response(NewsSerializer(form).data, status=HTTP_200_OK)