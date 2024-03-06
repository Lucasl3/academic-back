from django.urls import path

from services.controllers import NewsAPIView

# Definir rotas de acordo com o front-end
urlpatterns = [
    path('news/', NewsAPIView.as_view()),
]