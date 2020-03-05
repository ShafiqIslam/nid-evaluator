from datetime import date
from app.modules.evaluator.bd.parser import Parser
from typing import Final
import re


class NewNIDParser(Parser):
    regex: Final = r"(Name)|NID No(.+)|Birth(.+)|Nino(.+)?|nono([\w ]+)"
    keys: Final = ['name', 'nid_no', 'dob', 'nid_no', 'nid_no']

    def construct_nid(self):
        output = self.serialize()
        self.nid.id_no = output['nid_no']
        self.nid.name = output['name']
        self.nid.date_of_birth = date.today()

    def serialize(self):
        output = self.get_empty_output(self.keys)
        ex = r':+'
        i = 0
        for text in self.image_data_lines:
            text = re.sub(ex, '', text).strip()
            match = self.has_match(re.search(self.regex, text, re.IGNORECASE | re.UNICODE | re.MULTILINE | re.DOTALL))
            if match is None:
                continue
            index, content = match
            output[self.keys[index]] = content
            if 'name' == self.keys[index]:
                next_line = self.next_line_parse(i)
                if next_line:
                    output[self.keys[index]] = next_line
            i += 1
        return output

    def next_line_parse(self, data_index):
        if len(self.image_data_lines) > data_index + 1:
            return "{}".format(self.image_data_lines[data_index + 1])
