import importlib
import re

from app.modules.nid_parser.bd.constants import Quotes
from app.modules.nid_parser.bd.enums import Format, Side

from app.modules.ocr import Ocr, Preprocess


def exclude(data):
    result = re.sub(r'[-~—\\|+=\[\]]', '', data.strip())
    if not result == "" and not result == " ":
        return result
    else:
        return False


class Parser:
    side = Side.FRONT.value
    front_replace = Quotes.Replace
    format = Format.OLD.value

    def __init__(self, side=Side.FRONT.value, img_format=Format.OLD.value):
        self.side = side
        self.format = img_format
        pass

    @staticmethod
    def allowed(filename):
        return Ocr.allowed(filename)

    def parse_image(self, filename, pre_process=Preprocess.BLUR.value):
        data = Ocr().parse_image(filename, pre_process)
        module = importlib.import_module('app.modules.nid_parser.bd')
        class_name = "{}NIDParser".format(self.format)
        # method_call = getattr(self, methods, self.invalid_format)
        # return method_call(data)
        class_ = getattr(module, class_name)
        return class_(self.side).serialize(data)
