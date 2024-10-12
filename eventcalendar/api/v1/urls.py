from django.urls import path

from users.api.v1.views import (CurrentWeekEventsListAPIView, )

app_name = "v1"

urlpatterns = [
    path(
        "instructor/events/",
        CurrentWeekEventsListAPIView.as_view(),
        name="instructor_events_list",
    ),
]
