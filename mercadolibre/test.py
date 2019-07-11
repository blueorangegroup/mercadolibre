from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category
mercadolibre = mercadolibre.Mercadolibre(
    '1456087168099499',
    'idgjpAIjig8LJRjPvGac7NfaxdaJjPBF',
    'APP_USR-1456087168099499-071112-8b0de90187380f3ff196d7af77e16469-445346519'
)
mercadolibre_site = mercadolibre_site.MercadolibreSite(
    '1456087168099499',
    'idgjpAIjig8LJRjPvGac7NfaxdaJjPBF',
    'APP_USR-1456087168099499-071112-8b0de90187380f3ff196d7af77e16469-445346519'
)


# post('/users/test_user', access_token=....")
# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}
# {"id": 448773145, "nickname": "TETE2325736", "password": "qatest7469", "site_status": "active", "email": "test_user_39276001@testuser.com"}

# ORDENES
#print(mercadolibre.client_id)
#res = order.get_order_from_resource(mercadolibre, '/orders/2063424046')
#res = order.get_order_from_resource(mercadolibre, '/orders/2059281404')
#res = order.get_order_from_resource(mercadolibre, '/orders/2030428587')

#res = mercadolibre.get_with_token('/shipments/27994694366')
#res = mercadolibre.get_with_token('/users/445346519/items/search?seller_sku=REF1&status=active')
#res = mercadolibre.get_with_token('/users/445346519/items/search?sku=oso2&status=active')

#res = mercadolibre.get_with_token('/users/me')

# PUBLICACIONES
#res = product.get_publication_from_id(mercadolibre, 'MLA793185853')

#res = category.get_main_categories(mercadolibre_site)

#print(res)
# pprint(res.json())
# if res.json().get('results'):
#     res = mercadolibre.get_with_token('/items?ids={}&include_attributes=all'.format(','.join(res.json().get('results'))))
#     print(res)
#     pprint(res.json())

#pprint(res.json().get('total_amount_with_shipping'))
#pprint(res.json().get('shipping'))


#res = mercadolibre.get_with_token('/orders/2072409922')
#pprint(res.json())
item = {}
item['from'] = {'user_id': 445346519}
item['to'] = [{"user_id": 448773145, "resource": "orders", "resource_id": 2072431494, "site_id": "MLA"}]
item['text'] = {"plain": "Hola leandro4"}

# item_pack={}
# item_pack['from'] = {'user_id': 445346519, 'email': 'test'}
# item['to'] = [{"user_id": 448773145}]
# item['text'] = 'Hola leandro2'

print(item)
res = mercadolibre.post_with_token('/messages', item)
print(res.json())
