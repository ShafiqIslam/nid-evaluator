import re

from app.common.helpers import log
from app.modules.evaluator.bd import OldNidParser
from app.modules.evaluator.bd.constants import Constants
from app.modules.evaluator.bd.enums import Side
from app.modules.evaluator.bd.functions import getEmptyOutput, hasMatch
from app.modules.evaluator.nid_parser import NIDParser


class NewNidParser(NIDParser):

    def __init__(self, side=Side.FRONT.value):
        super().__init__(side)

    def preprocess(self, data):
        output = data.split("\n\n")
        final = []
        for item in output:
            sp = item.split("\n")
            final.append(sp[0])
            log(sp)
            if len(sp) > 1:
                final.append(sp[1])

        return final

    def parse_back_data(self, data):
        indexes = Constants.back_data
        output = getEmptyOutput(indexes)
        return OldNidParser.match(data, Constants.matches_back_old, indexes, output, True)

    def parse_front_data(self, data):
        indexes = Constants.front_data
        output = getEmptyOutput(indexes)
        return self.match(data, Constants.matches_front_new, indexes, output)

    def match(self, data, regex, indexes, output, back=False):
        ex = r':+'
        if back:
            ex = r':'
        i = 0
        for text in data:
            text = re.sub(ex, '', text).strip()
            match = hasMatch(re.search(regex, text, re.I | re.M | re.U | re.S))
            if match is not None:
                index, content = match
                output[indexes[index]] = content
                output = self.nextLineParse('name', indexes[index], output, i, data)
                output = self.nextLineParse('father_name', indexes[index], output, i, data)
                output = self.nextLineParse('mother_name', indexes[index], output, i, data)
                output = self.nextLineParse('bn_name', indexes[index], output, i, data)
                output = self.nextLineParse('husband', indexes[index], output, i, data)
            i += 1
        return output

    @staticmethod
    def nextLineParse(query, match, output, data_index, data):
        if query == match:
            if len(data) > data_index + 1:
                output[query] = "{}".format(data[data_index + 1])
        return output
