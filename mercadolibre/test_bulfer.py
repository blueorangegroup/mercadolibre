from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category
meli = mercadolibre.Mercadolibre(
    '1685879569528665',
    'jM6uC0FbarNN49zvIQkG2ofZ9Zlp5BZj',
    'APP_USR-1685879569528665-020813-e34c871094892e7b7635ee4d6d06f99a-145144901',

)

# TG-5e0b93db386486000b0b019c-294914374

mercadolibre_site = mercadolibre_site.MercadolibreSite(
    '1685879569528665',
    'jM6uC0FbarNN49zvIQkG2ofZ9Zlp5BZj',
    'APP_USR-1685879569528665-020813-e34c871094892e7b7635ee4d6d06f99a-145144901',
)

# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
#res = meli.get_with_token('/shipments/41168519241')
res = meli.put_with_token('/shipments/41168519241', {
    'speed': 120,
    'status': "shipped",
    'tracking_number': "X-857-1887",
    "receiver_id": 229577938,
    "comments": "https://www.mdcargas.com/#/"
})
pprint(res.json())
