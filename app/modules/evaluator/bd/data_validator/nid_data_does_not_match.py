from app.common.exceptions import JSONException


class NIDDataDoesNotMatch(JSONException):
    status_code = 404
    message = "NID data seems to be incorrect."
