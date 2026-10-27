"""Validate artifact links, public-file allowlist and snapshot integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
root=Path(__file__).resolve().parents[1];dist=root/'site-dist'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src') and value:self.links.append(value)
for page in dist.rglob('*.html'):
    parser=Links();parser.feed(page.read_text())
    for url in parser.links:
        parts=urlsplit(url)
        if parts.scheme or url.startswith(('#','/')):continue
        assert (page.parent/unquote(parts.path)).exists(),(page,url)
assert not list(dist.rglob('*.docx')) and not list(dist.rglob('*.xlsx'))
for file in dist.rglob('*'):
    if file.is_file():
        text=file.read_text()
        for forbidden in ['167,603.73','96,290','44,290','6158400718','FMfcgzQh','/Users/jason/','gho_']:
            assert forbidden not in text,(file,forbidden)
snapshot=json.loads((dist/'data/project.json').read_text());items=snapshot['items']
assert len({i['number'] for i in items})==len(items)
assert not {9,11,15,18,19,21,28,29,32,33,36}.intersection(i['number'] for i in items)
active=[i['number'] for i in items if i['status']=='In progress']
completed=sorted([i for i in items if i['status']=='Done'],key=lambda x:x['closedAt'] or '',reverse=True)[:3]
print('Validated local links and publication boundary. Active:',active,'Recent:',[x['number'] for x in completed])
