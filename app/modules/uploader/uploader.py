import os
from app.config import App
from app.common.helpers import get_time_string_file_name
from app.modules.uploader.unable_to_upload_file import UnableToUploadFile


class Uploader:
    @staticmethod
    def temp_upload(file):
        name = get_time_string_file_name(file.filename)
        if not os.path.exists(App.temp_image_folder):
            os.mkdir(App.temp_image_folder, 0o777)
        path = os.path.join(App.temp_image_folder, name)
        try:
            file.save(path)
            return path
        except Exception as e:
            raise UnableToUploadFile(e.__str__())
