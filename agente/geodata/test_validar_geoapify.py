import copy
import hashlib
import unittest
from validar_geoapify import reason, review

class AddressValidationTest(unittest.TestCase):
    def setUp(self):
        self.client = {'id': 'teste', 'endereco': 'AVENIDA SETE DE SETEMBRO, 00123', 'cidade': 'Sarandi', 'uf': 'RS', 'cep': '99560-000'}
        self.result = {'result_type': 'building', 'country_code': 'br', 'state_code': 'RS', 'city': 'Sarandi', 'street': 'Av. 7 de Setembro', 'housenumber': '123', 'lat': -27.94, 'lon': -52.92, 'rank': {k: 1 for k in ('confidence', 'confidence_city_level', 'confidence_street_level', 'confidence_building_level')}}
        address = ', '.join(self.client[k] for k in ('endereco', 'cidade', 'uf', 'cep')) + ', Brasil'
        self.entry = {'endereco_hash': hashlib.sha256(address.encode()).hexdigest(), 'resultados': [self.result]}

    def test_same_address_accepts_typographic_variants(self):
        self.assertIsNone(reason(self.client, self.result))

    def test_rejects_inferred_building_and_city_centroid(self):
        self.result['rank']['confidence_building_level'] = 0
        self.assertIsNotNone(reason(self.client, self.result))
        self.result['rank']['confidence_building_level'] = 1
        self.result['result_type'] = 'city'
        self.assertIsNotNone(reason(self.client, self.result))

    def test_rejects_wrong_city_number_street_and_specific_postcode(self):
        for key, value in [('city', 'Porto Alegre'), ('housenumber', '124'), ('street', 'Rua Outra')]:
            result = dict(self.result, **{key: value})
            self.assertIsNotNone(reason(self.client, result))
        self.client['cep'] = '99560-123'
        self.result['postcode'] = '99560-456'
        self.assertIsNotNone(reason(self.client, self.result))

    def test_known_branch_conflict_and_stale_cache_stay_pending(self):
        self.client['id'] = 'CLI-REAL-0023'
        self.assertIsNone(review(self.client, self.entry)[0])
        self.client['id'] = 'teste'
        self.client['endereco'] = 'Outra rua, 456'
        self.assertIsNone(review(self.client, self.entry)[0])

    def test_ambiguous_coordinates_stay_pending(self):
        alternate = copy.deepcopy(self.result)
        alternate['lat'] = -28
        self.entry['resultados'].append(alternate)
        self.assertIsNone(review(self.client, self.entry)[0])

if __name__ == '__main__':
    unittest.main()
