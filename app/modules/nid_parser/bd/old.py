import re

from app.modules.nid_parser.bd.constants import Quotes
from app.modules.nid_parser.bd.enums import Side, Format
from app.modules.nid_parser.nid_parser import NIDParser


def exclude_char(data):
    result = re.sub(r'[-~—\\|+=\[\]]', '', data.strip())
    if not result == "" and not result == " ":
        return result
    else:
        return False


class OldNidParser(NIDParser):
    front_replace = Quotes.ReplaceOld

    def __init__(self, side=Side.FRONT.value):
        self.format = Format.OLD
        super().__init__(side)

    def preprocess(self, data):
        newline_split = data.split("\n")
        processed = []
        for i in newline_split:
            e = exclude_char(i)
            if e is not False:
                processed.append(e)
        return processed

    def parse_back_data(self, data):
        pass

    def parse_front_data(self, data):
        data_sets = []
        dic = {}
        for outputs in data:
            split = outputs.split(": ")
            if len(split) > 1:
                data_sets.append([split[0], split[1]])
        for value in data_sets:
            key = value[0].strip()
            if key in self.front_replace:
                dic[self.front_replace[key]] = value[1]
            else:
                self.populateRandom(dic, value)

        return dic

    def populateRandom(self, dic, value):
        for key in self.front_replace:
            if key not in dic:
                dic[key] = ' '.join(value)
                return
