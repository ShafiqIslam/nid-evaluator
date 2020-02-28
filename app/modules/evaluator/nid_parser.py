from abc import ABC, abstractmethod
from app.modules.evaluator.bd.enums import Side, Format
from app.modules.evaluator.exceptions.invalids import InvalidSideException, NotClearImage
from app.modules.ocr import Ocr


class NIDParser(ABC):
    side = None
    format = Format.OLD
    preprocess_filter = None

    def __init__(self, side=Side.FRONT.value, preprocess=None):
        self.side = side
        self.filter = filter
        self.preprocess_filter = preprocess

    def parseImage(self, filename):
        data = Ocr().parse_image(filename, preprocess=self.preprocess_filter)
        self.serialize(data)
        return self

    def serialize(self, data):
        data = self.preprocess(data)
        methods = "parse_{}_data".format(self.side)
        method_call = getattr(self, methods, self.invalid_format)
        output = method_call(data)
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
