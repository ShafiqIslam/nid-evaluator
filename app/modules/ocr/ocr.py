# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os
from pytesseract import Output

from app.common.helpers import get_time_string_file_name
from app.config import App
from app.modules.ocr.enums import Preprocess, Lang

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
DefaultLang = '{}+{}'.format(Lang.ENG.value, Lang.BN.value)


class Ocr:
    lang = DefaultLang
    output_type = Output.STRING
    temp = App.temp_image_folder

    def __init__(self, lang=DefaultLang, output_type=Output.STRING):
        self.lang = lang
        self.output_type = output_type
        pass

    @staticmethod
    def thresh(image):
        # return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_TOZERO)[0]
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)[1]

    @staticmethod
    def blur(image, intensity=3):
        return cv2.GaussianBlur(image, (7, 7), intensity)

    @staticmethod
    def allowed(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def parse_image(self, file, preprocess=Preprocess.BLUR.value):
        output = None
        if file is not None:
            filename = self.process_image(file, preprocess)
            output = pytesseract.image_to_string(Image.open(filename), lang=self.lang, output_type=self.output_type)
            # os.remove(filename)
        return output

    def process_image(self, file, preprocess):
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # if preprocess == Preprocess.THRESHOLD.value:
        #     gray = self.thresh(gray)
        # else:
        #     gray = self.blur(gray)
        filename = "{}/{}".format(self.temp, get_time_string_file_name("_{}.png".format(os.getpid())))
        cv2.imwrite(filename, gray)
        return filename
