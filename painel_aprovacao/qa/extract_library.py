"""Preserva o texto editorial visível das antigas páginas, sem executar scripts."""
from html.parser import HTMLParser
from pathlib import Path
import zipfile,json,re
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.lines=[]
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style','svg'):self.skip+=1
  if tag in ('p','h1','h2','h3','h4','li','br','div'):self.lines.append('\n')
 def handle_endtag(self,tag):
  if tag in ('script','style','svg'):self.skip=max(0,self.skip-1)
  if tag in ('p','h1','h2','h3','h4','li','div'):self.lines.append('\n')
 def handle_data(self,s):
  if not self.skip:self.lines.append(s.strip()+' ')
titles={'stories':'Stories','carrosseis_feed':'Carrosséis de feed','roteiros_reels':'Roteiros para Reels','spots_radio':'Spots de rádio','estudio_brolls':'Planos de gravação','campanhas_ads':'Campanhas e anúncios','campanhas_trafego':'Textos de tráfego pago','figurinhas':'Textos para figurinhas','gerador_reels':'Ideias de Reels','gerador_carrosseis_916':'Carrosséis verticais','spots_radio_trilha':'Roteiros de locução','vitrine_comercios_rs':'Materiais de ponto de venda','pitch':'Apresentação comercial'}
data=[]
with zipfile.ZipFile(ROOT/'qa/ferramentas-fontes-antes.zip') as z:
 for stem,title in titles.items():
  p=Text();raw=z.read(stem+'.html').decode('utf8');p.feed(raw)
  lines=[' '.join(l.split()) for l in ''.join(p.lines).splitlines()];text='\n'.join(l for l in lines if l)
  # Textos de modelos que antes só apareciam após interação, preservados como referência.
  scripts='\n'.join(re.findall(r'<script[^>]*>(.*?)</script>',raw,re.S))
  literals=re.findall(r'(?:titulo|gancho|dor|solucao|cta|roteiro_completo|legenda|texto|headline|descricao|corpo|copy|textoMeta|textoGoogle)\s*:\s*([\'"`])((?:\\.|(?!\1).)*?)\1',scripts,re.S)
  extra=[]
  for _,value in literals:
   if len(value)>15 and '${' not in value:
    value=value.replace('\\n','\n').replace("\\'", "'").replace('\\"','"')
    if value not in extra and value not in text:extra.append(value)
  if extra:text+='\n\nModelos de texto da coleção\n\n'+'\n\n'.join(extra)
  data.append({'id':stem,'title':title,'text':text})
(ROOT/'biblioteca-dados.js').write_text('const BIBLIOTECA = '+json.dumps(data,ensure_ascii=False)+';',encoding='utf8')
print(len(data),'coleções preservadas')
