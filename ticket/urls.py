from django.urls import include, path

app_name = "ticket"

urlpatterns = [
    path("v1/", include("ticket.api.v1.urls", namespace="v1")),
]
