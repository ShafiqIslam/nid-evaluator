import os
from app.common import Request
from app.common.exceptions import InvalidRequestException
from app.modules.evaluator import BDEvaluator
from app.validators.schemas.nid_parser.nid_parse_schema import NidParseSchema
from . import evaluator
from app.modules.uploader import Uploader

nid_parse_schema = NidParseSchema()


@evaluator.route('/evaluate', methods=['POST'])
def nid_parse():
    file_name = process_request()

    try:
        nid = BDEvaluator.evaluate(file_name)
        os.remove(file_name)
    except Exception as e:
        os.remove(file_name)
        raise e

    return {
        "code": 200,
        "message": "Successful",
        "data": nid.__dict__,
    }


def process_request():
    errors = nid_parse_schema.validate(Request.form)
    if errors:
        raise InvalidRequestException()
    nid_image = Request.files['nid_image']
    return Uploader.temp_upload(nid_image)
