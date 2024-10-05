from django.urls import path

from schedule.api.v1.views import (
    InstructorScheduleListAPIView,
    InstructorScheduleByIdAPIView,
    ScheduleByInstructorAPIView,
)

app_name = 'v1'

urlpatterns = [
    path("instructor/schedules/", InstructorScheduleListAPIView.as_view(), name="instructor_schedule_list"),
    path("instructor/schedules/<str:schedule_code>/", InstructorScheduleByIdAPIView.as_view(), name="instructor_schedule"),
    path("instructor/<int:instructor_id>/schedules/", ScheduleByInstructorAPIView.as_view(), name="schedule"),
]
