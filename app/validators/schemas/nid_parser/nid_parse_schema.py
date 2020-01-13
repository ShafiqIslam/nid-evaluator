import typing

from marshmallow import Schema, fields, pre_load, EXCLUDE

from app.common import Request
from app.common.exceptions import InvalidRequestException
from app.modules.nid_parser import BDNIDParser
from app.modules.nid_parser.bd.enums import Side
from app.modules.nid_parser.exceptions.invalids import FormatNotExcepted
from app.modules.ocr.exceptions import FileNotSelectedException


class FILE(fields.Field):
    pass


def validateSide(value):
    value = value.strip()
    if Side.has_value(value):
        return value
    else:
        raise InvalidRequestException('Side is invalid')


class SideField(fields.Field):
    def _deserialize(
            self,
            value: typing.Any,
            attr: typing.Optional[str],
            data: typing.Optional[typing.Mapping[str, typing.Any]],
            **kwargs
    ):
        return validateSide(value)


class NidParseSchema(Schema):
    side = SideField(required=True)
    nid_image = FILE()

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def nid_image_validation(self, data, many, **kwargs):
        try:
            nid_image = Request.files['nid_image']
            if nid_image.filename == '':
                raise FileNotSelectedException()
            if nid_image and not BDNIDParser.allowed(nid_image.filename):
                raise FormatNotExcepted()
            data.nid_image = nid_image
            return data
        except Exception as e:
            raise e


class NidParseFromUrlSchema(Schema):
    front = fields.URL(required=True)
    back = fields.URL(required=True)
