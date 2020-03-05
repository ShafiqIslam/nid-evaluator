from .nid import NID
from .nid_format import NIDFormat
from .parser import Parser
from .data_validator import DataValidator
from .image_classifier import ImageClassifier


def classify_image(filename: str) -> NIDFormat:
    classifier = ImageClassifier()
    classifier.set_image(filename)
    return classifier.classify()


def get_parser(nid_format: NIDFormat, filename: str) -> Parser:
    if nid_format is NIDFormat.NEW:
        parser = Parser()
    else:
        parser = Parser()

    parser.set_image(filename)
    return parser


def parse_image(nid_format: NIDFormat, filename: str) -> NID:
    parser = get_parser(nid_format, filename)
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
