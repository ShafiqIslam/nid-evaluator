from app.common.exceptions import JSONException


class InvalidFormatException(JSONException):
    status_code = 500
    message = "Invalid format given please chose between 'old' or 'new'"


class FormatNotExcepted(JSONException):
    status_code = 500
    message = "Invalid format given for image"
