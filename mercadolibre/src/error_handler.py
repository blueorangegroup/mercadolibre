# -*- encoding: utf-8 -*-


class InvalidTokenException(Exception):
    pass


class RestErrorHandler:

    @staticmethod
    def handle_error(response):
        response_json = response.json()
        if response.status_code == 401:
            raise InvalidTokenException('El token que está tratando de utilizar es inválido')
        elif response.status_code != 200:
            message = response_json.get('message')
            raise Exception("Error: {}\n{}".format(
                message, '\n'.join([cause.get('message') for cause in response_json.get('cause', []) or []])
            ))
