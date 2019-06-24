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
        buyer.phone = ' '.join([dic.get('phone', {}).get('area_code') or '', dic.get('phone', {}).get('number') or ''])
        buyer.name = ' '.join([dic.get('first_name') or '', dic.get('last_name') or ''])
        billing_info = dic.get('billing_info', {})
        buyer.doc_number = billing_info.get('doc_number')
        buyer.doc_type = billing_info.get('doc_type')
        return buyer


class OrderItem(object):

    def __init__(self, item_id, quantity, unit_price, sku):
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.sku = sku

    @staticmethod
    def create_items_from_dic(dic):
        items = []
        for item in dic:
            meli_item = OrderItem(
                item.get('item').get('id'),
                item.get('quantity'),
                item.get('unit_price'),
                item.get('item').get('seller_sku')
            )
            items.append(meli_item)
        return items


class Order(object):

    def __init__(self, order_id, currency_id, status, buyer, items, shipping):
        self.order_id = order_id
        self.buyer = buyer
        self.currency_id = currency_id
        self.status = status
        self.items = items
        self.shipping = shipping
        self.pack_id = None
        self.total_amount = None
        self.shipping_amount = None
        self.paid_amount = None

    @staticmethod
    def get_sale_info_from_resource(meli, resource):
        res = get_order_from_resource(meli, resource)
        error_handler.RestErrorHandler.handle_error(res)
        res = res.json()
        buyer = Buyer.create_buyer_from_dic(res.get('buyer'))
        items = OrderItem.create_items_from_dic(res.get('order_items'))
        shipping = ml_shipping.Shipping.create_shipping_from_dic(res.get('shipping'))
        order = Order(res.get('id'), res.get('currency_id'), res.get('status'), buyer, items, shipping)
        order.pack_id = res.get('pack_id')
        order.total_amount = res.get('total_amount') or 0.0
        order.shipping_amount = shipping.cost or 0.0
        order.paid_amount = res.get('paid_amount') or 0.0
        return order
