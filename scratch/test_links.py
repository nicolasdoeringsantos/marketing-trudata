import urllib.request
import re

url = 'https://empresasriograndedosul.com.br/sarandi'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')

links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
print("Total links:", len(links))
for l in links[:30]:
    print("  ", l)
