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
