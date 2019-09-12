def get_merchant_order_data(mpago, order_id):
    return mpago.get_with_token("/merchant_orders/%s" % order_id)
