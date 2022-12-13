import requests
from pprint import pprint

# 1) SE LE PEGA A ESTA URL Y SE TOMA DEL REDIRECT EL TOKEN
# url_auth = "https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id=7577078471662421"
# TOKEN = TG-6144924d99b2870008e22fdd-92492618
# token = TG-6144cee35e22e5000a112f50-826159977

access_token = {'access_token': "APP_USR-7577078471662421-091713-6c4cefb90be4529b3303bda8b9be44ca-92492618"}

"""
# 2) SE ARMA JSON CON EL CODE Y LOS PARAMETROS DE LA APP GENERADA
json = {
    'grant_type': 'authorization_code',
    'client_id': '7577078471662421',
    'client_secret': '0Iyug6EabAqFwm92iLrIPpBUknk2ULsP',
    'code': 'TG-6144cee35e22e5000a112f50-826159977',
    'redirect_uri': 'https://mercadolibre.com'
}
url_auth_backend = "https://api.mercadolibre.com/oauth/token"
res = requests.post(url_auth_backend, json=json)
pprint(res.json())
# SE OBTIENE EL REFRESH Y APP TOKEN DE LA RESPUESTA
"""

# 3) CREAMOS EL USUARIO DE PRUEBA
#access_token = {'access_token': 'token', 'refresh-token': 'refresh_token'}
# res = requests.post('https://api.mercadolibre.com/users/test_user', params=access_token, json={'site_id': "MLA"})
# print(res.content)
# la respuesta tendra el login:
# {"id":826029795,"nickname":"TETE9488169","password":"qatest841",
# "site_status' b'":"active","email":"test_user_18700395@testuser.com"}
# {"id":826159977,"nickname":"TESTWTXAUV5J","password":"qatest1222",
# "site_status":"active","email":"test_user_63748917@testuser.com"}'

# 4) OBTENER TOKEN PARA EL USUARIO DE PRUEBA:
# HACER LO MISMO QUE EL PASO 1 y 2 PERO LOGEADO CON EL USER DE PRUEBA