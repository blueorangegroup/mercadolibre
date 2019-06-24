

def get_shippings_tags(meli, shipping_ids):
    response = meli.get('/shipment_labels', {'access_token': meli.access_token, 'shipment_ids': shipping_ids})
    return response.content


class Shipping(object):

    def __init__(self, shipping_id=None):
        self.shipping_id = shipping_id
        self.status = None
        self.shipment_type = None
        self.address_line = None
        self.zip_code = None
        self.city = None
        self.state = None
        self.cost = None
        self.logistic_type = None
        self.shipping_method_name = None

    @staticmethod
    def create_shipping_from_dic(dic):
        address = dic.get('receiver_address', {})
        shipping = Shipping(
            dic.get('id'),
        )
        shipping.status = dic.get('status')
        shipping.shipment_type = dic.get('shipment_type')
        shipping.address_line = address.get('address_line')
        shipping.zip_code = address.get('zip_code')
        shipping.city = address.get('city', {}).get('name')
        shipping.state = address.get('state', {}).get('name')
        shipping.cost = dic.get('cost')
        shipping.logistic_type = dic.get('logistic_type')
        shipping.shipping_method_name = dic.get('shipping_option', {}).get('name')
        return shipping

