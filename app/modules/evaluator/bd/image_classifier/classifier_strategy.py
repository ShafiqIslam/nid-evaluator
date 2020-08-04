from abc import ABC, abstractmethod
from typing import Optional

from app.modules.evaluator.bd.nid_format import NIDFormat


class ClassifierStrategy(ABC):
    filename: str = None
    format: NIDFormat = None
    training_dataset: list
    test_dataset: list

    def set_image(self, filename):
        self.filename = filename

    def set_dataset(self, training_dataset, test_dataset):
        self.training_dataset= training_dataset
        self.test_dataset = test_dataset

    @abstractmethod
    def classify(self) -> Optional[NIDFormat]:
        pass
