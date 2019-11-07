import re

from app.common.helpers import log
from app.modules.nid_parser.bd.constants import Constants
from app.modules.nid_parser.bd.enums import Side
from app.modules.nid_parser.bd.functions import getEmptyOutput, hasMatch
from app.modules.nid_parser.nid_parser import NIDParser


class NewNidParser(NIDParser):

    def __init__(self, side=Side.FRONT.value):
        super().__init__(side)

    def preprocess(self, data):
        output = data.split("\n\n")
        return output

    def parse_back_data(self, data):
        pass

    def parse_front_data(self, data):
        indexes = Constants.front_data
        output = getEmptyOutput(indexes)
        return self.match(data, Constants.matches_front_new, indexes, output)

    @staticmethod
    def match(data, regex, indexes, output, back=False):
        ex = r':+'
        if back:
            ex = r':'
        i = 0
        for text in data:
            text = re.sub(ex, '', text).strip()
            match = hasMatch(re.search(regex, text, re.I))
            log(match)
            if match is not None:
                index, content = match
                output[indexes[index]] = content
                if 'name' == indexes[index]:
                    output['permanent_address'] = "{} {}".format(output['permanent_address'], data[i + 1])
            i += 1
        return output
