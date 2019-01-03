import time

class ClientToken():

    token_type       = False
    epoch_expiration = False
    access_token     = False
    scope            = False

    def __init__(self, **data):

        self.token_type       = data.get('token_type', False)
        self.epoch_expiration = data.get('expires_in', 0) + int(time.time())
        self.access_token     = data.get('access_token', False)
        self.scope            = data.get('scope', False)
