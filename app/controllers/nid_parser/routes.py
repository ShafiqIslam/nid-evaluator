import os

from app.common import Request
from app.common.exceptions import InvalidRequestException
from app.common.helpers import log
from app.modules.nid_parser import BDNIDParser
from app.modules.ocr import Preprocess
from app.validators.schemas.nid_parser.nid_parse_schema import NidParseSchema
from . import nid_parser
from app.modules.ocr.exceptions import FileNotSelectedException, InvalidFileException
from app.modules.uploader import Uploader

nid_parse_schema = NidParseSchema()


@nid_parser.route('/parse-nid', methods=['POST'])
def nid_parse():
    try:
        errors = nid_parse_schema.validate(Request.form)
        if errors:
            log(errors)
            raise InvalidRequestException()
        nid_image = Request.files['nid_image']
        img_format = Request.form['format'].strip()
        img_side = Request.form['side'].strip()
        file_name = Uploader.temp_upload(nid_image)
        if file_name is not None:
            parser = BDNIDParser(img_format=img_format, side=img_side)
            data = parser.parse_image(file_name)
            data2 = parser.parse_image(file_name, Preprocess.THRESHOLD)
            os.remove(file_name)
            return {
                "code": 200,
                "message": "File Uploaded Successfully",
                "data": data,
                "data2": data2
            }
        else:
            raise InvalidFileException()
    except Exception as e:
        raise e
