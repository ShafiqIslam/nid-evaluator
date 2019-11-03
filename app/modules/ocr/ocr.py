# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os
from pytesseract import Output

from app.config import App

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class Ocr:
    lang = ''
    output_type = Output.STRING
    temp = App.temp_image_folder

    def __init__(self, lang='eng+ben', output_type=Output.STRING):
        self.lang = lang
        self.output_type = output_type

    @staticmethod
    def thresh(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    @staticmethod
    def blur(image, intensity=3):
        return cv2.medianBlur(image, intensity)

    @staticmethod
    def allowed(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @classmethod
    def parse_image(cls, file, preprocess='blur'):
        output = None
        if file is None:
            image = cv2.imread(file)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if preprocess == 'thresh':
                gray = cls.thresh(gray)
            else:
                gray = cls.blur(gray)
            filename = "{}/{}.png".format(cls.temp, os.getpid())
            cv2.imwrite(filename, gray)
            output = pytesseract.image_to_string(Image.open(filename), lang=cls.lang, output_type=cls.output_type)
            os.remove(filename)
        return output
