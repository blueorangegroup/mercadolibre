from mercadolibre.src import error_handler
from simplejson import errors


class InvoiceAttachedException(Exception):
    pass


def attach_invoice(meli, order_id, files):
    res = meli.upload(
        '/packs/{}/fiscal_documents'.format(order_id),
        files,
        {'access_token': meli.access_token}
    )
    try:
        error_handler.RestErrorHandler.handle_error(res)
        if not res.ok:
            message = res.json().get('message')
            if 'a file already exists' in message:
                raise InvoiceAttachedException("La orden {} ya tiene un adjunto de factura.".format(order_id))
            raise Exception(message)
        return res
    except errors.JSONDecodeError:
        if 'a file already exists' in res.text:
            raise InvoiceAttachedException("La orden {} ya tiene un adjunto de factura.".format(order_id))
        raise Exception("({}) {}".format(res.status_code, res.text))
