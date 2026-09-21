"""Regressões da central revisada, sem escrita no CRM."""
import json
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent / 'painel_aprovacao'

class CentralToolsTests(unittest.TestCase):
    def test_catalogue_targets(self):
        source = (ROOT / 'ferramentas.js').read_text(encoding='utf8')
        targets = re.findall(r'\[\s*"([\w-]+\.html(?:\?[^"\s]*)?)"', source)
        self.assertEqual(len(targets), 18)
        self.assertEqual(len(targets), len(set(targets)))
        for target in targets:
            self.assertTrue((ROOT / target.split('?')[0]).is_file(), target)

    def test_every_old_target_has_a_decision(self):
        original = json.loads((ROOT / 'qa/ferramentas-inventario.json').read_text(encoding='utf8'))
        decisions = json.loads((ROOT / 'qa/ferramentas-decisoes.json').read_text(encoding='utf8'))
        retained = {'crm.html','radar_clientes.html','calendario.html'}
        rewritten = {'checkup_loja.html','tco_roi.html','gerador_proposta.html','cadencia_sdr.html','checklist_implantacao.html','auditor_xml.html','teleprompter.html','demo_pdv.html'}
        self.assertEqual(set(original), retained | rewritten | {d['arquivo'] for d in decisions})
        for item in decisions:
            source = (ROOT / item['arquivo']).read_text(encoding='utf8')
            self.assertIn('replacement', source)
            self.assertNotRegex(source, r'alert\(|fetch\(|Math\.random')
            self.assertTrue((ROOT / item['destino'].split('?')[0]).is_file())

    def test_workshop_and_library_do_not_send_data(self):
        for name in ['oficina.js', 'biblioteca.js']:
            source = (ROOT / name).read_text(encoding='utf8')
            self.assertNotRegex(source, r'fetch\(|XMLHttpRequest|sendBeacon|/api/')
        source = (ROOT / 'oficina.js').read_text(encoding='utf8')
        self.assertIn('DOMParser', source)
        self.assertIn('textContent = output', source)

    def test_library_and_source_archive(self):
        source = (ROOT / 'biblioteca-dados.js').read_text(encoding='utf8')
        data = json.loads(source.split('=',1)[1].rstrip(';'))
        self.assertEqual(len(data),13)
        self.assertTrue(all(len(item['text'])>100 for item in data))
        self.assertTrue((ROOT / 'qa/ferramentas-fontes-antes.zip').is_file())

if __name__ == '__main__':
    unittest.main()
