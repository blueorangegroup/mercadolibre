from mercadolibre.src import error_handler


def attach_invoice(meli, order_id, files):
    res = meli.upload(
        '/packs/{}/fiscal_documents'.format(order_id),
        files,
        {'access_token': meli.access_token}
    )
    error_handler.RestErrorHandler.handle_error(res)
    return res
