from app.modules.evaluator.bd.nid_format import NIDFormat
from app.modules.evaluator.bd.parser import Parser
from app.modules.evaluator.bd.parser.smart import SmartNIDParser
from app.modules.evaluator.bd.parser.casual import CasualNIDParser


class ParserFactory:
    @staticmethod
    def get(nid_format: NIDFormat, filename: str) -> Parser:
        if nid_format is NIDFormat.SMART:
            parser = SmartNIDParser()
        else:
            parser = CasualNIDParser()

        parser.set_image(filename)
        return parser
