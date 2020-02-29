from app.modules.evaluator.bd.nid_format import NIDFormat
from app.modules.evaluator.bd.parser.unable_to_classify_as_nid import UnableToClassifyAsNID


class Classifier:
    filename: str = None
    format: NIDFormat = NIDFormat.NEW

    def set_image(self, filename):
        self.filename = filename

    def classify(self) -> NIDFormat:

        if self.format is None:
            raise UnableToClassifyAsNID()

        return self.format
