import urllib.request as ur
import urllib.error as ue
import json

from api_insee.conf import API_VERSION
import api_insee.criteria as Criteria
from api_insee.exeptions.request_exeption import RequestExeption
from .request import RequestService



#from api_insee.exeptions.params_exeption import ParamsExeption

class RequestEntrepriseService(RequestService):

    path = ""

    def __init__(self, *args, **kwargs):

        champs = kwargs.get('champs', False)
        if champs and isinstance(champs, list):
            kwargs.update({
                'champs' : ",".join(champs)
            })

        self.reference = False
        if len(args) and isinstance(args[0], str):
            self.reference = args[0]
            args = args[1:]

        super(RequestEntrepriseService, self).__init__(*args, **kwargs)

    @property
    def url_path(self):

        return (
            API_VERSION['url']
          + self.path
          + ('/%s' % self.reference if self.reference else '')
        )

    def pages(self, nombre=100):

        if self.format == 'csv':
            raise RequestExeption('You cannot use csv format with cursor')

        cursor = False
        next_cursor = "*"

        nombre = self._url_params.get('nombre', nombre)
        self.set_url_params('nombre', nombre)

        while cursor != next_cursor:
            self.set_url_params('curseur', next_cursor)
            page = self.get()

            yield page

            cursor = page['header']['curseur']
            next_cursor = page['header']['curseurSuivant']



class RequestEntrepriseServiceSiren(RequestEntrepriseService):
    path = API_VERSION['path_siren']

class RequestEntrepriseServiceSiret(RequestEntrepriseService):
    path = API_VERSION['path_siret']
