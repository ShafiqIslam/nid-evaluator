from app.modules.evaluator.bd.data_validator.porichoy import Porichoy
from app.modules.evaluator.bd.data_validator.validator_service import ValidatorService
from app.modules.evaluator.bd.nid import NID


class ValidatorLocator:

    @staticmethod
    def get(nid: NID) -> ValidatorService:
        validator = Porichoy()
        validator.set_nid(nid)
        return validator
