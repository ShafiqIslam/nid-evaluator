from app.common.exceptions import JSONException


class IncompleteNIDData(JSONException):
    status_code = 404
    message = "NID data is incomplete."

    def __init__(self, missing: str):
        self.message += " " + missing + " is not available"
