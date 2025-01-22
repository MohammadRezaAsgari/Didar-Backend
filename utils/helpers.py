import string
import secrets
import hashlib

from django.conf import settings
from pytz import UnknownTimeZoneError, timezone as pytz_timezone

from utils.validators import CustomValidationError
from utils.api.error_objects import ErrorObject


def convert_datetime_timezone(datetime, timezone):
    """
    This method get a timezone and convert datetime to that timezone.
    """
    try:
        timezone = pytz_timezone(timezone)
    except UnknownTimeZoneError:
        raise CustomValidationError(
            f"{timezone} timezone is not valid!",
            field="timezone",
            error_object=ErrorObject.BAD_REQUEST,
        )
    return str(datetime.astimezone(timezone).isoformat())


def get_hash(value: str) -> str:
    salt = settings.SECRET_KEY
    hashed_value = hashlib.sha1((value + salt).encode()).hexdigest()
    return hashed_value


def create_random_digits(length: int = 10) -> str:
    return "".join(secrets.choice(string.digits) for i in range(length))
