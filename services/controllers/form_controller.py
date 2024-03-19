from dataclasses import dataclass

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from services.models import Form, FormQuestion, FormItem
from services.serializers import FormSerializer

@dataclass()
class FormModelViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    
    def __init__(self, *args, **kwargs):
        self.suffix = kwargs.pop('suffix', None)
        super().__init__(*args, **kwargs)

    def get(self, request, co_form=None):

        if co_form:
            form = Form.objects.get(
                co_form=co_form
            )
            serializer = FormSerializer(form)

            questions = []
            for question_id in form.nco_question:
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

            result = serializer.data
            result['nco_question'] = questions

            return Response(result, status=HTTP_200_OK)

        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        
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