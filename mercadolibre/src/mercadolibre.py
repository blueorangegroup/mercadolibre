
from mercadolibre.python_sdk.lib import meli


class Mercadolibre(meli.Meli):

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        super(Mercadolibre, self).__init__(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token
        )

    def get_access_token(self):
        if self.access_token:
            return self.access_token
        app_client_values = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        access_data = self.post("/oauth/token", body=None, params=app_client_values)
        if access_data.status_code == 200:
            self.access_token = eval(access_data.content)['access_token']

    def post_with_token(self, path, body=None, extra_headers=None):
        return self.post(path, body=body, params={'access_token': self.access_token}, extra_headers=extra_headers)

    def put_with_token(self, path, body=None, extra_headers=None):
        return self.put(path, body=body, params={'access_token': self.access_token}, extra_headers=extra_headers)

    def get_with_token(self, path, extra_headers=None):
        return self.get(path, params={'access_token': self.access_token}, extra_headers=extra_headers)
