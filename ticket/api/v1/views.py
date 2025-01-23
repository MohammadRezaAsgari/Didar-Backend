from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from ticket.api.v1.serializers import (
    InputTicketMessageSerializer,
    InputTicketSerializer,
    InstructorInputUpdateTicketSerializer,
    InstructorInputTicketMessageSerializer,
    InstructorOutputTicketDetailSerializer,
    InstructorOutputTicketListSerializer,
    OutputTicketDetailSerializer,
    OutputTicketListSerializer,
)
from ticket.models import Ticket
from utils.api.error_objects import ErrorObject
from utils.api.mixins import BadRequestSerializerMixin
from utils.api.responses import error_response, success_response
from utils.permissions import IsInstructor, IsAuthenticatedAndActive


class TicketListAPIView(BadRequestSerializerMixin, ListAPIView):
    """
    Get List of Tickets.

    Status = `1:PENDING` , `2:ANSWERED`, `3:CLOSED`
    """

    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = OutputTicketListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "status",
    ]
    ordering_fields = [
        "created",
    ]
    ordering = ["-created"]

    def get_queryset(self):
        qs = self.request.user.tickets.all()
        return qs

    @extend_schema(
        request=None,
        responses={200: OutputTicketListSerializer},
        auth=None,
        operation_id="AllTickets",
        tags=["Tickets"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=InputTicketSerializer,
        responses={201: {}},
        auth=None,
        operation_id="CreateTicket",
        tags=["Tickets"],
    )
    def post(self, request):
        """
        Create new ticket.
        """
        serializer = InputTicketSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)
        serializer.save()
        return success_response(data=None, status_code=status.HTTP_201_CREATED)


class TicketByIDAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsAuthenticatedAndActive]

    def get_object(self):
        return self.request.user.tickets.get(id=self.kwargs.get("ticket_id"))

    @extend_schema(
        request=None,
        responses={200: OutputTicketDetailSerializer},
        auth=None,
        operation_id="TicketByID",
        tags=["Tickets"],
    )
    def get(self, request, *args, **kwargs):
        """
        Status = `1:PENDING` , `2:ANSWERED`, `3:CLOSED`
        """
        try:
            ticket = self.get_object()
        except Ticket.DoesNotExist:
            return error_response(
                error=ErrorObject.TICKET_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = OutputTicketDetailSerializer(ticket, context={"request": request})
        return success_response(data=serializer.data, status_code=status.HTTP_200_OK)

    @extend_schema(
        request=InputTicketMessageSerializer,
        responses={201: {}},
        auth=None,
        operation_id="CreateMessage",
        tags=["Tickets"],
    )
    def post(self, request, *args, **kwargs):
        """
        Create new message.
        """
        try:
            ticket = self.get_object()
        except Ticket.DoesNotExist:
            return error_response(
                error=ErrorObject.TICKET_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = InputTicketMessageSerializer(
            data=request.data, context={"request": request, "ticket": ticket}
        )
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)

        serializer.save()
        return success_response(data=None, status_code=status.HTTP_201_CREATED)


class InstructorTicketListAPIView(BadRequestSerializerMixin, ListAPIView):
    """
    Get list of all tickets for Instructor with filtering on status

    Status = `1:PENDING` , `2:ANSWERED`, `3:CLOSED`
    """

    permission_classes = [IsInstructor]
    serializer_class = InstructorOutputTicketListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "status",
    ]
    ordering_fields = [
        "created",
    ]
    ordering = ["-created"]

    def get_queryset(self):
        qs = self.request.user.instructor.tickets.all()
        return qs

    @extend_schema(
        request=None,
        responses={200: InstructorOutputTicketListSerializer},
        auth=None,
        operation_id="InstructorAllTickets",
        tags=["Tickets"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class InstructorTicketByIDAPIView(BadRequestSerializerMixin, APIView):
    permission_classes = [IsInstructor]

    def get_object(self):
        qs = self.request.user.instructor.tickets.get(id=self.kwargs.get("ticket_id"))
        return qs

    @extend_schema(
        request=None,
        responses={200: InstructorOutputTicketDetailSerializer},
        auth=None,
        operation_id="InstructorTicketByID",
        tags=["Tickets"],
    )
    def get(self, request, *args, **kwargs):
        """
        Getting ticket information by ID for the Instructor

        Status = `1:PENDING` , `2:ANSWERED`, `3:CLOSED`
        """
        try:
            ticket = self.get_object()
        except Ticket.DoesNotExist:
            return error_response(
                error=ErrorObject.TICKET_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = InstructorOutputTicketDetailSerializer(
            ticket, context={"request": request}
        )

        return success_response(data=serializer.data, status_code=status.HTTP_200_OK)

    @extend_schema(
        request=InstructorInputTicketMessageSerializer,
        responses={201: {}},
        auth=None,
        operation_id="InstructorCreateMessage",
        tags=["Tickets"],
    )
    def post(self, request, *args, **kwargs):
        """
        Sending a message by the Instructor to answer the user's ticket

        """
        try:
            ticket = self.get_object()
        except Ticket.DoesNotExist:
            return error_response(
                error=ErrorObject.TICKET_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = InstructorInputTicketMessageSerializer(
            data=request.data, context={"request": request, "ticket": ticket}
        )
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)

        serializer.save()
        return success_response(data=None, status_code=status.HTTP_201_CREATED)

    @extend_schema(
        request=InstructorInputUpdateTicketSerializer,
        responses={200: {}},
        auth=None,
        operation_id="InstructorUpdateTicketStatus",
        tags=["Tickets"],
    )
    def patch(self, request, *args, **kwargs):
        """
        Update the ticket by instructor

        Status = `1:PENDING` , `2:ANSWERED`, `3:CLOSED`
        """
        try:
            ticket_obj = self.get_object()
        except Ticket.DoesNotExist:
            return error_response(
                error=ErrorObject.TICKET_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = InstructorInputUpdateTicketSerializer(
            ticket_obj, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return self.serializer_error_response(serializer)
        serializer.save()

        return success_response(data=None, status_code=status.HTTP_204_NO_CONTENT)
