from app.modules.evaluator.bd.image_classifier.available_classifier import AvailableClassifier
from app.modules.evaluator.bd.image_classifier.classifier_factory import ClassifierFactory
from app.modules.evaluator.bd.parser.parser_factory import ParserFactory
from .nid import NID
from .nid_format import NIDFormat
from .data_validator import DataValidator


def classify_image(filename: str) -> NIDFormat:
    classifier = ClassifierFactory.get(filename, AvailableClassifier.RESNET50)
    return classifier.classify()


def parse_image(nid_format: NIDFormat, filename: str) -> NID:
    parser = ParserFactory.get(nid_format, filename)
    return parser.parse()


def validate_nid_data(nid: NID):
    data_validator = DataValidator()
    data_validator.set_nid(nid)
    data_validator.validate()


class Evaluator:
    def __init__(self):
        pass

    @staticmethod
    def evaluate(filename) -> NID:
        nid_format = classify_image(filename)
        nid = parse_image(nid_format, filename)
        validate_nid_data(nid)
        return nid
