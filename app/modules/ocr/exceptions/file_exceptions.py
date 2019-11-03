from app.common.exceptions import JSONException


class InvalidFileException(JSONException):
    status_code = 400
    message = "Selected File is invalid"


class FileNotSelectedException(JSONException):
    status_code = 404
    message = "No file is selected"
