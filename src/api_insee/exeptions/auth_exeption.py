

class AuthExeption(Exception):

    credential = None

    def __init__(self, credential):
        self.credential = credential

    def invalidkeyAndSecret(self):
        self.message = "Invalid consumer key or secret. key : %s secret : %s" % (
            self.credential.key,
            self.credential.secret
        )

        return self

    def unauthorized(self, reason=False):
        self.message = "Api connection unauthorized. key : %s secret : %s" % (
            self.credential.key,
            self.credential.secret
        )

        if reason:
            self.message += "\n %s" % (reason)

        return self

    def __str__(self):
        return self.message
