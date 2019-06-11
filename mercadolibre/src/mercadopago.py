from . import mercadolibre


class MercadoPago(mercadolibre.Mercadolibre):

    def post_payment(self, name, amount):
        return self.post_with_token("/checkout/preferences", body={'items':[{
            'title': name,
            'quantity': 1,
            'currency_id': 'ARS',
            'unit_price': amount,
        }]})
