from django.urls import path

from ticket.api.v1.views import (
    InstructorTicketListAPIView,
    InstructorTicketByIDAPIView,
    TicketByIDAPIView,
    TicketListAPIView,
)

app_name = "v1"


urlpatterns = [
    path("ticket/", TicketListAPIView.as_view(), name="ticket_list"),
    path("ticket/<int:ticket_id>/", TicketByIDAPIView.as_view(), name="add_message"),
    path(
        "instructor/ticket/",
        InstructorTicketListAPIView.as_view(),
        name="instructor_ticket_list",
    ),
    path(
        "instructor/ticket/<int:ticket_id>/",
        InstructorTicketByIDAPIView.as_view(),
        name="instructor_add_message",
    ),
]
