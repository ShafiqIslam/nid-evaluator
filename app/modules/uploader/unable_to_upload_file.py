from app.common.exceptions import JSONException


class UnableToUploadFile(JSONException):
    status_code = 500
    message = "Could not upload file."

    def __init__(self, reason: str):
        self.message += " " + reason
