#!/usr/bin/env python3
"""Check rendered content and every local link without network dependencies."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
import build

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags=[]
        self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        self.tags.append((tag,attrs))
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])

locales=json.loads((build.ROOT/'content/locales.json').read_text())
assert set(locales)=={'en','zh-Hans','ja','ko','fr','de'}
assert all(set(v)==set(locales['en']) for v in locales.values()), 'Missing translation keys'
assert all(len(v['petNames'])==7 and len(v['faqs'])==6 for v in locales.values())
checked=0
for lang in locales:
    for page in ('','support','privacy'):
        path=build.OUT/build.route(lang,page).lstrip('/')/'index.html'
        content=path.read_text()
        assert 'apps.apple.com/' not in content, 'Unreleased App Store link'
        doc=Document(); doc.feed(content)
        assert len([t for t,a in doc.tags if t=='h1'])==1, path
        assert any(t=='html' and a.get('lang')==locales[lang]['htmlLang'] for t,a in doc.tags)
        assert len([a for t,a in doc.tags if t=='link' and a.get('hreflang')])==7
        if page=='':
            assert len([a for t,a in doc.tags if t=='button' and 'data-pet' in a])==7
        if page=='privacy':
            source=(build.ROOT/f'content/privacy/{lang}.md').read_text().split('\n\n')[1:]
            for paragraph in source:
                assert build.esc(paragraph.strip()) in content, 'Reviewed policy was modified'
        for tag,a in doc.tags:
            if tag=='img': assert 'alt' in a, f'Missing alt: {path}'
            for key in ('href','src'):
                ref=a.get(key,'')
                if not ref or urlsplit(ref).scheme or ref.startswith('//'): continue
                parsed=urlsplit(ref)
                if parsed.path:
                    target=unquote(parsed.path)
                    if build.BASE:
                        assert target.startswith(build.BASE+'/'), f'Wrong base path: {ref}'
                        target=target[len(build.BASE):]
                    file=build.OUT/target.lstrip('/')
                    if file.is_dir(): file=file/'index.html'
                    assert file.is_file(), f'Broken {key}: {ref} in {path}'
                elif parsed.fragment:
                    assert parsed.fragment in doc.ids, f'Broken anchor: {ref}'
        checked+=1
print(f'PASS: {checked} localized pages; complete translation keys; reviewed privacy; all local links and images; no unreleased download links')
