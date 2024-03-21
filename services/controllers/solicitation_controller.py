from dataclasses import dataclass
from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from services.models import Solicitation, AnswerFormQuestion
from services.serializers import SolicitationSerializer, AnswerFormQuestionSerializer

from services.functions.notification_functions import send_notification_solicitation

@dataclass()
class SolicitationModelViewSet(ModelViewSet):
    queryset = Solicitation.objects.all()
    serializer_class = SolicitationSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def list(self, request):
        answer_forms = Solicitation.objects.all()
        serializer = SolicitationSerializer(answer_forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def create(self, request):
        
        data_format = {
            'co_status': 0,
            'co_form': request.data.get('co_form'),
            'co_user': request.data.get('co_user'),
            'nco_answer_form_question': []
        }

        # Criar solicitação sem resposta de formulário
        serializer_solicitation = SolicitationSerializer(data=data_format)
        if serializer_solicitation.is_valid():
            serializer_solicitation.save()
        else:
            return Response(serializer_solicitation.errors, status=HTTP_400_BAD_REQUEST)
        
        # Criar resposta de formulário
        new_answer_form_question_code = []
        for answer_form_question in request.data.get('nco_answer_form_question'):
            curr_answer_form_question = {
                'co_form_question': answer_form_question.get('co_form_question'),
                'nds_answer_question_item': answer_form_question.get('nds_answer_question_item'),
                'nds_answer_question_str': answer_form_question.get('nds_answer_question_str')
            }
            curr_answer_form_question['co_solicitation'] = serializer_solicitation.data.get('co_solicitation')
            serializer_form_question = AnswerFormQuestionSerializer(data=curr_answer_form_question)
            if serializer_form_question.is_valid():
                serializer_form_question.save()
                new_answer_form_question_code.append(serializer_form_question.data.get('co_answer_form_question'))
            else:
                return Response(serializer_form_question.errors, status=HTTP_400_BAD_REQUEST)

        # atualizar solicitação com resposta de formulário
        serializer_solicitation = SolicitationSerializer(
            serializer_solicitation.instance,
            data={'nco_answer_form_question': new_answer_form_question_code},
            partial=True
        )
        if serializer_solicitation.is_valid():
            serializer_solicitation.save()
        else:
            return Response(serializer_solicitation.errors, status=HTTP_400_BAD_REQUEST)
        
        notification_sent = send_notification_solicitation(serializer_solicitation.instance)
        if not notification_sent:
            return Response({'error': 'Erro ao enviar notificação'}, status=HTTP_400_BAD_REQUEST)

        return Response(serializer_solicitation.data, status=HTTP_200_OK)
        

    def partial_update(self, request, pk): # patch
        
        for new_answer_form_question in request.data.get('nco_answer_form_question'):
            old_answer_form_question = AnswerFormQuestion.objects.get(
                co_answer_form_question=new_answer_form_question.get('co_answer_form_question')
            )
            serializer_form_question = AnswerFormQuestionSerializer(
                old_answer_form_question,
                data=new_answer_form_question,
                partial=True
            )
            if serializer_form_question.is_valid():
                serializer_form_question.save()
            else:
                return Response(serializer_form_question.errors, status=HTTP_400_BAD_REQUEST)
        
        curr_solicitation = Solicitation.objects.get(pk=pk)
        notification_sent = send_notification_solicitation(curr_solicitation, 'update')
        if not notification_sent:
            return Response({'error': 'Erro ao enviar notificação'}, status=HTTP_400_BAD_REQUEST)
            
        return Response(serializer_form_question.data, status=HTTP_200_OK)



    
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
    
    @action(detail=False, methods=['GET'])
    def list_questions(self, request):
        answer_questions = AnswerFormQuestion.objects.all()
        serializer = AnswerFormQuestionSerializer(answer_questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
