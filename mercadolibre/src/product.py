from . import error_handler


class Product(object):

    def __init__(self, title, category_id, price, currency_id, available_quantity, listing_type_id):
        self.title = title
        self.category_id = category_id
        self.price = price
        self.currency_id = currency_id
        self.available_quantity = available_quantity
        self.listing_type_id = listing_type_id
        self.buying_mode = None
        self.condition = None
        self.video_id = None
        self.pictures = []
        self.product_id = None
        self.permalink = None
        self.description = None
        self.variations = []

    def publish(self, meli):
        body = {
            'title': self.title,
            'category_id': self.category_id,
            'price': self.price,
            'currency_id': self.currency_id,
            'available_quantity': self.available_quantity,
            'listing_type_id': self.listing_type_id,
            'buying_mode': self.buying_mode,
            'condition': self.condition,
            'video_id': self.video_id,
            'pictures': self.pictures,
            'description': self.description,
        }
        # Ejemplo de variantes
        # body['variations'] = [
        #     {'attribute_combinations': [
        #         {
        #             'name': 'Color',
        #             'value_id': '52049',
        #             'value_name': 'Negro'
        #         }
        #     ],
        #     'price': 11,
        #     'available_quantity': 10,
        #     'picture_ids': ["https://www.artesanosdelaflor.com/1602-large_default/osito-peluche-te-amo-musical.jpg"]
        #     },
        #     {'attribute_combinations': [
        #         {
        #             'name': 'Color',
        #             'value_id': '52005',
        #             'value_name': 'Marrón'
        #         }
        #     ],
        #         'price': 11,
        #         'available_quantity': 3,
        #         'picture_ids': ["https://pbs.twimg.com/profile_images/993967511099068416/F3HK-M-4_400x400.jpg"]
        #     },
        # ]
        response = meli.post_with_token('/items', body)
        error_handler.RestErrorHandler.handle_error(response)
        res = response.json()
        self.product_id = res.get('id')
        self.permalink = res.get('permalink')

    def update_status(self, meli, state):
        body = {
            'status': state
        }
        response = meli.put_with_token('/items/{}'.format(self.product_id), body)
        error_handler.RestErrorHandler.handle_error(response)

    def update(self, meli):
        if not self.product_id:
            raise Exception("El producto a actualizar no tiene ID")
        body = {
            'available_quantity': self.available_quantity
        }
        response = meli.put_with_token('/items/{}'.format(self.product_id), body)
        error_handler.RestErrorHandler.handle_error(response)
