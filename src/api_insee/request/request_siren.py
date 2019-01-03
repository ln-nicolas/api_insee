import urllib.request as ur
import urllib.error as ue
import json

from api_insee.conf import API_VERSION
import api_insee.criteria as Criteria
from .request import Request

#from api_insee.exeptions.params_exeption import ParamsExeption

class RequestSiren(Request):

    def __init__(self, *args, **kwargs):

        if isinstance(args[0], str):
            self.init_from_string(*args, **kwargs)
        else:
            self.init_from_criteria(*args, **kwargs)

        self.init_siren_url_params()

    def init_from_string(self, siren, date=None):
        self.siren = siren
        self.date  = Criteria.Raw(date or "")
        super(RequestSiren, self).__init__(Criteria.Raw(""))

    def init_from_criteria(self, *criteria, date=None):
        self.siren = ""
        self.date  = Criteria.Raw(date or "")
        super(RequestSiren, self).__init__(*criteria)

    def init_siren_url_params(self):

        q    = self.criteria.toURLParams()
        date = self.date.toURLParams()

        if q: self.set_url_params('q', q)
        if date: self.set_url_params('date', date)

    @property
    def url_path(self):

        return (
            API_VERSION['url']
          + API_VERSION['path_siren']
          + ('/%s/' % self.siren if self.siren else '/')
        )
