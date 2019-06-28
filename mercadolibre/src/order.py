from mercadolibre.src import error_handler, utils, shipping as ml_shipping


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
            dic_item = item.get('item')
            meli_item = OrderItem(
                dic_item.get('id'),
                item.get('quantity'),
                item.get('unit_price'),
                dic_item.get('seller_sku') or dic_item.get('seller_custom_field')
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
        self.date_closed = None

    @staticmethod
    def get_sale_info_from_resource(meli, resource):
        res = get_order_from_resource(meli, resource)
        error_handler.RestErrorHandler.handle_error(res)
        res = res.json()
        buyer = Buyer.create_buyer_from_dic(res.get('buyer'))
        items = OrderItem.create_items_from_dic(res.get('order_items'))
        shipping = ml_shipping.Shipping.create_shipping_from_id(meli, res.get('shipping', {}).get('id'))
        order = Order(res.get('id'), res.get('currency_id'), res.get('status'), buyer, items, shipping)
        order.pack_id = res.get('pack_id')
        order.total_amount = res.get('total_amount') or 0.0
        order.shipping_amount = shipping.cost or 0.0
        order.paid_amount = res.get('paid_amount') or 0.0
        if res.get('date_closed'):
            order.date_closed = utils.iso8601_to_datetime_utc(res.get('date_closed'))
        # payments = res.get('payments')
        # # Tomamos como fecha de cierre de la orden la fecha del último pago aprobado
        # if payments and any(payment.get('date_approved') for payment in payments):
        #     order.date_closed = max(
        #         utils.iso8601_to_datetime_utc(payment.get('date_approved')) for payment in res.get('payments')
        #         if payment.get('date_approved')
        #     )
        return order
