from app.common import Request
from app.common.validation import schema
from app.controllers import nid_parser
from app.modules.ocr import Ocr
from app.modules.ocr.exceptions import FileNotSelectedException, InvalidFileException
from app.modules.uploader import Uploader


@nid_parser.route('/parse-nid', methods=['POST'])
@schema('/nid_parser/nid_parse.json')
def nid_parse():
    nid_image = Request.files['nid_image']
    if nid_image.filename == '':
        raise FileNotSelectedException()
    if nid_image and Ocr.allowed(nid_image.filename):
        file_name = Uploader.temp_upload(nid_image)
        return {
            "code": 200,
            "message": "File Uploaded Successfully",
            "name": file_name
        }
    else:
        raise InvalidFileException()
