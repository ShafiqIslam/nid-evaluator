from app.modules.evaluator.bd.data_validator.nid_data_does_not_match import NIDDataDoesNotMatch
from app.modules.evaluator.bd.nid import NID


class Validator:
    nid: NID

    def set_nid(self, nid: NID):
        self.nid = nid

    def validate(self):
        if self.nid.has_data() is False:
            raise NIDDataDoesNotMatch()
