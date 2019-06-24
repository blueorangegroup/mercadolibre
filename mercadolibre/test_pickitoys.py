from pprint import pprint

from src import mercadolibre, mercadolibre_site, order, product, category

mercadolibre = mercadolibre.Mercadolibre(
    '6889730284272595',
    'RzYpozRRwjWm03kJZ9y4KrHnwi0wsepv',
    'APP_USR-6889730284272595-062105-57eea12f5ad79138b18d8aa38571bb9a-163123417'
)


# {'id': 445346519, 'nickname': 'TETE8847199', 'password': 'qatest7226', 'site_status': 'active', 'email': 'test_user_16828405@testuser.com'}

# ORDENES
res = order.get_order_from_resource(mercadolibre, '/orders/2057239278')

#res = mercadolibre.get_with_token('/items/MLA726610598')

# PUBLICACIONES
#res = product.get_publication_from_id(mercadolibre, 'MLA793185853')

#res = category.get_main_categories(mercadolibre_site)

#print(res)
pprint(res.json())
#pprint(res.json().get('total_amount_with_shipping'))
#pprint(res.json().get('shipping'))
