
from pprint import pprint
import requests
from urllib.parse import urlencode


token_dcrocco = 'APP_USR-7577078471662421-110108-c1233eb9efd2f3b1aea65576f9fd0713-761350533'


#token_dtr = 'APP_USR-7116374573666927-083010-bceb7c754aa01b6ec6d0d12199787e65-199772443'
#token_nova = 'APP_USR-4030296695793169-030718-0facd08660c43cdfe728e9e358c7cb6f-2743712'
#token_electroaccess = 'APP_USR-89234852548127-030714-66a6282637e732ad43635549b0cf7a6b-685950789'
#token_es = 'APP_USR-8867802852831644-051019-df43d59e8a80f5b0c0b755e8cdf3d2bc-13262009'
#token_rejovot = 'APP_USR-2292843253910358-061708-622f98fd8b15b65a57741cfdbfdb555a-767897471'
#access_token_nova = {'access_token': token_nova, 'refresh-token': 'TG-604223efbf39fd00070ce121-13262009'}
#access_token_electroaccess = {'access_token': token_electroaccess, 'refresh-token': 'TG-6042ffcfbc4b1200073e0e5a-685950789'}
#access_token_es = {'access_token': token_es, 'refresh-token': 'TG-60451f51828ef80007e5bdf6-13262009'}
access_token_dcc = {'access_token': token_dcrocco, 'refresh-token': 'TG-63503576f4f56c0001bc5451-761350533', 'site_id': "MLA"}
#access_token_rejovot = {'access_token': token_rejovot, 'refresh-token': 'TG-60c9fd7728d2320008d27215-767897471', 'site_id': "MLA" }
#access_token_dtr = {'access_token': token_dtr, 'site_id': "MLA"}


#res = requests.post('https://api.mercadolibre.com/users/test_user', params=access_token_dcc, json={'site_id': "MLA"})
# (b'{"id":826029795,"nickname":"TETE9488169","password":"qatest841","site_status' b'":"active","email":"test_user_18700395@testuser.com"}')

#res = requests.post(url_auth_backend, json=json)

#res = res.json()
#date_from = res.get('date_created')
#nickname = res.get('buyer').get('nickname')
#res = requests.get('https://api.mercadolibre.com/orders/search?seller=13262009&order.date_created.from={}&order.date_created.to={}&q={}'.format(date_from, date_from, nickname), params=access_token_es)
#res = requests.get('https://api.mercadolibre.com/orders/{}'.format('4646890210'), params=access_token_rejovot)
#res = requests.get('https://api.mercadolibre.com/orders/{}'.format('4786163338'), params=access_token_dcc)
#res = requests.get('https://api.mercadolibre.com/orders/{}/shipments'.format('4786163338'), params=access_token_dcc)
#res = requests.post('https://api.mercadolibre.com/orders/{}/feedback'.format('4786163338'), json={'fulfilled': True, 'rating': 'positive'}, params=access_token_dcc)
#res = requests.get('https://api.mercadolibre.com/orders/4795456278', params=access_token_dtr)
res = requests.get('https://api.mercadolibre.com/orders/{}'.format('2000004464659008'), params=access_token_dcc)
pprint(res.json())
