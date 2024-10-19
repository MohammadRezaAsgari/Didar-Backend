from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from social_django.models import UserSocialAuth

from eventcalendar.api.v1.serializers import (
    GoogleCalendarEventInputSerializer, GoogleCalendarEventSerializer)
from utils.api.error_objects import ErrorObject
from utils.api.mixins import BadRequestSerializerMixin
from utils.api.responses import error_response, success_response
from utils.permissions import IsAuthenticatedAndActive, IsInstructor


class CurrentWeekEventsListAPIView(BadRequestSerializerMixin, ListAPIView):
    permission_classes = [IsAuthenticatedAndActive, IsInstructor]

    @extend_schema(
        request=None,
        parameters=[],
        responses={200: GoogleCalendarEventSerializer},
        auth=None,
        operation_id="EventsList",
        tags=["Event"],
    )
    def get(self, request, *args, **kwargs):
        """
        get an instructor's current week meetings from Google Calender if has logged in with google
        otherwise return GOOGLE_CREDENTIAL_NOT_FOUND

        signup your google acount with requesting to /google-auth/login/google-oauth2/
        """
        user_obj = request.user
        try:
            events_list = user_obj.get_google_calendar_events()
        except UserSocialAuth:
            return error_response(
                error=ErrorObject.GOOGLE_CREDENTIAL_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return error_response(
                error=e.error_object,
                status_code=e.status_code,
            )

        serializer = GoogleCalendarEventSerializer(data=events_list, many=True)
        if not serializer.is_valid():
            return error_response(
                error=ErrorObject.NOT_VALID_EVENTS_ERROR,
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return success_response(data=serializer.data, status_code=status.HTTP_200_OK)

    @extend_schema(
        request=GoogleCalendarEventInputSerializer,
        parameters=[],
        responses={200: GoogleCalendarEventSerializer},
        auth=None,
        operation_id="EventCreation",
        tags=["Event"],
    )
    def post(self, request, *args, **kwargs):
        serializer = GoogleCalendarEventInputSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                error=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = request.user
        try:
            created_event = user_obj.create_google_calendar_event(
                summary=serializer.validated_data.get("summary"),
                start=serializer.validated_data.get("start").get("dateTime"),
                end=serializer.validated_data.get("end").get("dateTime"),
                attendees_emails=serializer.validated_data.get("attendees_emails", []),
                time_zone=serializer.validated_data.get("start").get("timeZone"),
            )
        except Exception as e:
            return error_response(
                error=e.error_object,
                status_code=e.status_code,
            )

        output = GoogleCalendarEventSerializer(created_event)
        return success_response(data=output.data, status_code=status.HTTP_200_OK)
