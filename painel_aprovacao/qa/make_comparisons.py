from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
q=Path(__file__).parent
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',28)
for old,new,name in [('aprovacao-antes.png','index-chrome-1366.png','comparativo-aprovacao'),('calendario-antes.png','calendario-chrome-1366.png','comparativo-calendario')]:
 a,b=Image.open(q/old).convert('RGB'),Image.open(q/new).convert('RGB')
 canvas=Image.new('RGB',(a.width+b.width+24,max(a.height,b.height)+72),'white')
 canvas.paste(a,(0,72));canvas.paste(b,(a.width+24,72))
 d=ImageDraw.Draw(canvas);d.text((24,20),'Antes',font=font,fill='#0f172a');d.text((a.width+48,20),'Depois',font=font,fill='#0f172a')
 canvas.save(q/(name+'.jpg'),quality=91)
def luminance(h):
 v=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 v=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in v]
 return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
pairs=[('Texto','#0f172a','#ffffff'),('Texto secundário','#475569','#f1f5f9'),('Botão principal','#ffffff','#075985'),('Sucesso','#166534','#dcfce7'),('Pendente','#854d0e','#fef9c3'),('Erro','#991b1b','#fee2e2'),('Informação','#075985','#e0f2fe'),('Marca','#0f172a','#009fe3')]
report=[]
for name,fg,bg in pairs:
 x,y=sorted([luminance(fg),luminance(bg)])
 ratio=(y+.05)/(x+.05)
 assert ratio>=4.5,(name,ratio)
 report.append({'uso':name,'texto':fg,'fundo':bg,'contraste':round(ratio,2)})
(q/'contraste.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
