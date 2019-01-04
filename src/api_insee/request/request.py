
import urllib.request as ur
import urllib.parse as up
import urllib.error as ue
import json

from api_insee.conf import API_VERSION
from api_insee.exeptions.auth_exeption import AuthExeption
from api_insee.exeptions.request_exeption import RequestExeption
import api_insee.criteria as Criteria


class RequestService():

    _url_params = {}

    def __init__(self, *args, **kwargs):

        self._url_params = {}

        for (key, value) in kwargs.items():
            self.set_url_params(key, value)

    def init_criteria_from_dictionnary(self, dictionnary):
        self.criteria = Criteria.List(*[
            Criteria.Field(key, value)
            for (key, value) in dictionnary.items()
        ])

    def init_criteria_from_criteria(self, *args):
        self.criteria = Criteria.List(*args)

    def useToken(self, token):
        self.token = token

    def get(self):

        try:
            request  = self.getRequest()
            response = ur.urlopen(request)
            return self.formatResponse(response)
        except ue.HTTPError as EX:
            self.catchHTTPError(EX)
        except Exception as EX:
            raise Exception(self.url_encoded)


    def getRequest(self):

        return ur.Request(
            self.url_encoded,
            data    = self.data,
            headers = self.header
        )

    def formatResponse(self, response):
        raw    = response.read().decode('utf-8')
        parsed = json.loads(raw)
        return parsed

    @property
    def url(self):
        # url_encoded_params use urlencode, with
        # by default quote_plus
        return up.unquote_plus(self.url_encoded)

    @property
    def url_encoded(self):
        return self.url_path + self.url_encoded_params

    @property
    def url_path(self):
        return '/'

    @property
    def url_encoded_params(self):

        params = up.urlencode(self.url_params, quote_via=up.quote_plus).split('&')
        params = "&".join(sorted(params))

        if len(params) == 0:
            return ""
        else:
            return "?" + params

    @property
    def url_params(self):
        return self._url_params.copy()

    def set_url_params(self, name, value):

        if isinstance(value, dict):
            criteria = Criteria.List(*[
                Criteria.Field(key, value)
               for (key, value) in value.items()
           ]).toURLParams()

        elif isinstance(value, list) or \
             isinstance(value, tuple):
            criteria = Criteria.List(*value).toURLParams()

        elif isinstance(value, str) or \
             isinstance(value, int) or \
             isinstance(value, float):
            criteria = Criteria.Raw(str(value)).toURLParams()

        elif isinstance(value, Criteria.Base):
            criteria = value.toURLParams()

        else:
            raise Exception

        self._url_params[name] = criteria

    @property
    def data(self):
        return None

    @property
    def header(self):
        return {
            'Accept' : 'application/json',
            'Authorization' : 'Bearer %s' % (self.token.access_token)
        }


    def catchHTTPError(self, error):

        if error.code == 400:
            raise RequestExeption(self).badRequest()

        elif error.code == 401:
            raise AuthExeption(self.credentials).unauthorized(error.reason)

        else:
            raise error
