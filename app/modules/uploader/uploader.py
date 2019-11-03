from werkzeug.utils import secure_filename

from app.config import App


class Uploader:
    temp_dir = ''

    def __init__(self):
        self.temp_dir = App.temp_image_folder

    @classmethod
    def temp_upload(cls, file):
        name = secure_filename(file.filename)
        return file.save(cls.temp_dir, name)
