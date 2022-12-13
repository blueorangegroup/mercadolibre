from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category
meli = mercadolibre.Mercadolibre(
    '8867802852831644',
    'ocJrHXpoLWzfofZE2XWs7lKqrIuayc1e',
    'APP_USR-8867802852831644-062206-adf17d7d8f912f45fe7c9a6fd48ed555-13262009',

)

# TG-5e0b93db386486000b0b019c-294914374

mercadolibre_site = mercadolibre_site.MercadolibreSite(
    '8867802852831644',
    'ocJrHXpoLWzfofZE2XWs7lKqrIuayc1e',
    'APP_USR-8867802852831644-051019-df43d59e8a80f5b0c0b755e8cdf3d2bc-13262009',
)

token = 'Slngpq757k3O0pGnDpggU54lbVgu8w6d1PS83kWV'
# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
#res = order.get_order_from_resource(mercadolibre, '/shipments/2190236756')
#res = order.get_order_from_resource(meli, '/orders/2000003746423748')
#res = order.get_order_from_resource(meli, '/orders/2000003746423748')
res = order.get_order_from_resource(meli, '/orders/2000003761246850')

# res = order.get_order_from_resource(meli, '/orders/4557463506')

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
