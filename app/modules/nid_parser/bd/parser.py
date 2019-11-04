import re

from app.common.helpers import log
from app.modules.nid_parser.bd.constants import Quotes
from app.modules.nid_parser.bd.enums import Format, Side
from app.modules.nid_parser.exceptions.invalids import InvalidFormatException
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
        methods = "serialize_{}".format(self.format)
        method_call = getattr(self, methods, self.invalid_format)
        return method_call(data)

    def serialize_old(self, data):
        newline_split = data.split("\n")
        processed = []
        for i in newline_split:
            e = exclude(i)
            if e is not False:
                processed.append(e)
        if len(processed) > 0:
            if self.side == Side.FRONT.value:
                data = self.format_front_data(processed)
            else:
                data = self.format_back_data(processed)
            return data
        return data

    def serialize_new(self, data):
        return data

    def format_front_data(self, data):
        data_sets = []
        dic = {}
        for outputs in data:
            split = outputs.split(": ")
            if len(split) > 1:
                data_sets.append([split[0], split[1]])
        for value in data_sets:
            log(value[0])
            key = value[0].strip()
            if key in self.front_replace:
                dic[self.front_replace[key]] = value[1]
            else:
                if 'address' in dic:
                    dic['address'] = "{} {}".format(dic['address'], value[1])
                else:
                    dic['address'] = value[1]
        return dic

    @staticmethod
    def format_back_data(data):
        return data

    def invalid_format(self):
        raise InvalidFormatException()
