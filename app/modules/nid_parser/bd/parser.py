import importlib
import re

from app.common.helpers import log
from app.modules.nid_parser.bd.enums import Format, Side
from app.modules.nid_parser.exceptions.invalids import NotClearImage

from app.modules.ocr import Ocr, Preprocess


def exclude(data):
    result = re.sub(r'[-~—\\|+=\[\];*]', '', data.strip())
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
        output_old = self.parse_image(filename)
        log(output_old)
        if self.validOutput(output_old):
            return output_old

        self.format = Format.NEW.value
        output_new = self.parse_image(filename)
        if self.validOutput(output_new):
            return output_new
        raise NotClearImage()

    @staticmethod
    def validOutput(output):
        return output['nid_no'] is not None and output['name'] is not None

    @staticmethod
    def mergeOutput(output_old, output_new):
        return output_old
