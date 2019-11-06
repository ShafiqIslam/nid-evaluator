from abc import ABC, abstractmethod

from app.modules.nid_parser.bd.enums import Side, Format
from app.modules.nid_parser.exceptions.invalids import InvalidSideException, NotClearImage
from app.modules.ocr import Ocr


class NIDParser(ABC):
    side = None
    format = Format.OLD

    def __init__(self, side=Side.FRONT.value):
        self.side = side

    def parseImage(self, filename):
        data = Ocr().parse_image(filename)
        self.serialize(data)
        return self

    def serialize(self, data):
        data = self.preprocess(data)
        methods = "parse_{}_data".format(self.side)
        method_call = getattr(self, methods, self.invalid_format)
        output = method_call(data)
        if 'nid_number' not in output or 'name' not in output:
            raise NotClearImage()
        return output

    @abstractmethod
    def preprocess(self, data):
        pass

    @abstractmethod
    def parse_front_data(self, data):
        pass

    @abstractmethod
    def parse_back_data(self, data):
        pass

    def invalid_format(self):
        raise InvalidSideException()
