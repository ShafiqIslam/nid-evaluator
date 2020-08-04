from app.modules.evaluator.bd.data_validator.incomplete_nid_data import IncompleteNIDData
from app.modules.evaluator.bd.data_validator.nid_data_does_not_match import NIDDataDoesNotMatch
from app.modules.evaluator.bd.data_validator.validator_locator import ValidatorLocator
from app.modules.evaluator.bd.nid import NID


class Validator:
    nid: NID

    def set_nid(self, nid: NID):
        self.nid = nid

    def validate(self):
        if self.nid.has_data() is False:
            raise IncompleteNIDData(self.nid.get_missing_key())
        self._validate_consistency()

    def _validate_consistency(self):
        validator = ValidatorLocator.get(self.nid)
        if validator.validate() is False:
            raise NIDDataDoesNotMatch()
