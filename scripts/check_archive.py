"""Check redesigned entry points and preservation of the original archive.

Run from any directory: python3 scripts/check_archive.py
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'Writings/Writing.html', 'Projects/Projects Page.html',
         'Life.html', 'About_This_Site.html', 'Contact.html']


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids = [], set()
        self.h1 = 0
        self.viewport = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.h1 += tag == 'h1'
        self.viewport |= tag == 'meta' and attrs.get('name') == 'viewport'
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


for name in PAGES:
    page = Page((ROOT / name).read_text())
    assert page.h1 == 1 and page.viewport, name
    for link in page.links:
        assert link, f'{name}: empty link'
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (ROOT / name).parent / unquote(url.path) if url.path else ROOT / name
        assert target.is_file(), f'{name}: missing {link}'
        if url.fragment:
            assert unquote(url.fragment) in Page(target.read_text()).ids, link

writings = Page((ROOT / 'Writings/Writing.html').read_text())
linked = {unquote(urlsplit(link).path) for link in writings.links}
essays = {p.name for p in (ROOT / 'Writings').glob('*.html') if p.name != 'Writing.html'}
assert essays <= linked, f'Unlisted essays: {essays - linked}'

# The original content and binary assets must remain byte-for-byte intact.
BASE = 'afce9024ff3cca54612ec307132e55b906831cde'
for folder in ['Writings', 'Images', 'Web font']:
    for file in (ROOT / folder).rglob('*'):
        if file.is_file() and file.name != 'Writing.html':
            name = file.relative_to(ROOT).as_posix()
            original = subprocess.check_output(['git', 'show', f'{BASE}:{name}'], cwd=ROOT)
            assert original == file.read_bytes(), f'Original content changed: {name}'
print(f'PASS: {len(PAGES)} entry pages, all local links and anchors, {len(essays)} essays indexed; original essays and assets unchanged.')
