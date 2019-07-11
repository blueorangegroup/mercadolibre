from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category

mercadolibre = mercadolibre.Mercadolibre(
    '6889730284272595',
    'RzYpozRRwjWm03kJZ9y4KrHnwi0wsepv',
    'APP_USR-5615248823896035-071012-42dbdec18090bd737f026c16415798bb-163123417'
)


#res = mercadolibre.get_with_token('/users/163123417/items/search?sku=LOL0007')
#res = mercadolibre.get_with_token('/users/163123417/items/search?seller_sku=RAIN0001&sub_status=out_of_stock')

#pprint(res.json())
#res = mercadolibre.get_with_token(
#                '/items?ids={}&include_attributes=all'.format(','.join(res.json().get('results')))
#            )
#pprint(res.json())

# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
#res = order.get_order_from_resource(mercadolibre, '/orders/2066509064')
res = mercadolibre.get_with_token('/shipments/28014349147')

#res = mercadolibre.get_with_token('/items/MLA726610598')

# PUBLICACIONES
#res = product.get_publication_from_id(mercadolibre, 'MLA793185853')

#res = category.get_main_categories(mercadolibre_site)
#res = mercadolibre.get_with_token('/users/163123417/items/search?sku=FURB0001CELESTE&status=active')
#res = mercadolibre.get_with_token('/users/163123417/items/search?sku=PEPP0008')
#MLA641452315

#print(res)
#pprint(res.json())
#pprint(res.json().get('order_items')[0].get('item'))

#for publication in res.json().get('results', {}):
    #res = mercadolibre.get_with_token('/items/{}?include_attributes=all'.format(publication))
    #print(res)
    #pprint(res.json())

#pprint(res.json().get('total_amount_with_shipping'))
#pprint(res.json().get('shipping'))
pprint(res.json())