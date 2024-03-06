from django.urls import path

from services.controllers import TutorialAPIView

# Definir rotas de acordo com o front-end
urlpatterns = [
    path('tutorial/', TutorialAPIView.as_view()),
]