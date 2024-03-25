from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from services.models import Form, FormQuestion, FormItem, FormStep
from services.serializers import FormSerializer

@dataclass()
class FormModelViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def list(self, request, co_form=None):

        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()

        form = Form.objects.get(
            co_form=pk
        )
        serializer = FormSerializer(form)

        steps = []
        for step_id in form.nco_step:
            step = FormStep.objects.get(
                co_form_step=step_id
            )
            
            questions = []
            for question_id in step.nco_form_question:
                question = FormQuestion.objects.get(
                    co_form_question=question_id
                )

                items = []
                for item_id in question.nco_form_item:
                    item = FormItem.objects.get(co_form_item=item_id)
                    items.append(
                        {
                            "co_form_item": item.co_form_item,
                            "ds_item": item.ds_item,
                        }
                    )

                questions.append(
                    {
                        "co_form_question": question.co_form_question,
                        "no_question": question.no_question,
                        "ds_question": question.ds_question,
                        "co_type_question": question.co_type_question,
                        "nco_form_item": items,
                    }
                )
        
            steps.append(
                {
                    "co_form_step": step.co_form_step,
                    "no_form_step": step.no_form_step,
                    "ds_form_step": step.ds_form_step,
                    "nco_form_question": questions,
                }
            )

        result = serializer.data
        result["nco_step"] = steps

        return Response(result, status=HTTP_200_OK)

    
    def create(self, request):
        
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