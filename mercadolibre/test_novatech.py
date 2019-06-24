from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category
mercadolibre = mercadolibre.Mercadolibre(
    '950742134248790',
    'sSHFXolSwIUBJQwaeFYCiHTh5vbn4VFr',
    'APP_USR-950742134248790-062414-e0d14cdb26d0df60caf940422d70f686-294914374'
)


mercadolibre_site = mercadolibre_site.MercadolibreSite(
    '4860383088298642',
    'stY1A7O5K8unJITtcVNhr5QcJLKWAtJU',
    'APP_USR-523586263281297-062018-c54e47492a38ff8e0b190b2524bc5459-437468731'
)

# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
# CASO DE MERCADOLIBRE FULL
res = order.get_order_from_resource(mercadolibre, '/orders/2061286594')
#res = order.get_order_from_resource(mercadolibre, '/orders/2062013078')
#res = order.get_order_from_resource(mercadolibre, '/orders/2030428587')

#res = mercadolibre.get_with_token('/shipments/27994694366')
#res = mercadolibre.get_with_token('/users/437468731/items/search?seller_sku=REF2&status=active')
#res = mercadolibre.get_with_token('/users/me')

# PUBLICACIONES
#res = product.get_publication_from_id(mercadolibre, 'MLA793185853')

#res = category.get_main_categories(mercadolibre_site)

#print(res)
pprint(res.json())
#pprint(res.json().get('total_amount_with_shipping'))
#pprint(res.json().get('shipping'))
