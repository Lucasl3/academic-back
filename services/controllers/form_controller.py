from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

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
                        "is_required": question.is_required,
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

        data_format = {
            "no_form": request.data.get("no_form"),
            "ds_form": request.data.get("ds_form"),
            "nco_step": [],
            "dt_limit": request.data.get("dt_limit"),
        }

        nco_step_req = request.data.get("nco_step")
        for step in nco_step_req:
            nco_form_question = []
            for question in step.get("nco_form_question"):
                nco_form_item = []
                for item in question.get("nco_form_item"):
                    form_item = FormItem.objects.create(
                        ds_item=item.get("ds_item")
                    )
                    nco_form_item.append(form_item.co_form_item)

                form_question = FormQuestion.objects.create(
                    no_question=question.get("no_question"),
                    ds_question=question.get("ds_question"),
                    co_type_question=question.get("co_type_question"),
                    nco_form_item=nco_form_item,
                    is_required=question.get("is_required"),
                )
                nco_form_question.append(form_question.co_form_question)

            form_step = FormStep.objects.create(
                no_form_step=step.get("no_form_step"),
                ds_form_step=step.get("ds_form_step"),
                nco_form_question=nco_form_question,
            )
            data_format["nco_step"].append(form_step.co_form_step)

        serializer = FormSerializer(data=data_format)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):

        # Implementar função que gerencie a exclusão de um formulário
        # Implementar permissões para exclusão de formulários

        form = Form.objects.get(pk=pk)
        form.hard_delete()
        return Response(status=HTTP_204_NO_CONTENT)