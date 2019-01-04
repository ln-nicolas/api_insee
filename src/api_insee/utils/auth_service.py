from api_insee.utils.client_credentials import ClientCredentials
from api_insee.utils.client_token import ClientToken
from api_insee.request.request_token import RequestTokenService

class AuthService():

    token = None

    def __init__(self, key=False, secret=False):

        self.credentials = ClientCredentials(
            key    = key,
            secret = secret
        )
        self.generateToken()

    def generateToken(self):
        data = RequestTokenService(self.credentials).get()
        self.token = ClientToken(**data)
