from app.common.exceptions import JSONException


class InvalidFormatException(JSONException):
    status_code = 500
    message = "Invalid format given please chose between 'old' or 'new'"


class InvalidSideException(JSONException):
    status_code = 500
    message = "Side name is invalid please use front or back"


class NotClearImage(JSONException):
    status_code = 404
    message = "Image is not clear"
