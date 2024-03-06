from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import APIView, Response

from services.models import Tutorial
from services.serializers import TutorialSerializer

@dataclass()
class TutorialAPIView(APIView):

    def get(self, request):
        forms = Tutorial.objects.all()
        serializer = TutorialSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
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