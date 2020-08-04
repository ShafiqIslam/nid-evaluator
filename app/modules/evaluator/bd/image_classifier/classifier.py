from app.modules.evaluator.bd.image_classifier.classifier_strategy import ClassifierStrategy
from app.modules.evaluator.bd.nid_format import NIDFormat
from app.modules.evaluator.bd.image_classifier.unable_to_classify_as_nid import UnableToClassifyAsNID


class Classifier:
    strategy: ClassifierStrategy

    def set_strategy(self, strategy: ClassifierStrategy):
        self.strategy = strategy

    def classify(self) -> NIDFormat:
        nid_format = self.strategy.classify()

        if nid_format is None:
            raise UnableToClassifyAsNID()

        return nid_format
