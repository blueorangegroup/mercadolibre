# -*- encoding: utf-8 -*-
"""
Sincronización de stock de user-products: qué location se escribe según lo que
devuelve el GET y según si el vendedor puede escribir selling_address.

Los cuatro escenarios reales de Mercado Libre que tiene que distinguir:

- Full pura: solo meli_facility. No hay nada que el vendedor administre.
- Full pura con remanente: meli_facility + selling_address con unidades viejas
  que ML dejó congeladas. La location existe pero ML rechaza el PUT.
- Coexistencia Full + Flex: meli_facility + selling_address escribible.
- Híbrida por depósito: meli_facility + seller_warehouse. No depende del tag.
"""

import unittest

from mercadolibre.src import product as product_api


class FakeResponse(object):

    def __init__(self, status_code=200, body=None, headers=None):
        self.status_code = status_code
        self.ok = status_code < 400
        self._body = body if body is not None else {}
        self.headers = headers if headers is not None else {}

    def json(self):
        return self._body


class FakeMeli(object):
    """Cliente de Mercado Libre mínimo: registra las llamadas y devuelve lo pautado."""

    def __init__(self, locations, x_version='v-1', put_status=204):
        self._locations = locations
        self._x_version = x_version
        self._put_status = put_status
        self.gets = []
        self.puts = []

    def get_with_token(self, uri, params=None):
        self.gets.append(uri)
        return FakeResponse(
            body={'locations': self._locations},
            headers={'x-version': self._x_version},
        )

    def put_with_token(self, uri, body=None, extra_headers=None):
        self.puts.append({'uri': uri, 'body': body, 'headers': extra_headers})
        return FakeResponse(status_code=self._put_status, body={})


SELLING_ADDRESS = {'type': 'selling_address', 'quantity': 15}
MELI_FACILITY = {'type': 'meli_facility', 'quantity': 5}
SELLER_WAREHOUSE = {
    'type': 'seller_warehouse',
    'store_id': 'ST-1',
    'network_node_id': 'NN-1',
    'quantity': 3,
}


class TestUserProductStock(unittest.TestCase):

    def _product(self, user_product_id='MLAU3883726087', quantity=20):
        meli_product = product_api.Product()
        meli_product.product_id = 'MLA3283330096'
        meli_product.user_product_id = user_product_id
        meli_product.available_quantity = quantity
        return meli_product

    # -- Full pura con remanente en selling_address: el caso del bug -----------

    def test_fulfillment_only_publication_does_not_write_the_frozen_selling_address(self):
        """
        La location selling_address existe con unidades congeladas de antes, pero
        la publicación es Full pura: ML rechaza el PUT. No se escribe nada.
        """
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        updated = self._product().update_seller_warehouse_stock(
            meli, can_write_selling_address=False
        )

        self.assertFalse(updated)
        self.assertEqual(meli.puts, [])

    def test_fulfillment_only_publication_reads_the_stock_only_once(self):
        """Un solo GET y ningún PUT: no se gasta cuota en una publicación que no se puede tocar."""
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        self._product().update_seller_warehouse_stock(meli, can_write_selling_address=False)

        self.assertEqual(len(meli.gets), 1)

    # -- Coexistencia Full + Flex: selling_address sí se escribe ---------------

    def test_a_seller_that_can_write_selling_address_updates_it(self):
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        updated = self._product().update_seller_warehouse_stock(
            meli, can_write_selling_address=True
        )

        self.assertTrue(updated)
        self.assertEqual(len(meli.puts), 1)
        self.assertIn('/stock/type/selling_address', meli.puts[0]['uri'])
        self.assertEqual(meli.puts[0]['body'], {'quantity': 20})

    def test_the_put_sends_the_version_returned_by_the_get(self):
        """Sin el header x-version ML responde 400."""
        meli = FakeMeli([SELLING_ADDRESS], x_version='v-42')

        self._product().update_seller_warehouse_stock(meli)

        self.assertEqual(meli.puts[0]['headers'], {'x-version': 'v-42'})

    # -- Híbrida por depósito: seller_warehouse no depende del tag -------------

    def test_the_warehouse_stock_is_updated_even_when_selling_address_is_not_writable(self):
        """
        Las publicaciones híbridas (fulfillment con depósito propio) se actualizan
        por seller_warehouse. Ese camino no depende de que el vendedor pueda
        escribir selling_address: es el fix de las híbridas, no se toca.
        """
        meli = FakeMeli([SELLER_WAREHOUSE, MELI_FACILITY])

        updated = self._product().update_seller_warehouse_stock(
            meli, can_write_selling_address=False
        )

        self.assertTrue(updated)
        self.assertEqual(len(meli.puts), 1)
        self.assertIn('/stock/type/seller_warehouse', meli.puts[0]['uri'])
        self.assertEqual(meli.puts[0]['body'], {
            'locations': [{'store_id': 'ST-1', 'network_node_id': 'NN-1', 'quantity': 20}],
        })

    def test_the_warehouse_stock_is_updated_when_there_is_no_selling_address(self):
        meli = FakeMeli([SELLER_WAREHOUSE, MELI_FACILITY])

        updated = self._product().update_seller_warehouse_stock(meli)

        self.assertTrue(updated)
        self.assertIn('/stock/type/seller_warehouse', meli.puts[0]['uri'])

    # -- Full pura sin remanente ----------------------------------------------

    def test_a_publication_with_stock_only_in_full_has_nothing_to_update(self):
        meli = FakeMeli([MELI_FACILITY])

        updated = self._product().update_seller_warehouse_stock(meli)

        self.assertFalse(updated)
        self.assertEqual(meli.puts, [])

    # -- Varios nodos: no hay regla de distribución, falla ---------------------

    def test_several_warehouse_locations_fail_instead_of_reporting_a_false_success(self):
        meli = FakeMeli([
            dict(SELLER_WAREHOUSE, store_id='ST-1'),
            dict(SELLER_WAREHOUSE, store_id='ST-2'),
        ])

        with self.assertRaises(Exception):
            self._product().update_seller_warehouse_stock(meli, can_write_selling_address=False)

    # -- Retrocompatibilidad: la lib la comparten todas las versiones de Odoo --

    def test_the_flag_is_optional_and_defaults_to_the_previous_behaviour(self):
        """
        Los módulos de 12.0 a 18.0 llaman update_seller_warehouse_stock(meli) sin
        el flag. Sin argumento tiene que escribir selling_address como siempre.
        """
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        updated = self._product().update_seller_warehouse_stock(meli)

        self.assertTrue(updated)
        self.assertIn('/stock/type/selling_address', meli.puts[0]['uri'])

    def test_the_internal_helper_also_defaults_to_the_previous_behaviour(self):
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        updated = self._product()._update_user_product_stock(meli, 'MLAU3883726087', 7)

        self.assertTrue(updated)
        self.assertEqual(meli.puts[0]['body'], {'quantity': 7})

    # -- Variaciones -----------------------------------------------------------

    def _product_with_variations(self, quantities):
        meli_product = product_api.Product()
        meli_product.product_id = 'MLA3283330096'
        variations = []
        for index, quantity in enumerate(quantities):
            variation = product_api.Variant()
            variation.product_id = 'VAR-{}'.format(index)
            variation.user_product_id = 'MLAU-{}'.format(index)
            variation.available_quantity = quantity
            variations.append(variation)
        meli_product.variations = variations
        return meli_product

    def test_the_flag_reaches_every_variation(self):
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        updated = self._product_with_variations([4, 6]).update_seller_warehouse_stock(
            meli, can_write_selling_address=False
        )

        self.assertFalse(updated)
        self.assertEqual(meli.puts, [])

    def test_variations_update_their_own_quantity(self):
        meli = FakeMeli([SELLING_ADDRESS, MELI_FACILITY])

        updated = self._product_with_variations([4, 6]).update_seller_warehouse_stock(meli)

        self.assertTrue(updated)
        self.assertEqual(
            [put['body'] for put in meli.puts],
            [{'quantity': 4}, {'quantity': 6}],
        )


if __name__ == '__main__':
    unittest.main()
