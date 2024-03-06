from django.urls import path

from services.controllers import NotificationAPIView

# Definir rotas de acordo com o front-end
urlpatterns = [
    path('notification/', NotificationAPIView.as_view()),
]