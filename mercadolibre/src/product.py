from . import error_handler

NOT_FOUND_STATUS = 404


def get_publication_from_id(meli, product_id):
    return meli.get_with_token('/items/{}?include_attributes=all'.format(product_id))


def get_publication_description_from_id(meli, product_id):
    return meli.get_with_token('/items/{}/description'.format(product_id))


class Product(object):

    def __init__(self, title=None, category_id=None, price=None, currency_id=None,
                 available_quantity=None, listing_type_id=None):
        self.title = title
        self.category_id = category_id
        self.price = price
        self.currency_id = currency_id
        self.available_quantity = available_quantity
        self.listing_type_id = listing_type_id
        self.buying_mode = None
        self.condition = None
        self.video_id = None
        self.pictures = []
        self.shipping_mode = None
        self.product_id = None
        self.user_product_id = None
        self.permalink = None
        self.description = None
        self.variations = []
        self.attributes = []
        self.sku = None
        self.status = None
        self.installments_campaign_name = None
        self.family_name = None

    @staticmethod
    def get_product_from_id(meli, product_id):
        res = get_publication_from_id(meli, product_id)
        error_handler.RestErrorHandler.handle_error(res)
        description = get_publication_description_from_id(meli, product_id)
        # La API de Mercadolibre devuelve 404 si se hace get a la descripción de una publicación que no tiene, así que
        # para evitar que se corte un flujo por eso hago manejo de errores solamente si no devolvió 404 (se espera que
        # en caso de solicitar una publicación inexistente el error sea atrapado por el handler anterior, que evalúa el
        # get al endpoint de items)
        if description.json().get('status') != NOT_FOUND_STATUS:
            error_handler.RestErrorHandler.handle_error(description)
            description = description.json().get('plain_text')
        else:
            description = False
        res = res.json()
        product = Product(res.get('title'), res.get('category_id'), res.get('price'), res.get('currency_id'),
                          res.get('available_quantity'), res.get('listing_type_id'))
        product.description = description
        product.buying_mode = res.get('buying_mode')
        product.condition = res.get('condition')
        product.video_id = res.get('video_id')
        product.pictures = res.get('pictures')
        product.shipping_mode = res.get('shipping', {}).get('mode')
        product.product_id = res.get('id')
        product.permalink = res.get('permalink')
        product.status = res.get('status')
        product.family_name = res.get('family_name')
        product.sku = None
        for attribute in res.get('attributes', []):
            if attribute.get('id') == 'SELLER_SKU':
                product.sku = attribute.get('value_name')
                break
        if not product.sku:
            product.sku = res.get('seller_custom_field')

        if res.get('variations'):
            variations = []
            for variation in res.get('variations'):
                new_variation = Variant()
                new_variation.product_id = variation.get('id')
                new_variation.sku = None
                for attribute in variation.get('attributes'):
                    if attribute.get('id') == 'SELLER_SKU':
                        new_variation.sku = attribute.get('value_name')
                        break
                if not new_variation.sku:
                    new_variation.sku = variation.get('seller_custom_field')
                variations.append(new_variation)
            product.variations = variations

        if res.get('sale_terms'):
            for term in res.get('sale_terms'):
                if term.get('id') == 'INSTALLMENTS_CAMPAIGN':
                    product.installments_campaign_name = term.get('value_name')
                    break
        return product

    def get_body(self):
        body = {
            'title': self.title,
            'category_id': self.category_id,
            'price': self.price,
            'listing_type_id': self.listing_type_id,
            'buying_mode': self.buying_mode,
            'condition': self.condition,
            'video_id': self.video_id,
            'pictures': self.pictures,
            'available_quantity': self.available_quantity,
            'family_name': self.family_name,
            'description': {
                'plain_text': self.description,
            }
        }
        if self.shipping_mode:
            body['shipping'] = {
                'mode': self.shipping_mode
            }

        attributes = list(self.attributes) if self.attributes else []

        # El SKU se mantiene en el atributo SELLER_SKU (forma correcta según la
        # API de Mercado Libre). seller_custom_field queda como uso interno del
        # vendedor y se completa por compatibilidad.
        if self.sku:
            body['seller_custom_field'] = self.sku
            if not any(attr.get('id') == 'SELLER_SKU' for attr in attributes):
                attributes.append({'id': 'SELLER_SKU', 'value_name': self.sku})

        if attributes:
            body['attributes'] = attributes

        return body

    def publish(self, meli):
        body = self.get_body()
        description = body.get('description', {}).get('plain_text', '')
        body.update({
            'currency_id': self.currency_id
        })
        if self.variations:
            body['variations'] = [
                {
                    'attribute_combinations': [
                        {
                            "name": attribute.attribute_id,
                            "value_name": attribute.value,
                        }
                        for attribute in variant.attribute_combinations
                    ],
                    'available_quantity': variant.available_quantity,
                    'price': variant.price,
                    'attributes': [
                        {
                            "id": "SELLER_SKU",
                            "value_name": variant.sku,
                        }
                    ] + variant.attributes,
                    'picture_ids': variant.pictures
                }
                for variant in self.variations
            ]

        response = meli.post_with_token('/items', body)
        error_handler.RestErrorHandler.handle_error(response)
        res = response.json()
        self.product_id = res.get('id')

        self.update_description(meli, description)

        # Tenemos que mapear el id de la variante matcheando por SKU
        if self.variations:
            for variation in self.variations:
                for meli_variation in res.get('variations'):
                    for meli_attribute in meli_variation.get('attributes'):
                        if meli_attribute.get('id') == 'SELLER_SKU' \
                                and meli_attribute.get('value_name') == variation.sku:
                            variation.product_id = meli_variation.get('id')

        self.permalink = res.get('permalink')

    def update_description(self, meli, description):
        if description:
            response = meli.put_with_token(
                '/items/{}/description'.format(self.product_id),
                {'plain_text': description}
            )
            error_handler.RestErrorHandler.handle_error(response)

    def update(self, meli):
        body = self.get_body()
        # Si la publicación tiene family_name puesto no actualizo el title, ya que va a dar error
        if body.get('family_name'):
            body.pop('title')
            body.pop('family_name')
        # La descripción se actualiza con un put aislado
        description = body.get('description', {}).get('plain_text', '')
        body.pop('description')
        # El manejo de fotos es a parte
        body.pop('pictures')
        # Estos campos no se pueden sincronizar en publicaciones con ventas.
        body.pop('category_id')
        body.pop('buying_mode')
        body.pop('condition')
        body.pop('listing_type_id')
        if self.variations:
            # Si estoy actualizando una publicación con variantes, no debo enviar el price (se informa en las variantes)
            if len(self.variations) > 1:
                body.pop('price')
            body.pop('available_quantity')
            variations = []
            for variant in self.variations:
                if variant.product_id:
                    variant_attrs = {
                        'price': variant.price,
                        'available_quantity': variant.available_quantity,
                        'id': variant.product_id,
                    }
                elif variant.attribute_combinations:
                    # Caso de variacion nueva que no existia
                    variant_attrs = {
                        'attribute_combinations': [
                            {
                                "name": attribute.attribute_id,
                                "value_name": attribute.value,
                            }
                            for attribute in variant.attribute_combinations
                        ],
                        'available_quantity': variant.available_quantity,
                        'price': variant.price,
                        'attributes': [
                                          {
                                              "id": "SELLER_SKU",
                                              "value_name": variant.sku,
                                          }
                                      ] + variant.attributes,
                        'picture_ids': variant.pictures
                    }
                else:
                    continue
                variations.append(variant_attrs)

            body['variations'] = variations

        try:
            self.update_description(meli, description)
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)
        except Exception as e:
            raise Exception(e.args[0])

        for variation in self.variations:
            for meli_variation in response.json().get('variations'):
                for meli_attribute in meli_variation.get('attributes'):
                    if meli_attribute.get('id') == 'SELLER_SKU' \
                            and meli_attribute.get('value_name') == variation.sku:
                        variation.product_id = meli_variation.get('id')

    def update_pictures(self, meli):
        body = {'pictures': self.pictures}
        if self.variations:
            variations = []
            for variation in self.variations:
                variations.append({'id': variation.product_id, 'picture_ids': variation.pictures})
                for picture in variation.pictures:
                    body['pictures'].append({'id': picture})
            body['variations'] = variations

        response = meli.put_with_token('/items/{}'.format(self.product_id), body)
        error_handler.RestErrorHandler.handle_error(response)

    def update_status(self, meli, state):
        body = {
            'status': state
        }
        response = meli.put_with_token('/items/{}'.format(self.product_id), body)
        error_handler.RestErrorHandler.handle_error(response)

    def update_stock(self, meli):
        if not self.product_id:
            raise Exception("El producto a actualizar no tiene ID")

        if self.variations:
            variations = []
            for variation in self.variations:
                if not variation.product_id:
                    raise Exception("El producto a actualizar no tiene ID")
                vals = {'id': variation.product_id}
                vals['available_quantity'] = variation.available_quantity or 0.0

                variations.append(vals)

            body = {
                'variations': variations,
            }
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)
        else:
            body = {
                'available_quantity': self.available_quantity
            }
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)
    
    def update_hybrid_stock(self, meli):
        # CÓDIGO MUERTO: no tiene llamadores en los repos actuales. Quedó obsoleto
        # tras unificar la sincronización de stock de user-products en
        # update_seller_warehouse_stock / _update_user_product_stock, que ya
        # contempla el caso selling_address que este método manejaba. Conservado
        # por si existiera algún consumidor externo; eliminar al confirmar que no.
        if not self.product_id:
            raise Exception("El producto a actualizar no tiene ID")
        if not (self.variations or self.user_product_id):
            raise Exception("El producto a actualizar no tiene ID de usuario")
        if self.variations and not any(v.user_product_id for v in self.variations):
            raise Exception("No se informó ID de usuario en ninguna de las variantes del producto")

        if self.variations:
            for variation in self.variations:
                user_product_data = meli.get_with_token('/user-products/{}/stock'.format(variation.user_product_id))
                if not any(l['type'] == 'selling_address' for l in user_product_data.json().get('locations', [])):
                    continue
                header = {'x-version': user_product_data.headers['x-version']}
                body = {
                    'quantity': int(variation.available_quantity)
                }
                response = meli.put_with_token('/user-products/{}/stock/type/selling_address'.format(variation.user_product_id), body=body, extra_headers=header)
                if response.status_code != 204:
                    error_handler.RestErrorHandler.handle_error(response)
        else:
            user_product_data = meli.get_with_token('/user-products/{}/stock'.format(self.user_product_id))
            if not any(l['type'] == 'selling_address' for l in user_product_data.json().get('locations', [])):
                return
            header = {'x-version': user_product_data.headers['x-version']}
            body = {
                'quantity': int(self.available_quantity)
            }
            response = meli.put_with_token('/user-products/{}/stock/type/selling_address'.format(self.user_product_id), body=body, extra_headers=header)
            if response.status_code != 204:
                error_handler.RestErrorHandler.handle_error(response)

    def _update_user_product_stock(self, meli, user_product_id, quantity,
                                   can_write_selling_address=True):
        """
        Actualiza el stock de un user-product. Hace un GET para obtener la versión
        actual de stock (header x-version) y las locations existentes, detecta el
        tipo de location y arma el PUT correspondiente respetando los datos del
        GET, modificando únicamente el quantity. El header x-version es obligatorio
        (ML responde 400 si no se envía).

        Soporta dos tipos de ubicación actualizables por el vendedor:
        - selling_address: stock en el domicilio del vendedor, body {quantity}.
        - seller_warehouse: stock por depósito/nodo, body con locations. Solo se
          actualiza si existe exactamente una location, ya que no hay regla
          confiable para distribuir el stock total de Odoo entre varios nodos.

        Las locations de tipo meli_facility (stock alojado en Mercado Libre Full)
        no las gestiona el vendedor y se ignoran. Un user-product con SOLO
        meli_facility corresponde a una publicación Fulfillment pura: no hay nada
        que actualizar, se retorna False sin error. En cambio una publicación
        híbrida (Fulfillment con stock propio) trae además seller_warehouse, que
        sí se actualiza.

        La presencia de una location selling_address no alcanza para saber si el
        vendedor la puede escribir: una publicación Fulfillment pura puede
        arrastrar unidades congeladas en selling_address de antes de pasar a Full,
        y ML rechaza el PUT con un error de "solo fulfillment". Quién puede
        escribirla depende de la logística de la publicación, dato que la lib no
        tiene acá, así que lo informa el llamador en can_write_selling_address.
        El default es True para no cambiar el comportamiento de los llamadores que
        no lo informan. seller_warehouse NO depende de este flag: las
        publicaciones híbridas por depósito se actualizan siempre.

        Retorna True si actualizó stock, False si no había nada actualizable
        (Full pura). Si hay una location actualizable pero la actualización falla,
        lanza excepción (fail fast): no debe reportarse como actualizado algo que
        en realidad no se modificó.
        """
        user_product_data = meli.get_with_token('/user-products/{}/stock'.format(user_product_id))
        error_handler.RestErrorHandler.handle_error(user_product_data)

        locations = user_product_data.json().get('locations', [])
        header = {'x-version': user_product_data.headers['x-version']}

        if can_write_selling_address \
                and any(location.get('type') == 'selling_address' for location in locations):
            body = {'quantity': int(quantity)}
            response = meli.put_with_token(
                '/user-products/{}/stock/type/selling_address'.format(user_product_id),
                body=body,
                extra_headers=header,
            )
            if response.status_code != 204:
                error_handler.RestErrorHandler.handle_error(response)
            return True

        warehouse_locations = [
            location for location in locations
            if location.get('type') == 'seller_warehouse'
        ]
        # Sin seller_warehouse, y descartada arriba la selling_address escribible,
        # no hay stock gestionado por el vendedor: es una publicación Fulfillment
        # pura (solo meli_facility, o con selling_address congelada que ML no deja
        # tocar). No es un error, simplemente no hay nada que actualizar.
        # Retornamos False para que el llamador no lo cuente como publicación
        # sincronizada.
        if not warehouse_locations:
            return False
        # Sin regla de distribución para múltiples nodos no podemos actualizar de
        # forma confiable: fallamos en lugar de reportar un falso éxito.
        if len(warehouse_locations) > 1:
            raise Exception(
                "El user-product {} tiene múltiples ubicaciones seller_warehouse; "
                "no hay regla para distribuir el stock total".format(user_product_id)
            )

        location = warehouse_locations[0]
        body = {
            'locations': [
                {
                    'store_id': location.get('store_id'),
                    'network_node_id': location.get('network_node_id'),
                    'quantity': int(quantity),
                }
            ]
        }
        response = meli.put_with_token(
            '/user-products/{}/stock/type/seller_warehouse'.format(user_product_id),
            body=body,
            extra_headers=header,
        )
        if response.status_code != 204:
            error_handler.RestErrorHandler.handle_error(response)
        return True

    def update_seller_warehouse_stock(self, meli, can_write_selling_address=True):
        """
        Actualiza el stock de publicaciones cuyas unidades de stock se gestionan
        vía user-products (atributo user_product_id en el item o en cada
        variación). Detecta automáticamente el tipo de ubicación de stock
        (selling_address o seller_warehouse) y actualiza en consecuencia.

        can_write_selling_address informa si el vendedor puede escribir la
        location selling_address de esta publicación; ver
        _update_user_product_stock. Es opcional y su default preserva el
        comportamiento anterior.

        Retorna True si se actualizó al menos un stock, False si no había nada
        actualizable (p. ej. publicación Fulfillment pura, con stock solo en
        meli_facility). El llamador usa este retorno para no contar como
        sincronizada una publicación que en realidad no se modificó.
        """
        if not self.product_id:
            raise Exception("El producto a actualizar no tiene ID")
        if not (self.variations or self.user_product_id):
            raise Exception("El producto a actualizar no tiene ID de usuario")
        if self.variations and not any(v.user_product_id for v in self.variations):
            raise Exception("No se informó ID de usuario en ninguna de las variantes del producto")

        if self.variations:
            updated_any = False
            for variation in self.variations:
                if not variation.user_product_id:
                    continue
                # _update_user_product_stock retorna False para Full puras (solo
                # meli_facility): esas no cuentan como actualización real.
                updated = self._update_user_product_stock(
                    meli, variation.user_product_id, variation.available_quantity or 0,
                    can_write_selling_address=can_write_selling_address
                )
                updated_any = updated_any or updated
            # Si el guard de arriba pasó pero ninguna variante con user_product_id
            # tenía stock actualizable (todas Full puras o sin user_product_id), no
            # se actualizó nada.
            return updated_any
        else:
            return self._update_user_product_stock(
                meli, self.user_product_id, self.available_quantity or 0,
                can_write_selling_address=can_write_selling_address
            )

    def update_price(self, meli):
        if not self.product_id:
            raise Exception("El producto a actualizar no tiene ID")

        # Si no se informaron variaciones, consultamos la publicación en Mercado
        # Libre: puede tener variaciones aunque el llamador no las haya cargado
        # (caso típico: en Odoo la publicación no tiene variantes pero en ML sí).
        # La API de ML rechaza un PUT con 'price' a nivel item cuando la
        # publicación tiene variaciones, así que en ese caso replicamos el mismo
        # precio a todas las variaciones (omitir alguna la eliminaría).
        if not self.variations:
            remote_product = self.get_product_from_id(meli, self.product_id)
            if remote_product.variations:
                for variation in remote_product.variations:
                    variation.price = self.price
                self.variations = remote_product.variations

        if self.variations:
            variations = []
            for variation in self.variations:
                if not variation.product_id:
                    raise Exception("El producto a actualizar no tiene ID")
                vals = {'id': variation.product_id}
                vals['price'] = variation.price

                variations.append(vals)

            body = {
                'variations': variations,
            }
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)
        else:
            body = {
                'price': self.price
            }
            response = meli.put_with_token('/items/{}'.format(self.product_id), body)
            error_handler.RestErrorHandler.handle_error(response)

class Variant(object):

    def __init__(self, attribute_combinations=None, available_quantity=None, price=None, pictures=None, sku=None):
        self.attribute_combinations = attribute_combinations
        self.available_quantity = available_quantity
        self.price = price
        self.pictures = pictures
        self.sku = sku
        self.product_id = None
        self.user_product_id = None
        self.attributes = []


class AttributeCombination(object):

    def __init__(self, attribute_id, value):
        self.attribute_id = attribute_id
        self.value = value
