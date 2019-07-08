from unidecode import unidecode

from mercadolibre.src import error_handler


class Attachment(object):

    def __init__(self, name, attachment):
        self.name = name
        self.attachment = attachment


class Message(object):

    def __init__(self, seller_id, buyer_id, resource, resource_id, text):
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.resource = resource
        self.resource_id = resource_id
        self.text = text
        self.attachments = None

    def send_messages(self, meli_site):
        item = {
            'from': {'user_id': self.seller_id},
            'to': [{"user_id": self.buyer_id, "resource": self.resource,
                    "resource_id": self.resource_id}],
            'text': {"plain": self.text}
        }
        if self.attachments:
            attachments = []
            for attachment in self.attachments:
                attachment_file = {'file': (unidecode(attachment.name), attachment.attachment, "application/pdf")}
                response = meli_site.upload(
                    '/messages/attachments',
                    attachment_file,
                    {'access_token': meli_site.access_token}
                )

                if not response.ok:
                    raise Exception("Hubo un error al intentar subir el adjunto en mercadolibre: {}".format(
                        response.json().get('message')
                    ))

                attachments.append(response.json().get('id'))

            item['attachments'] = attachments

        res = meli_site.post_with_token('/messages', item)
        error_handler.RestErrorHandler.handle_error(res)
