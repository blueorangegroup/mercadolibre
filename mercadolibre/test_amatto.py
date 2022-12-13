from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category
meli = mercadolibre.Mercadolibre(
    '362798896691254',
    'HT7QzTjmcQNYiKKT1XPJvkL2JxDqposr',
    'APP_USR-362798896691254-081011-8cc1e0972d37118647c77a244f715fd1-156247907',

)

# TG-5e0b93db386486000b0b019c-294914374


mercadolibre_site = mercadolibre_site.MercadolibreSite(
    '362798896691254',
    'HT7QzTjmcQNYiKKT1XPJvkL2JxDqposr',
    'APP_USR-362798896691254-081011-8cc1e0972d37118647c77a244f715fd1-156247907',

)
# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
#res = order.get_order_from_resource(mercadolibre, '/shipments/2190236756')
res = order.get_order_from_resource(mercadolibre, '/orders/2000003731247729')
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
#res = order.get_order_from_resource(meli, '/orders/2249215846')
pprint(res.json())
#pprint(res)
#res = mercadolibre.get_with_token('/users/294914374/applications')
#pprint(res.json())
#pprint(res.json())
