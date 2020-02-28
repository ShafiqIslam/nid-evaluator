import importlib
import os
import re

from app.common.helpers import log
from app.modules.evaluator.bd.enums import Format, Side
from app.modules.evaluator.exceptions.invalids import NotClearImage

from app.modules.ocr import Ocr, Preprocess
from app.modules.uploader import Uploader


def exclude(data):
    result = re.sub(r'[-~—\\|+=\[\];*]', '', data.strip())
    if not result == "" and not result == " ":
        return result
    else:
        return False


class BDNIDEvaluator:
    side = Side.FRONT.value
    format = Format.OLD.value

    def __init__(self):
        pass

    @staticmethod
    def allowed(filename):
        return Ocr.allowed(filename)

    def parse_image(self, filename, pre_process=None):
        data = Ocr().parse_image(filename, pre_process)
        module = importlib.import_module('app.modules.evaluator.bd')
        class_name = "{}NIDParser".format(self.format)
        class_ = getattr(module, class_name)
        return class_(self.side).serialize(data)

    def evaluate(self, filename):
        filter_img = None
        if self.side == Side.BACK.value:
            filter_img = Preprocess.THRESHOLD.value
        output_old = self.parse_image(filename, filter_img)
        if self.validOutput(output_old):
            return output_old

        self.format = Format.NEW.value
        output_new = self.parse_image(filename, filter_img)
        if self.validOutput(output_new):
            return output_new
        raise NotClearImage()

    def parse_from_url(self, url, name):
        filename = Uploader.temp_upload_from_url(url, "{}_{}".format(self.side, name))
        filter_img = None
        if self.side == Side.BACK.value:
            filter_img = Preprocess.THRESHOLD.value
        output_old = self.parse_image(filename, filter_img)

        self.format = Format.NEW.value
        output_new = self.parse_image(filename, filter_img)
        os.remove(filename)
        log(output_new, output_old)
        return self.mergeOutput(output_new, output_old)

    def validOutput(self, output):
        log(self.side)
        if self.side == Side.FRONT.value:
            return output['nid_no'] is not None and output['name'] is not None

        return True

    @staticmethod
    def mergeOutput(dic1, dic2):
        dict3 = {**dic1, **dic2}
        for key, value in dict3.items():
            if key in dic1 and key in dic1:
                if not value:
                    dict3[key] = dic1[key]

        return dict3
