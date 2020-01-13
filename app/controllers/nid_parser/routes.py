import os

from app.common import Request
from app.common.exceptions import InvalidRequestException, JSONException
from app.modules.nid_parser import BDNIDParser
from app.validators.schemas.nid_parser.nid_parse_schema import NidParseSchema, NidParseFromUrlSchema
from . import nid_parser
from app.modules.ocr.exceptions import InvalidFileException
from app.modules.uploader import Uploader
from ...common.helpers import log, get_filename_from_url
from ...modules.nid_parser.bd.enums import Side

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


@nid_parser.route('/parse-from-url', methods=['POST'])
def parse_from_url():
    try:

        nid_parse_schema_from_url = NidParseFromUrlSchema()
        errors = nid_parse_schema_from_url.validate(Request.form)
        if errors:
            raise InvalidRequestException()
        data = Request.form
        parser = BDNIDParser(side=Side.FRONT.value)
        front_file_name = get_filename_from_url(data.get('front'))
        output_front = parser.parse_from_url(data.get('front'), front_file_name)
        parser = BDNIDParser(side=Side.BACK.value)
        back_file_name = get_filename_from_url(data.get('back'))
        back_data = parser.parse_from_url(data.get('back'), back_file_name)
        return {"code": 200, "data": {"front": output_front, "back": back_data}}
    except Exception as e:
        raise e
