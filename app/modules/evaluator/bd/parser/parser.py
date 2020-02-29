from datetime import date

from app.modules.evaluator.bd.nid import NID


class Parser:
    image: str

    def set_image(self, filename):
        self.image = filename

    def parse(self) -> NID:
        nid = NID()
        nid.id_no = "123"
        nid.name = "Test"
        nid.date_of_birth = date.today()
        return nid
