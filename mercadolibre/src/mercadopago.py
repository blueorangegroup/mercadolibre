from mercadolibre.python_sdk.lib import meli


class Mercadopago(meli.Meli):

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        super(Mercadopago, self).__init__(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token
        )
        self.mpago_root_url = "https://api.mercadopago.com"

    def post_with_token(self, path, body=None, extra_headers=None):
        return self.post(path, body=body, params={'access_token': self.access_token}, extra_headers=extra_headers)

    def put_with_token(self, path, body=None, extra_headers=None):
        return self.put(path, body=body, params={'access_token': self.access_token}, extra_headers=extra_headers)

    def get_with_token(self, path, extra_headers=None):
        return self.get(path, params={'access_token': self.access_token}, extra_headers=extra_headers)

    def make_path(self, path, params=None):
        """ Copio la original pero usando la URL de Mercadopago """
        params = params or {}
        if not (re.search("^\/", path)):
            path = "/" + path
        path = self.mpago_root_url + path
        if params:
            path = path + "?" + urlencode(params)
        return path
