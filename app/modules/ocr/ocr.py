import re
from typing import List
from PIL import Image
import pytesseract
import cv2
import os
from pytesseract import Output
from app.common.helpers import get_time_string_file_name, get_extension_from_filename
from app.config import App
from app.modules.ocr.enums import Language

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class Ocr:
    languages = Language.ENG.value
    preprocess = None

    def __init__(self, pre_process=None):
        self.preprocess = pre_process
        pass

    def set_languages(self, languages: List[Language]):
        if not isinstance(languages, List):
            languages = [languages]

        self.languages = ""
        for language in languages:
            self.languages += language.value + "+"

        self.languages = self.languages[:-1]

    @staticmethod
    def thresh(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU+cv2.THRESH_TOZERO)[1]

    @staticmethod
    def blur(image, ksize=3):
        return cv2.GaussianBlur(image, (ksize, ksize), ksize)

    @staticmethod
    def resize(img, scale_percent):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def is_allowed(filename):
        return get_extension_from_filename(filename) in ALLOWED_EXTENSIONS

    def parse_image(self, file, preprocess=None):
        self.preprocess = preprocess
        filename = self.process_image(file)
        output = pytesseract.image_to_string(Image.open(filename), lang=self.languages, output_type=Output.STRING)
        self.log_output(filename, output)
        return output

    @staticmethod
    def process_image(file):
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filename = "{}/{}".format(App.temp_image_folder, get_time_string_file_name("_{}.png".format(os.getpid())))
        cv2.imwrite(filename, gray)
        return filename

    def filter(self, image):
        if self.preprocess is None:
            return image
        method = getattr(self, "{}".format(self.preprocess))
        return method(image)

    @staticmethod
    def log_output(filename: str, output: str):
        log_file = open("{}/{}".format(App.temp_image_folder, 'output.log'), 'a')
        log_file.write("image: {} \n:{}\n".format(filename, re.sub(r"\n\n", '', output)))
