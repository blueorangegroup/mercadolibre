from . import error_handler


def get_publication_from_id(meli, product_id):
    return meli.get_with_token('/items/{}/variations'.format(product_id))


class Product(object):

    def __init__(self, title=None, category_id=None, price=None, currency_id=None,
                 available_quantity=None, listing_type_id=None):
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
        self.shipping_mode = None
        self.product_id = None
        self.permalink = None
        self.description = None
        self.variations = []
        self.sku = None

    def get_body(self):
        return {
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
            'description': {
                'plain_text': self.description,
            }
        }

    def publish(self, meli):
        body = self.get_body()
        if self.shipping_mode:
            body['shipping'] = {
                'mode': self.shipping_mode
            }

        if self.sku:
            body['seller_custom_field'] = self.sku

        if self.variations:
            body['variations'] = [
                {
                    'attribute_combinations': [
                        {
                            "id": attribute.attribute_id,
                            "value_id": attribute.value,
                        }
                        for attribute in variant.attribute_combinations
                    ],
                    'available_quantity': variant.available_quantity,
                    'price': variant.price,
                    'attributes': [
                        {
                            "id": "SELLER_SKU",
                            "value_name": variant.sku,
                        }
                    ],
                    'picture_ids': variant.pictures
                }
                for variant in self.variations
            ]

        response = meli.post_with_token('/items', body)
        error_handler.RestErrorHandler.handle_error(response)
        res = response.json()
        self.product_id = res.get('id')

        # Tenemos que mapear el id de la variante matcheando por SKU
        if self.variations:
            for variation in self.variations:
                for meli_variation in res.get('variations'):
                    for meli_attribute in meli_variation.get('attributes'):
                        if meli_attribute.get('id') == 'SELLER_SKU' \
                                and meli_attribute.get('value_name') == variation.sku:
                            variation.product_id = meli_variation.get('id')

        self.permalink = res.get('permalink')

    def update_status(self, meli, state):
        body = {
            'status': state
        }
        response = meli.put_with_token('/items/{}'.format(self.product_id), body)
        error_handler.RestErrorHandler.handle_error(response)

    def update_stock(self, meli):
        if not self.product_id:
            raise Exception("El producto a actualizar no tiene ID")

        if self.variations:
            variations = []
            for variation in self.variations:
                if not variation.product_id:
                    raise Exception("El producto a actualizar no tiene ID")
                vals = {'id': variation.product_id}
                if variation.available_quantity:
                    vals['available_quantity'] = variation.available_quantity

                variations.append(vals)

            body = {
                'variations': variations,
            }
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)
        else:
            body = {
                'available_quantity': self.available_quantity
            }
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)


class Variant(object):

    def __init__(self, attribute_combinations=None, available_quantity=None, price=None, pictures=None, sku=None):
        self.attribute_combinations = attribute_combinations
        self.available_quantity = available_quantity
        self.price = price
        self.pictures = pictures
        self.sku = sku
        self.product_id = None


class AttributeCombination(object):

    def __init__(self, attribute_id, value):
        self.attribute_id = attribute_id
        self.value = value
