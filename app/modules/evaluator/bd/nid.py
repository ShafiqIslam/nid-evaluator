from datetime import date
from app.modules.evaluator.bd.nid_format import NIDFormat


class NID:
    id_no: str
    name: str
    date_of_birth: date
    format: NIDFormat

    def has_data(self):
        return self.id_no is not None and self.name is not None and self.date_of_birth is not None

    def get_missing_key(self):
        if self.id_no is None:
            return "id no"
        if self.name is None:
            return "name"
        if self.date_of_birth is None:
            return "date of birth"
