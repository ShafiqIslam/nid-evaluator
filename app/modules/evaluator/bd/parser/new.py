from datetime import date
from app.modules.evaluator.bd.parser import Parser
from typing import Final
from app.modules.evaluator.bd.parser.functions import has_match, get_empty_output
import re


class NewNIDParser(Parser):
    regex: Final = r"(Name)|NID No(.+)|Birth(.+)|Nino(.+)?|nono([\w ]+)"
    keys: Final = ['name', 'nid_no', 'dob', 'nid_no', 'nid_no']

    def construct_nid(self):
        self.nid.id_no = "123"
        self.nid.name = "Test"
        self.nid.date_of_birth = date.today()

    def serialize(self):
        output = get_empty_output(self.keys)
        ex = r':+'
        i = 0
        for text in self.image_data_lines:
            text = re.sub(ex, '', text).strip()
            match = has_match(re.search(self.regex, text, re.I | re.M | re.U | re.S))
            if match is not None:
                index, content = match
                output[self.keys[index]] = content
                if 'name' == self.keys[index]:
                    output = self.next_line_parse(self.keys[index], output, i)
            i += 1
        return output

    def next_line_parse(self, query, output, data_index):
        if len(self.image_data_lines) > data_index + 1:
            output[query] = "{}".format(self.image_data_lines[data_index + 1])
        return output
