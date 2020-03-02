from app.common.exceptions import ValidationFailed


class FormatNotExcepted(ValidationFailed):
    status_code = 500
    message = "Invalid format given for image"
