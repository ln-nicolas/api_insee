from api_insee.request.request_entreprises import (
    RequestEntrepriseServiceLiensSuccession, RequestEntrepriseServiceSiren,
    RequestEntrepriseServiceSiret)
from api_insee.utils.auth_service import AuthService, MockAuth


class ApiInsee():

    def __init__(self, key, secret, format='json', noauth=False):

        if noauth:
            self.auth = MockAuth()
        else:
            self.auth = AuthService(
                key = key,
                secret = secret
            )
        self.format = format

        self.use('siren', RequestEntrepriseServiceSiren)
        self.use('siret', RequestEntrepriseServiceSiret)
        self.use('liens_succession', RequestEntrepriseServiceLiensSuccession)

    def use(self, serviceName, requestService):

        def wrap(*args, **kwargs):
            service = requestService(*args, **kwargs)
            service.format = self.format
            service.useToken(self.auth.token)
            return service

        setattr(self, serviceName, wrap)
