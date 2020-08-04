from abc import ABC, abstractmethod

from app.modules.evaluator.bd.nid import NID


class ValidatorService(ABC):
    nid: NID

    def set_nid(self, nid: NID):
        self.nid = nid

    @abstractmethod
    def validate(self):
        pass
