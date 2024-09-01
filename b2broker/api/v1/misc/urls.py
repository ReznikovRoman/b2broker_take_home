from django.urls import path

from .views import Healthcheck

urlpatterns = [
    path("healthcheck", Healthcheck.as_view(), name="healthcheck"),
]
