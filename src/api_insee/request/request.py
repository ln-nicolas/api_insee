import ssl
import urllib.request as ur
import urllib.parse as up
import urllib.error as ue
import json

from api_insee.conf import API_VERSION
from api_insee.exeptions.auth_exeption import AuthExeption
from api_insee.exeptions.request_exeption import RequestExeption
import api_insee.criteria as Criteria


class RequestService(object):

    _url_params = {}
    _accept_format = 'application/json'

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

    def get(self, format=None, method='get'):

        if format:
            self.format = format

        try:

            if method == 'get':
                request = self.getRequest()
            elif method == 'post':
                request = self.postRequest()
            gcontext = ssl.SSLContext()
            response = ur.urlopen(request, context=gcontext)
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

    def postRequest(self):

        header = self.header
        header.update({
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        data = up.urlencode(self._url_params).encode('utf-8')

        return ur.Request(
            self.url_path,
            data=data,
            headers = header
        )

    def formatResponse(self, response):

        if self.format == 'json':
            return self.formatResponseJson(response)

        if self.format == 'csv':
            return self.formatResponseCsv(response)

    def formatResponseJson(self, response):
        raw = response.read().decode('utf-8')
        parsed = json.loads(raw)
        return parsed

    def formatResponseCsv(self, response):
        raw = response.read().decode('utf-8')
        return raw

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
            'Accept' : self._accept_format,
            'Authorization' : 'Bearer %s' % (self.token.access_token)
        }

    @property
    def format(self):
        if self._accept_format == 'application/json':
            return 'json'
        if self._accept_format == 'text/csv':
            return 'csv'

    @format.setter
    def format(self, value):
        if value == 'csv':
            self._accept_format = 'text/csv'
        if value == 'json':
            self._accept_format == 'application/json'

    def catchHTTPError(self, error):

        if error.code == 400:
            raise RequestExeption(self).badRequest()

        elif error.code == 401:
            raise AuthExeption(self.credentials).unauthorized(error.reason)

        else:
            raise error
