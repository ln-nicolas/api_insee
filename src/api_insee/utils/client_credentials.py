import base64
from api_insee.exeptions.auth_exeption import AuthExeption

class ClientCredentials():

    def __init__(self, key=False, secret=False):

        self.key     = key
        self.secret  = secret

        if not self.key or not self.secret:
            raise AuthExeption(self).invalidkeyAndSecret()

        self.encoded = self.getEncodedCredential()

    def getEncodedCredential(self):
        blike   = (self.key+':'+self.secret).encode('utf-8')
        encoded = base64.b64encode(blike).decode('utf-8')
        return encoded
