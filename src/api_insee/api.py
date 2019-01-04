from api_insee.utils.auth_service import AuthService
from api_insee.request.request_entreprises import RequestEntrepriseServiceSiren, RequestEntrepriseServiceSiret

class ApiInsee():

    def __init__(self, key, secret):

        self.auth = AuthService(
            key = key,
            secret = secret
        )

        self.use('siren', RequestEntrepriseServiceSiren)
        self.use('siret', RequestEntrepriseServiceSiret)

    def use(self, serviceName, requestService):

        def wrap(*args, **kwargs):
            service = requestService(*args, **kwargs)
            service.useToken(self.auth.token)
            return service

        setattr(self, serviceName, wrap)
