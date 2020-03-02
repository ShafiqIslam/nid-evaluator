from app.common.exceptions import JSONException


class UnableToClassifyAsNID(JSONException):
    status_code = 404
    message = "Unable to classify as nid."
