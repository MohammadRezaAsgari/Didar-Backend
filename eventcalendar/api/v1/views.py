from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from eventcalendar.api.v1.serializers import GoogleCalendarEventSerializer
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
        except Exception as e:
            return error_response(
                error=ErrorObject.GOOGLE_CREDENTIAL_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = GoogleCalendarEventSerializer(data=events_list, many=True)
        print(serializer.initial_data)
        if not serializer.is_valid():
            print(serializer.errors)
            return error_response(
                error=ErrorObject.NOT_VALID_EVENTS_ERROR,
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return success_response(data=serializer.data, status_code=status.HTTP_200_OK)
