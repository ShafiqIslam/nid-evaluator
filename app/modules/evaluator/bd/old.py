import re

from app.common.helpers import log
from app.modules.evaluator.bd.constants import Constants
from app.modules.evaluator.bd.enums import Side, Format
from app.modules.evaluator.bd.functions import hasMatch, getEmptyOutput
from app.modules.evaluator.functions import exclude_special_char
from app.modules.evaluator.nid_parser import NIDParser


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
        indexes = Constants.back_data
        output = getEmptyOutput(indexes)
        return self.match(data, Constants.matches_back_old, indexes, output, True)

    def parse_front_data(self, data, back=False):
        indexes = Constants.front_data
        output = getEmptyOutput(indexes)
        return self.match(data, Constants.matches_front_old, indexes, output, back)

    @staticmethod
    def match(data, regex, indexes, output, back=False):
        ex = r':+'
        if back:
            ex = r':'
        i = 0
        for text in data:
            text = re.sub(ex, '', text).strip()
            match = hasMatch(re.search(regex, text, re.I | re.U | re.M))
            if match is not None:
                index, content = match
                output[indexes[index]] = content
                if 'address' == indexes[index]:
                    output['address'] = "{} {}".format(output['address'], data[i + 1])
            i += 1
        return output
