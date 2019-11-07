import re

from app.common.helpers import log
from app.modules.nid_parser.bd.constants import Constants
from app.modules.nid_parser.bd.enums import Side, Format
from app.modules.nid_parser.bd.functions import hasMatch, getEmptyOutput
from app.modules.nid_parser.functions import exclude_special_char
from app.modules.nid_parser.nid_parser import NIDParser


class OldNidParser(NIDParser):

    def __init__(self, side=Side.FRONT.value):
        self.format = Format.OLD
        super().__init__(side)

    def preprocess(self, data):
        newline_split = data.split("\n")
        processed = []
        for i in newline_split:
            e = exclude_special_char(i)
            if e is not False:
                processed.append(e)
        return processed

    def parse_back_data(self, data):
        pass

    def parse_front_data(self, data):
        indexes = Constants.back_data
        output = getEmptyOutput(indexes)
        for text in data:
            text = re.sub(r':', '', text).strip()
            match = hasMatch(re.search(Constants.matches_front_old, text, re.I | re.S | re.U))
            if match is not None:
                index, content = match
                output[indexes[index]] = content
        return output
