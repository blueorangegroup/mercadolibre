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
            cause_messages = []
            cause_refs = []
            for c in cause:
                cause_messages.append(c.get('message', ''))
                code = c.get('code', '')
                references = c.get('references', [])
                if references or code:
                    ref = ', '.join(references) if references else ''
                    parts = [p for p in [ref, code] if p]
                    cause_refs.append(' - '.join(parts))
            full_message += "\n{}".format('\n'.join(cause_messages))
            if cause_refs:
                full_message += "\nCódigo y referencia de error: {}".format('\n'.join(cause_refs))
        if response.status_code in [401, 403]:
            raise InvalidTokenException(
                'El token que está tratando de utilizar es inválido o no tiene los permisos necesarios para hacer esta acción. Error: {}'.format(
                    full_message
                )
            )
        elif not response.ok:
            raise Exception("Error: {}".format(full_message))
