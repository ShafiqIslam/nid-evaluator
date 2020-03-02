from abc import ABC, abstractmethod
from app.modules.evaluator.bd.nid import NID
from app.modules.evaluator.bd.parser.functions import exclude_special_char
from app.modules.ocr import Ocr
from app.modules.ocr.enums import Language


class Parser(ABC):
    image_path: str
    image_data: str
    image_data_lines = []
    nid: NID

    def set_image(self, filename):
        self.image_path = filename

    def parse(self) -> NID:
        self.nid = NID()
        self.read_image()
        self.pre_process()
        self.construct_nid()
        return self.nid

    def read_image(self):
        ocr = Ocr()
        ocr.set_languages([Language.BN, Language.ENG])
        self.image_data = ocr.parse_image(self.image_path)

    def pre_process(self):
        lines = self.image_data.split("\n")
        for line in lines:
            e = exclude_special_char(line)
            if e is not False:
                self.image_data_lines.append(e)

    @abstractmethod
    def construct_nid(self):
        pass
