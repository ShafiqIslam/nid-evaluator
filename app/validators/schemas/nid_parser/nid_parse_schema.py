from marshmallow import Schema, fields, pre_load, EXCLUDE
from app.common import Request
from app.modules.ocr import Ocr
from app.validators.schemas.nid_parser.file_not_selected import FileNotSelected
from app.validators.schemas.nid_parser.format_not_expected import FormatNotExcepted


class FILE(fields.Field):
    pass


class NidParseSchema(Schema):
    nid_image = FILE()

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def nid_image_validation(self, data, many, **kwargs):
        nid_image = Request.files['nid_image']
        if nid_image.filename == '':
            raise FileNotSelected()
        if nid_image and not Ocr.is_allowed(nid_image.filename):
            raise FormatNotExcepted()
        data.nid_image = nid_image
        return data
