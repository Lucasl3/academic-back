from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from services.models import User
from services.serializers import UserSerializer

@dataclass()
class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def get(self, request):
        forms = User.objects.all()
        
        name_or_email = self.request.query_params.get('search', '')

        forms = forms.filter(
            Q(no_user__icontains=name_or_email) | Q(ds_email__icontains=name_or_email)
        )
        
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