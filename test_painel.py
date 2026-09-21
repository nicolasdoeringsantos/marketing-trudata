# -*- coding: utf-8 -*-
import urllib.request
import re

url = "http://127.0.0.1:8080/"
html = urllib.request.urlopen(url).read().decode('utf-8')

print("1. Cockpit Section:", 'id="secao-cockpit"' in html)
cards = re.findall(r'class="[^"]*cockpit-card', html)
print(f"2. Cockpit Cards: {len(cards)} cards found")
pillares = re.findall(r'class="[^"]*cockpit-pilar-bloco', html)
print(f"3. Pillars: {len(pillares)} pillars found")
print("4. Quick Dock:", 'Quick Dock de Balcão' in html)
print("5. Search input:", 'id="busca-cockpit"' in html)
print("6. Counter element:", 'id="cockpit-contador"' in html)
print("7. Init calls cockpit:", "alternarAba('cockpit')" in html)
print("8. Galeria hidden by default:", 'id="secao-galeria" class="hidden' in html)
print("9. Tab buttons present:", 'btn-aba-cockpit' in html and 'btn-aba-galeria' in html and 'btn-aba-posts' in html and 'btn-aba-stories' in html and 'btn-aba-auditoria' in html)
