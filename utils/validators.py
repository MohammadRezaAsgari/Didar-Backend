from rest_framework.exceptions import ValidationError
from rest_framework import status

from utils.api.error_objects import ErrorObject


class CustomValidationError(ValidationError):
    def __init__(self, detail, field=None, error_object=None, status_code=status.HTTP_400_BAD_REQUEST):
        # detail is the error message
        # field is the name of the field which caused the error (optional)
        # status_code is the HTTP status code for this error
        if field:
            self.detail = {field: [detail]}
        else:
            self.detail = detail
        self.error_object = error_object or ErrorObject.BAD_REQUEST
        self.status_code = status_code
