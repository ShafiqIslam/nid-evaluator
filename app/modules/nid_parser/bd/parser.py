import importlib
import re

from app.common.helpers import log
from app.modules.nid_parser.bd.constants import Quotes
from app.modules.nid_parser.bd.enums import Format, Side
from app.modules.nid_parser.exceptions.invalids import NotClearImage

from app.modules.ocr import Ocr, Preprocess


def exclude(data):
    result = re.sub(r'[-~—\\|+=\[\];]', '', data.strip())
    if not result == "" and not result == " ":
        return result
    else:
        return False


class Parser:
    side = Side.FRONT.value
    format = Format.OLD.value

    def __init__(self, side=Side.FRONT.value):
        self.side = side
        pass

    @staticmethod
    def allowed(filename):
        return Ocr.allowed(filename)

    def parse_image(self, filename, pre_process=None):
        data = Ocr().parse_image(filename, pre_process)
        module = importlib.import_module('app.modules.nid_parser.bd')
        class_name = "{}NIDParser".format(self.format)
        class_ = getattr(module, class_name)
        return class_(self.side).serialize(data)

    def parse(self, filename):
        output = self.parse_image(filename)
        if self.validOutput(output):
            return output

        self.format = Format.NEW.value
        output = self.parse_image(filename, Preprocess.BLUR.value)
        if self.validOutput(output):
            return output
        raise NotClearImage()

    @staticmethod
    def validOutput(output):
        return 'nid_number' in output and 'name' in output
