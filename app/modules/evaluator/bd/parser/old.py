from datetime import date
from app.modules.evaluator.bd.parser import Parser
from app.modules.evaluator.bd.parser.functions import has_match, get_empty_output
import re
from typing import Final


class OldNIDParser(Parser):
    regex: Final = r"Name([\w ]+)|ID NO([\w ]+).|Date of Birth(.+)|IDNO([\w ]+)."
    keys: Final = ['name', 'nid_no', 'dob', 'nid_no']

    def construct_nid(self):
        output = self.serialize()
        self.nid.id_no = output['nid_no']
        self.nid.name = output['name']
        self.nid.date_of_birth = date.today()  # output['dob']

    def serialize(self):
        output = get_empty_output(self.keys)
        for line in self.image_data_lines:
            text = re.sub(r':+', '', line).strip()
            match = has_match(re.search(self.regex, text, re.IGNORECASE | re.UNICODE | re.MULTILINE))
            if match is not None:
                index, content = match
                output[self.keys[index]] = content
        return output
