from rest_framework import routers

from services.controllers import (
    FormQuestionModelViewSet, 
    FormItemModelViewSet, 
    FormModelViewSet, 
    NewsModelViewSet,
    NotificationModelViewSet,
    TutorialModelViewSet,
    SolicitationModelViewSet,
    FormMessageModelViewSet,
)
from services.controllers.form_message_controller import FormMessageModelViewSet

router = routers.DefaultRouter()
router.register('form-question', FormQuestionModelViewSet, basename='FormQuestion')
router.register('form-item', FormItemModelViewSet, basename='FormItem')
router.register('form', FormModelViewSet, basename='Form')
router.register('news', NewsModelViewSet, basename='News')
router.register('notification', NotificationModelViewSet, basename='Notification')
router.register('tutorial', TutorialModelViewSet, basename='Tutorial')
router.register('solicitation', SolicitationModelViewSet, basename='Solicitation')
router.register('form-message', FormMessageModelViewSet, basename='FormMessage')