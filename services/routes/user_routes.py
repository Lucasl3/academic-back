from django.urls import path

from services.controllers import UserAPIView

# Definir rotas de acordo com o front-end
urlpatterns = [
    path('user/', UserAPIView.as_view()),
]