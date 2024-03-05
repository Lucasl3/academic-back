from .form_routes import urlpatterns as form_routes
from .tutorial_routes import urlpatterns as tutorial_routes
from .news_routes import urlpatterns as news_routes

urlpatterns = [
    *form_routes,
    *tutorial_routes,
    *news_routes,
]