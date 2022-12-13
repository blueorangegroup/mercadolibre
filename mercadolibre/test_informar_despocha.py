import requests
from pprint import pprint
import datetime


access_token = {'access_token': "APP_USR-7577078471662421-091714-290b875689ac006030e054b6315e8fd9-826029795"}
"""
# 2) SE ARMA JSON CON EL CODE Y LOS PARAMETROS DE LA APP GENERADA
json = {
    'grant_type': 'authorization_code',
    'client_id': '7577078471662421',
    'client_secret': '0Iyug6EabAqFwm92iLrIPpBUknk2ULsP',
    'code': 'TG-6144a3dc5e22e5000a10f334-826029795',
    'redirect_uri': 'https://mercadolibre.com'
}
url_auth_backend = "https://api.mercadolibre.com/oauth/token"
res = requests.post(url_auth_backend, json=json)

# SE OBTIENE EL REFRESH Y APP TOKEN DE LA RESPUESTA
"""

ship_id = '40843313708'
tracking_values = {"tracking_number": "OP123456789AR"}


def poner_tracking(shipment_id, tracking_number):
    res = requests.put(
        'https://api.mercadolibre.com/shipments/{}'.format(shipment_id), params=access_token, json=tracking_number
    )
    pprint(res.json())


def consultar_shipping(shipment_id):
    res = requests.get('https://api.mercadolibre.com/shipments/{}'.format(shipment_id), params=access_token)
    pprint(res.json())


def informar_despocha(shipment_id):
    res = requests.post(
        'https://api.mercadolibre.com/shipments/{}/seller_notifications'.format(shipment_id),
        params=access_token,
        json={
            'payload': {
                'comment': 'despachado',
                # 'date': datetime.datetime.now().isoformat()
                'date': '2021-09-17T12:00:51.175-03:00'
            },
            'status': 'shipped',
            'substatus': 'null'
        }
    )
    pprint(res.json())


consultar_shipping(ship_id)
print(datetime.datetime.now().isoformat())
#informar_despocha(ship_id)