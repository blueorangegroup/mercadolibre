from mercadolibre.src import error_handler, shipping as ml_shipping


def get_order_from_resource(meli, resource):
    return meli.get_with_token(resource)


class Buyer(object):

    def __init__(self, buyer_id, nickname, email):
        self.buyer_id = buyer_id
        self.nickname = nickname
        self.email = email

    @staticmethod
    def create_buyer_from_dic(dic):
        buyer = Buyer(dic.get('id'), dic.get('nickname'), dic.get('email'))
        buyer.phone = ' '.join([dic.get('phone').get('area_code'), dic.get('phone').get('number')])
        buyer.name = ' '.join([dic.get('first_name'), dic.get('last_name')])
        billing_info = dic.get('billing_info', {})
        buyer.doc_number = billing_info.get('doc_number')
        buyer.doc_type = billing_info.get('doc_type')
        return buyer


class OrderItem(object):

    def __init__(self, item_id, quantity, unit_price):
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price

    @staticmethod
    def create_items_from_dic(dic):
        return [OrderItem(item.get('item').get('id'), item.get('quantity'), item.get('unit_price')) for item in dic]


class Order(object):

    def __init__(self, order_id, currency_id, status, buyer, items, shipping):
        self.order_id = order_id
        self.buyer = buyer
        self.currency_id = currency_id
        self.status = status
        self.items = items
        self.shipping = shipping

    @staticmethod
    def get_sale_info_from_resource(meli, resource):
        res = get_order_from_resource(meli, resource)
        error_handler.RestErrorHandler.handle_error(res)
        res = res.json()
        buyer = Buyer.create_buyer_from_dic(res.get('buyer'))
        items = OrderItem.create_items_from_dic(res.get('order_items'))
        shipping = ml_shipping.Shipping.create_shipping_from_dic(res.get('shipping'))
        return Order(res.get('id'), res.get('currency_id'), res.get('status'), buyer, items, shipping)
