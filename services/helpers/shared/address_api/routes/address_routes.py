from django.urls import path

from services.helpers.shared.address_api.controllers.user_address_controller import (
    CityAPIView,
    CountryAPIView,
    PostalCodeAPIView,
    UfAPIView,
)

urlpatterns = [
    path('countries', CountryAPIView.as_view()),
    path('ufs', UfAPIView.as_view()),
    path('cities', CityAPIView.as_view()),
    path('postalcode', PostalCodeAPIView.as_view()),
]
