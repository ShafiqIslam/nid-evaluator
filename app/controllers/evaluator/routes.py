import os
from app.common import Request
from app.common.exceptions import InvalidRequestException, JSONException
from app.modules.evaluator import BDNIDEvaluator
from app.validators.schemas.nid_parser.nid_parse_schema import NidParseSchema, NidParseFromUrlSchema
from . import evaluator
from app.modules.ocr.exceptions import InvalidFileException
from app.modules.uploader import Uploader
from ...modules.evaluator.bd.enums import Side

nid_parse_schema = NidParseSchema()


@evaluator.route('/evaluate', methods=['POST'])
def nid_parse():
    file_name = process_request()

    try:
        data = BDNIDEvaluator().evaluate(file_name)
        os.remove(file_name)
    except Exception as e:
        os.remove(file_name)
        raise e

    return {
        "code": 200,
        "message": "Successful",
        "data": data,
    }


def process_request():
    errors = nid_parse_schema.validate(Request.form)
    if errors:
        raise InvalidRequestException()
    nid_image = Request.files['nid_image']
    # img_side = Request.form['side'].strip()
    file_name = Uploader.temp_upload(nid_image)

    if file_name is None:
        raise InvalidFileException()

    return file_name
