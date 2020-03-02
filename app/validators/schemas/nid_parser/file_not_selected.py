from app.common.exceptions import ValidationFailed


class FileNotSelected(ValidationFailed):
    status_code = 404
    message = "No file is selected"
