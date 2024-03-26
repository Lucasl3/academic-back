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

from services.models import Solicitation, AnswerFormQuestion, Form, FormQuestion, MessageForm, FormItem, User
from services.serializers import SolicitationSerializer, AnswerFormQuestionSerializer, FormQuestionSerializer

from services.functions.notification_functions import send_notification_solicitation
from services.functions.email_functions import send_email_new_status

@dataclass()
class SolicitationModelViewSet(ModelViewSet):
    queryset = Solicitation.objects.all()
    serializer_class = SolicitationSerializer
    # print("aqui")
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def list(self, request):
        answer_forms = Solicitation.objects.all()
        serializer = SolicitationSerializer(answer_forms, many=True)
        print(serializer.data)
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
    
    def update(self, request, pk):

        # Implementar função que gerencie a atualização de uma resposta de formulário
        # Implementar permissões para atualização da resposta de formulário

        answer_form = Solicitation.objects.get(pk=pk)
        serializer = SolicitationSerializer(answer_form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # Implementar função que gerencie a exclusão de uma resposta de formulário
        # Implementar permissões para exclusão da resposta de formulário

        answer_form = Solicitation.objects.get(pk=pk)
        answer_form.hard_delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'])
    def list_questions(self, request):
        answer_questions = AnswerFormQuestion.objects.all()
        serializer = AnswerFormQuestionSerializer(answer_questions, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def update_status(self, request):
        co_solicitation = request.data.get('co_solicitation')
        new_status = request.data.get('co_status')

        solicitation = Solicitation.objects.get(pk=co_solicitation)
        form = Form.objects.get(pk=solicitation.co_form.co_form)
        num_of_status = len(form.nco_status)
        if new_status < 0 or new_status > num_of_status-1:
            return Response({'error': 'Status inválido'}, status=HTTP_400_BAD_REQUEST)

        solicitation.co_status = new_status
        solicitation.save()

        notification_sent = send_email_new_status(co_solicitation)
        if not notification_sent:
            return Response({'error': 'Erro ao enviar notificação'}, status=HTTP_400_BAD_REQUEST)
        
        solicitation = SolicitationSerializer(solicitation).data
        return Response(solicitation, status=HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def list_by_user(self, request):
        co_user = request.query_params.get("co_user")
        solicitation = Solicitation.objects.filter(co_user=co_user)
        serializer = SolicitationSerializer(solicitation, many=True)
        return Response(serializer.data, status=HTTP_200_OK)    
    
    def retrieve(self, request, pk=None):
        solicitation = Solicitation.objects.get(
            co_solicitation = pk
        )
        serializer = SolicitationSerializer(solicitation)

        form = Form.objects.get(
            co_form=serializer.data['co_form']
        )

        status = []
        for i, status_code in enumerate(form.nco_status):
            messages = MessageForm.objects.filter(
                co_solicitation=pk,
                co_status=i,
                is_deleted=False
            )
            
            message_status = []
            for message in messages:
                message_status.append({
                    'ds_message_form': message.ds_message,
                    'dt_updated_at': message.dt_updated_at,
                })
                
            status.append({
                'ds_status': status_code,
                'messages': message_status,
                'done': True if i < serializer.data['co_status'] else False
            })
        
        questions = []
        for question_id in solicitation.nco_answer_form_question:
            question_answer = AnswerFormQuestion.objects.get(
                co_answer_form_question=question_id
            )
            question_answer = AnswerFormQuestionSerializer(question_answer).data
            
            question = FormQuestion.objects.get(
                co_form_question=question_answer['co_form_question']
            )
            question = FormQuestionSerializer(question).data
            
            if question['co_type_question'] == 'text' or question['co_type_question'] == 'file':
                answer = question_answer['nds_answer_question_str']
            else:
                options = question_answer['nds_answer_question_item']
                answer = [FormItem.objects.get(co_form_item=item).ds_item for item in options]
            
            questions.append({
                'co_form_question': question['co_form_question'],
                'no_question': question['no_question'],
                'ds_question': question['ds_question'],
                'co_type_question': question['co_type_question'],
                'answer': answer,
            })
        
        user_id = serializer.data['co_user']
        user = User.objects.get(co_user=user_id)

        result = serializer.data
        result['status'] = status
        result['title'] = form.no_form
        result['description'] = form.ds_form
        result['questions'] = questions
        result['user_name'] = user.no_user
        
        return Response(result, status=HTTP_200_OK)