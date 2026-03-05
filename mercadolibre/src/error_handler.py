# -*- encoding: utf-8 -*-


class InvalidTokenException(Exception):
    pass


class RestErrorHandler:

    @staticmethod
    def handle_error(response):
        response_json = response.json()
        message = response_json.get('message')
        full_message = message
        cause = response_json.get('cause', []) or []
        if cause:
            full_message += "\n{}".format(
                '\n'.join([c.get('message') for c in cause])
            )
        if response.status_code in [401, 403]:
            raise InvalidTokenException(
                'El token que está tratando de utilizar es inválido o no tiene los permisos necesarios para hacer esta acción. Error: {}'.format(
                    full_message
                )
            )
        elif not response.ok:
            raise Exception("Error: {}".format(full_message))
