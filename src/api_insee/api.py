from api_insee.utils.auth_service import AuthService
from api_insee.request.request_siren import RequestSiren

class ApiInsee():

    def __init__(self, key, secret):

        self.auth = AuthService(
            key = key,
            secret = secret
        )

        self.use('siren', RequestSiren)

    def use(self, serviceName, requestService):

        def wrap(*args, **kwargs):
            service = requestService(*args, **kwargs)
            service.useToken(self.auth.token)
            return service

        setattr(self, serviceName, wrap)
