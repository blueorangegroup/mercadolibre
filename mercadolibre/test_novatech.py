from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category
mercadolibre = mercadolibre.Mercadolibre(
    '7960706369164127',
    'u4F3RGYtG3SSYNvWhBTK77WMyi0x9H3b',
    'APP_USR-7960706369164127-071113-54def65d434492f1166e8a98181f6c98-294914374'
)


mercadolibre_site = mercadolibre_site.MercadolibreSite(
    '4860383088298642',
    'stY1A7O5K8unJITtcVNhr5QcJLKWAtJU',
    'APP_USR-7960706369164127-071107-380e6010c16aae6d49071e19cfaef032-294914374'
)

# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
#res = order.get_order_from_resource(mercadolibre, '/shipments/28009155822')
#res = order.get_order_from_resource(mercadolibre, '/orders/2070834351')
#res = order.get_order_from_resource(mercadolibre, '/payments/4922256059')

#res = order.get_order_from_resource(mercadolibre, '/orders/2045663884')
#res = order.get_order_from_resource(mercadolibre, '/orders/2030428587')
#res = mercadolibre.get_with_token('/shipments/28001940003')
#res = mercadolibre.get_with_token('/shipments/27994694366')
#res = mercadolibre.get_with_token(
#    '/users/294914374/items/search?sku=INTCOM-MT14&status=active'
#)

#res = mercadolibre.get_with_token('/users/me')

# PUBLICACIONES
#res = product.get_publication_from_id(mercadolibre, 'MLA793185853')

#res = category.get_main_categories(mercadolibre_site)

#print(res)
#pprint(res.json())
# res = mercadolibre.get_with_token('/items?ids={}&include_attributes=all'.format(','.join(res.json().get('results'))))
# for publication in res.json():
#     item = publication.get('body')
#     print(item.get('shipping'))
#     if item.get('shipping', {}).get('logistic_type') == 'fulfillment':
#         print('SOY FULLFIL {}'.format(item.get('id')))

#pprint(res.json().get('shipping_option', {}).get('cost'))
#pprint(res.json().get('shipping'))
res = mercadolibre.get_with_token('/messages/orders/2081244382')
pprint(res)
pprint(res.json())
