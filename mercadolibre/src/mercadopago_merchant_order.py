def get_merchant_order_data(meli, order_id):
    return meli.get_with_token("/merchant_orders/%s" % order_id)
