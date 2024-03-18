from django.urls import path

from services.controllers import (
    FormQuestionAPIView, 
    FormItemAPIView, 
    FormAPIView, 
    SolicitationAPIView
    )

# Definir rotas de acordo com o front-end
urlpatterns = [
    path('form-question/', FormQuestionAPIView.as_view()),
    path('form-item/', FormItemAPIView.as_view()),
    path('form/', FormAPIView.as_view()),
    path('form/<int:co_form>/', FormAPIView.as_view()),
    path('solicitation/', SolicitationAPIView.as_view()),
]