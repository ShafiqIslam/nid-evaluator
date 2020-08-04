import requests
from app.modules.evaluator.bd.data_validator.validator_service import ValidatorService
from app.config import Porichoy as PorichoyConfig


class Porichoy(ValidatorService):

    url: str
    api_key: str

    def __init__(self):
        self.url = PorichoyConfig.url
        self.api_key = PorichoyConfig.api_key

    def validate(self):
        response = self._call()
        return 'passKyc' in response and response['passKyc'] != "no"

    def _call(self):
        url = self.url + "?national_id=" + self.nid.id_no
        url += '&person_fullname=' + self.nid.name
        url += '&person_dob=' + self.nid.date_of_birth.__str__()

        headers = {'Ocp-Apim-Subscription-Key': self.api_key}

        response = requests.post(url, headers=headers)
        return response.json()
