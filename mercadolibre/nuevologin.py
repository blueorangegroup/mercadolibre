from urllib.parse import urlencode
import requests, ssl, re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version
        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)


def make_path(path, params=None):
    params = params or {}
    # Making Path and add a leading / if not exist
    if not (re.search("^\/", path)):
        path = "/" + path
    path = "https://api.mercadolibre.com" + path
    if params:
        path = path + "?" + urlencode(params)

    return path


_requests = requests.Session()
try:
    SSL_VERSION = 'PROTOCOL_TLSv1'
    _requests.mount('https://', SSLAdapter(ssl_version=getattr(ssl, SSL_VERSION)))
except:
    _requests = requests

params = {'grant_type': 'client_credentials', 'client_id': '8867802852831644', 'client_secret': 'ocJrHXpoLWzfofZE2XWs7lKqrIuayc1e'}
headers = {'Accept': 'application/json', 'User-Agent': 'MELI-PYTHON-SDK-2.0.0', 'Content-type': 'application/json'}
uri = make_path("/oauth/token")
response = _requests.post(uri, params=urlencode(params), headers=headers, data=params)

print (response.content)
#
# params = {'grant_type': 'client_credentials', 'client_id': '1349863402307086', 'client_secret': 'Smn31Xc1LGgH3IaayWItcPGAvLp49wLS'}
# headers = {'Accept': 'application/json', 'User-Agent': 'MELI-PYTHON-SDK-2.0.0', 'Content-type': 'application/json'}
# uri = make_path("/oauth/token")
# response = _requests.post(uri, params=urlencode(params), headers=headers, data=params)
#
# print (response.content)