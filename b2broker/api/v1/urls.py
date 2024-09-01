from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("schema/", include("b2broker.api.v1.schema.urls")),
    path("misc/", include("b2broker.api.v1.misc.urls")),
]
