from django.urls import include, path

app_name = "eventcalendar"

urlpatterns = [
    path("v1/", include("eventcalendar.api.v1.urls", namespace="v1")),
]
