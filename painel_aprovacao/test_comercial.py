import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from comercial_api import Commercial, write_json


class CommercialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.s = Commercial(Path(self.tmp.name))
        self.clients = [{'id': 'a', 'nome': 'Empresa de teste', 'endereco': 'Rua A, 123', 'cidade': 'Sarandi', 'uf': 'RS', 'cep': '99560000', 'lat': -27.94, 'lon': -52.92, 'geolocalizacao': {'status': 'localizado'}}, {'id': 'b', 'nome': 'Pendente', 'endereco': 'Rua A, 123', 'cidade': 'Sarandi', 'uf': 'RS', 'cep': '99560000', 'geolocalizacao': {'status': 'pendente'}}]
        write_json(self.s.base, self.clients)
        write_json(self.s.crm, [{'id': 'l', 'empresa': 'Empresa de teste', 'fase': 'novo'}])

    def test_planned_contact_not_counted_as_performed(self):
        self.s.mutate('salvar-contato', {'id': 'l', 'data': '2026-09-22', 'acao': 'Retornar'})
        self.assertEqual(self.s.state()['eventos'], [])
        self.s.mutate('salvar-contato', {'id': 'l', 'data': '', 'acao': '', 'realizado': True, 'nota': 'Conversamos'})
        self.assertEqual(self.s.state()['eventos'][0]['tipo'], 'contato')
        self.assertEqual(self.s.state()['contatos']['l']['ultima_nota'], 'Conversamos')

    def test_visit_rejects_pending_and_duplicate_and_records_once(self):
        for stops in [[{'id': 'b', 'hora': '09:00'}], [{'id': 'a', 'hora': '09:00'}, {'id': 'a', 'hora': '10:00'}]]:
            with self.assertRaises(ValueError):
                self.s.mutate('salvar-visita', {'data': '2026-09-22', 'paradas': stops})
        self.s.mutate('salvar-visita', {'data': '2026-09-22', 'paradas': [{'id': 'a', 'hora': '09:00'}]})
        ident = self.s.state()['visitas'][0]['id']
        for _ in range(2):
            self.s.mutate('concluir-visita', {'plano': ident, 'id': 'a'})
        self.assertEqual(len(self.s.state()['eventos']), 1)

    def test_proposal_lifecycle_and_invalid_money(self):
        body = {'cliente_id': 'a', 'validade': '2026-10-01', 'condicoes': 'Mensal', 'itens': [{'descricao': 'ERP', 'tipo': 'mensal', 'valor': 100}]}
        invalid = copy.deepcopy(body)
        invalid['itens'][0]['valor'] = float('nan')
        with self.assertRaises(ValueError):
            self.s.mutate('salvar-proposta', invalid)
        self.s.mutate('salvar-proposta', body)
        self.assertEqual(self.s.state()['eventos'], [])
        ident = self.s.state()['propostas'][0]['id']
        with self.assertRaises(ValueError):
            self.s.mutate('status-proposta', {'id': ident, 'status': 'aceita'})
        for status in ['apresentada', 'aceita']:
            self.s.mutate('status-proposta', {'id': ident, 'status': status})
        self.assertEqual([x['tipo'] for x in self.s.state()['eventos']], ['proposta', 'venda'])

    def test_address_preview_does_not_write_and_stale_apply_rejected(self):
        r = {'result_type': 'building', 'country_code': 'br', 'state_code': 'RS', 'city': 'Sarandi', 'street': 'Rua A', 'housenumber': '123', 'lat': -27.94, 'lon': -52.92, 'rank': {k: 1 for k in ['confidence', 'confidence_city_level', 'confidence_street_level', 'confidence_building_level']}}
        before = self.s.base.read_bytes()
        with patch('comercial_api.api_key', return_value='test'), patch('comercial_api.fetch', return_value=[r]):
            result = self.s.preview({'id': 'b', 'endereco': 'Rua A, 123', 'cidade': 'Sarandi', 'uf': 'RS', 'cep': '99560000'})
        self.assertEqual(before, self.s.base.read_bytes())
        body = {'token': result['token'], 'indice': 0, 'confirmado': False}
        with self.assertRaises(ValueError):
            self.s.mutate('aplicar-endereco', body)
        body['confirmado'] = True
        self.s.mutate('aplicar-endereco', body)
        self.assertEqual(self.s.data()['clientes'][1]['geolocalizacao']['status'], 'localizado')
        with self.assertRaises(ValueError):
            self.s.mutate('aplicar-endereco', body)

    def test_invalid_record_does_not_destroy_existing_data(self):
        self.s.mutate('salvar-contato', {'id': 'l', 'data': '2026-09-22', 'acao': 'Retornar'})
        before = self.s.file.read_bytes()
        with self.assertRaises(ValueError):
            self.s.mutate('salvar-contato', {'id': 'inexistente', 'data': '', 'acao': ''})
        self.assertEqual(before, self.s.file.read_bytes())


if __name__ == '__main__':
    unittest.main()
