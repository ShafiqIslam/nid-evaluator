# import the necessary packages
import re

from PIL import Image
import pytesseract
import cv2
import os
from pytesseract import Output

from app.common.helpers import get_time_string_file_name, log
from app.config import App
from app.modules.ocr.enums import Preprocess, Lang

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DefaultLang = '{}+{}'.format(Lang.ENG.value, Lang.BN.value)


class Ocr:
    lang = DefaultLang
    output_type = Output.STRING
    temp = App.temp_image_folder
    preprocess = None

    def __init__(self, lang=DefaultLang, pre_process=None, output_type=Output.STRING):
        self.lang = lang
        self.output_type = output_type
        self.preprocess = pre_process
        pass

    @staticmethod
    def thresh(image):
        image = cv2.medianBlur(image, 5)
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    @staticmethod
    def blur(image, ksize=3):
        return cv2.GaussianBlur(image, (ksize, ksize), ksize)

    @staticmethod
    def allowed(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def parse_image(self, file, preprocess=None):
        output = None
        self.preprocess = preprocess
        if file is not None:
            filename = self.process_image(file)
            output = pytesseract.image_to_string(Image.open(filename), lang=self.lang, output_type=self.output_type)
            image_file = open("{}/{}".format(self.temp, 'output.log'), 'a')
            image_file.write("image: {} \n:{}\n".format(filename, re.sub(r"\n\n", '', output)))
        return output

    def process_image(self, file):
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = self.filter(gray)
        filename = "{}/{}".format(self.temp, get_time_string_file_name("_{}.png".format(os.getpid())))
        cv2.imwrite(filename, gray)
        return filename

    def filter(self, image):
        if self.preprocess is None:
            return image
        method = getattr(self, "{}".format(self.preprocess))
        return method(image)
