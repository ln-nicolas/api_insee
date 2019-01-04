import urllib.request as ur
import urllib.error as ue
import json

from api_insee.conf import API_VERSION
from .request import RequestService

class RequestTokenService(RequestService):

    def __init__(self, credentials):
        self.credentials = credentials

    @property
    def url_path(self):
        return API_VERSION['url'] + API_VERSION['path_token']

    @property
    def data(self):
        return "grant_type=client_credentials".encode('ascii')

    @property
    def header(self):
        return {
            'Authorization' : 'Basic %s' % (self.credentials.encoded)
        }
