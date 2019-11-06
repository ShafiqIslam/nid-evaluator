import os

from app.common import Request
from app.common.exceptions import InvalidRequestException
from app.modules.nid_parser import BDNIDParser
from app.validators.schemas.nid_parser.nid_parse_schema import NidParseSchema
from . import nid_parser
from app.modules.ocr.exceptions import InvalidFileException
from app.modules.uploader import Uploader

nid_parse_schema = NidParseSchema()


@nid_parser.route('/parse-nid', methods=['POST'])
def nid_parse():
    try:
        errors = nid_parse_schema.validate(Request.form)
        if errors:
            raise InvalidRequestException()
        nid_image = Request.files['nid_image']
        img_side = Request.form['side'].strip()
        file_name = Uploader.temp_upload(nid_image)

        if file_name is None:
            raise InvalidFileException()
        try:
            parser = BDNIDParser(side=img_side)
            data = parser.parse(file_name)
            os.remove(file_name)
        except Exception as e:
            os.remove(file_name)
            raise e
        return {
            "code": 200,
            "message": "Data parsed successfully",
            "data": data,
        }

    except Exception as e:
        raise e
