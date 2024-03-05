from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView, Response

from services.models import Notification
from services.serializers import NotificationSerializer

@dataclass()
class NotificationAPIView(APIView):

    def get(self, request):
        forms = Notification.objects.all()
        serializer = NotificationSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
        # Implementar função que gerencie a criação de um notification
        # Implementar permissões para criação de notification
 
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request):

        co_notification = request.data.get('co_notification')
        if not co_notification:
            return Response(status=HTTP_400_BAD_REQUEST)

        form = Notification.objects.get(pk=co_notification)
        serializer = NotificationSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):

        pk = request.data.get('co_notification')

        # Implementar função que gerencie a exclusão de um notification
        # Implementar permissões para exclusão de notification

        form = Notification.objects.get(pk=pk)
        form.delete()

        return Response(NotificationSerializer(form).data, status=HTTP_200_OK)