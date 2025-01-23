from django.urls import path

from ticket.api.v1.views import (
    InstructorTicketListAPIView,
    InstructorTicketByIDAPIView,
    TicketByIDAPIView,
    TicketListAPIView,
)

app_name = "v1"


urlpatterns = [
    path("tickets/", TicketListAPIView.as_view(), name="ticket_list"),
    path("tickets/<int:ticket_id>/", TicketByIDAPIView.as_view(), name="add_message"),
    path(
        "instructor/tickets/",
        InstructorTicketListAPIView.as_view(),
        name="instructor_ticket_list",
    ),
    path(
        "instructor/tickets/<int:ticket_id>/",
        InstructorTicketByIDAPIView.as_view(),
        name="instructor_add_message",
    ),
]
