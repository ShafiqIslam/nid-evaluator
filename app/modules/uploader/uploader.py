import os

import requests

from app.common import Request
from app.config import App
from app.common.helpers import log, get_time_string_file_name


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
            return None

    @staticmethod
    def temp_upload_from_url(url, name):
        if not os.path.exists(App.temp_image_folder):
            os.mkdir(App.temp_image_folder, 0o777)
        path = os.path.join(App.temp_image_folder, name)
        file = requests.get(url)
        open(path, "wb").write(file.content)
        return path
