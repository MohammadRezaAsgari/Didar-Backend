from django.urls import path

from eventcalendar.api.v1.views import InstructorEventsListAPIView

app_name = "v1"

urlpatterns = [
    path(
        "instructor/events/",
        InstructorEventsListAPIView.as_view(),
        name="instructor_events_list",
    ),
]
