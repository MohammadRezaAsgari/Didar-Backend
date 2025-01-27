from datetime import timedelta

from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.loggers import stdout_logger
from users.models import Instructor


@shared_task
def check_instructors_meetings():
    instructor_objs = Instructor.objects.all()

    for instructor in instructor_objs:
        user = instructor.user
        try:
            social_user = user.social_auth.filter(provider="google-oauth2").last()

            credentials = Credentials(
                token=social_user.extra_data["access_token"],
                refresh_token=social_user.extra_data["refresh_token"],
                client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                token_uri="https://oauth2.googleapis.com/token",
            )

            # Build Google Calendar API client
            service = build("calendar", "v3", credentials=credentials)

            now = datetime.utcnow()
            one_hours_later = now + timedelta(hours=1)
            time_min = now.isoformat() + "Z"
            time_max = one_hours_later.isoformat() + "Z"

            stdout_logger.info(f"Geting {user.username} events from google calender...")
            try:
                events_result = (
                    service.events()
                    .list(
                        calendarId="primary",
                        timeMin=time_min,  # From now (to exclude past events)
                        timeMax=time_max,  # Until 1 hour from now
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
            except HttpError as error:
                # Catch the HttpError
                error_details = error.content.decode("utf-8")
                stdout_logger.error(f"Get f{user.username} faild.{error_details}")

            events = events_result.get("items", [])
            if len(events) > 0 and instructor.is_available_now:
                instructor.is_available_now = False
                instructor.save()

        except Exception:
            stdout_logger.error(f"Cred for f{user.username} not available!")
            continue
