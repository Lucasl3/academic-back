from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import APIView, Response

from services.models import User
from services.serializers import UserSerializer

@dataclass()
class UserAPIView(APIView):

    def get(self, request):
        forms = User.objects.all()
        serializer = UserSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
        # Implementar função que gerencie a criação de um user
        # Implementar permissões para criação de users
 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request):

        co_user = request.data.get('co_user')
        if not co_user:
            return Response(status=HTTP_400_BAD_REQUEST)

        form = User.objects.get(pk=co_user)
        serializer = UserSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):

        pk = request.data.get('co_user')

        # Implementar função que gerencie a exclusão de um user
        # Implementar permissões para exclusão de users

        form = User.objects.get(pk=pk)
        form.delete()

        return Response(UserSerializer(form).data, status=HTTP_200_OK)