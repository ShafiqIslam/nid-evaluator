import requests
from app.modules.evaluator.bd.nid import NID
from app.config import Porichoy as PorichoyConfig


class Porichoy:
    url: str
    api_key: str
    nid: NID

    def __init__(self):
        self.url = PorichoyConfig.url
        self.api_key = PorichoyConfig.api_key

    def set_nid(self, nid: NID):
        self.nid = nid

    def check(self):
        response = self.call()
        return 'passKyc' in response and response['passKyc'] != "no"

    def call(self):
        url = self.url + "?national_id=" + self.nid.id_no
        url += '&person_fullname=' + self.nid.name
        url += '&person_dob=' + self.nid.date_of_birth.__str__()

        headers = {'Ocp-Apim-Subscription-Key': self.api_key}

        response = requests.post(url, headers=headers)
        return response.json()
