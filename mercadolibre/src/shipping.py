

def get_shippings_tags(meli, shipping_ids):
    response = meli.get('/shipment_labels', {'access_token': meli.access_token, 'shipment_ids': shipping_ids})
    if not response.ok:
        raise Exception("Hubo un error al intentar descargar la(s) etiqueta(s)")
    return response.content


def get_shipping(meli, shipping_id):
    return meli.get_with_token('/shipments/{}'.format(shipping_id))


class Shipping(object):

    def __init__(self, shipping_id=None):
        self.shipping_id = shipping_id
        self.status = None
        self.address_line = None
        self.zip_code = None
        self.city = None
        self.state = None
        self.cost = None
        self.logistic_type = None
        self.shipping_method_name = None

    @staticmethod
    def create_shipping_from_id(meli, shipping_id):
        shipping = Shipping(shipping_id)
        try:
            dic = get_shipping(meli, shipping_id).json()
        except Exception:
            return shipping

        address = dic.get('receiver_address', {})
        shipping.status = dic.get('status')
        shipping.address_line = address.get('address_line')
        shipping.zip_code = address.get('zip_code')
        shipping.city = address.get('city', {}).get('name')
        shipping.state = address.get('state', {}).get('name')
        shipping.logistic_type = dic.get('logistic_type')
        shipping.cost = dic.get('shipping_option', {}).get('cost')
        shipping.shipping_method_name = dic.get('shipping_option', {}).get('name')
        return shipping
