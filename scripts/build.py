#!/usr/bin/env python3
"""Render every locale and route as static HTML. Python standard library only."""
import html
import json
import os
from pathlib import Path
import shutil
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
SITE = os.environ.get('SITE_URL', 'https://glzlaohuai.github.io/desktoppet-site').rstrip('/')
if urlsplit(SITE).scheme not in ('https', 'http') or not urlsplit(SITE).netloc:
    raise ValueError('SITE_URL must be an absolute HTTP(S) URL')
BASE = urlsplit(SITE).path.rstrip('/')
LOCALES = json.loads((ROOT / 'content/locales.json').read_text())
MARKETING = json.loads((ROOT / 'content/marketing.json').read_text())
KINDS = ['cat', 'shiba', 'rabbit', 'hamster', 'ragdoll', 'blackCat', 'corgi']
ISSUES = 'https://github.com/glzlaohuai/desktoppet-site/issues'
APPLE = 'https://support.apple.com/billing'
APPLE_PRIVACY = 'https://www.apple.com/legal/privacy/'
GH_PRIVACY = 'https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement'
esc = lambda value: html.escape(str(value), quote=True)

def route(lang, page=''):
    return '/' + '/'.join(x for x in [lang if lang != 'en' else '', page] if x) + ('/' if lang != 'en' or page else '')

def href(lang, page=''):
    return BASE + route(lang, page)

def asset(path):
    return BASE + '/assets/' + path

def para(text):
    return '<p>' + esc(text) + '</p>'

def pet_image(kind, css='', pose='idle', size=96):
    return f'<img class="pixel {css}" src="{asset(f"pets/{kind}-{pose}-0.png")}" alt="" width="{size}" height="{size}">'

def shell(lang, page, body):
    t = LOCALES[lang]
    title = t['title'] if not page else t['supportTitle'] if page == 'support' else t['privacyTitlePage'] if page == 'privacy' else t['notFound']
    description = t['intro'] if not page else t['supportIntro'] if page == 'support' else t['privacyIntro']
    canonical = SITE + route(lang, page)
    alternates = ''.join(f'<link rel="alternate" hreflang="{v["htmlLang"]}" href="{SITE}{route(k,page)}">' for k,v in LOCALES.items())
    options = ''.join(f'<option value="{href(k,page)}" {"selected" if k==lang else ""}>{esc(v["name"])}</option>' for k,v in LOCALES.items())
    language_links = ''.join(f'<a href="{href(k,page)}" lang="{v["htmlLang"]}" hreflang="{v["htmlLang"]}">{esc(v["name"])}</a>' for k,v in LOCALES.items())
    def nav_link(label, target):
        current = ' aria-current="page"' if target == page else ''
        return f'<a href="{href(lang,target)}"{current}>{esc(t[label])}</a>'
    schema = json.dumps({'@context':'https://schema.org','@type':'SoftwareApplication','name':'DesktopPet','applicationCategory':'LifestyleApplication','operatingSystem':'macOS 14 or later','description':description,'url':SITE+route(lang),'inLanguage':t['htmlLang'],'image':SITE+'/assets/og.png'},ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="{t['htmlLang']}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · DesktopPet</title><meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#f4bd96"><link rel="canonical" href="{esc(canonical)}">
{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}{route('en',page)}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} · DesktopPet">
<meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{asset('favicon.png')}">
<link rel="stylesheet" href="{asset('site.css')}"><script src="{asset('site.js')}" defer></script>
<script type="application/ld+json">{schema}</script>
</head>
<body data-page="{esc(page)}">
<a class="skip" href="#main">{esc(t['skip'])}</a>
<header class="header wrap">
<a class="brand" href="{href(lang)}"><img src="{asset('icon.png')}" alt="" width="40" height="40">DesktopPet<span class="brand-dot" aria-hidden="true">.</span></a>
<nav aria-label="{esc(t['home'])}">{nav_link('pets','')}{nav_link('support','support')}{nav_link('privacy','privacy')}</nav>
<div class="language"><label class="sr-only" for="language">{esc(t['language'])}</label><span aria-hidden="true">◎</span><select id="language">{options}</select></div>
</header>
<main id="main">{body}</main>
<footer class="footer wrap"><div><a class="brand" href="{href(lang)}">DesktopPet<span class="brand-dot" aria-hidden="true">.</span></a><p>{esc(t['footer'])}</p></div>
<div class="footer-links">{nav_link('support','support')}{nav_link('privacy','privacy')}<a href="https://github.com/glzlaohuai/desktoppet-site">GitHub ↗</a></div>
<div class="language-links" aria-label="{esc(t['language'])}">{language_links}</div><small>© 2026 DesktopPet</small></footer>
</body></html>'''

def home(lang):
    t=LOCALES[lang]
    desc=MARKETING[lang]
    picker=''.join(f'''<button class="pet-choice" type="button" data-pet="{kind}" data-name="{esc(t['petNames'][i])}" aria-pressed="{'true' if i==0 else 'false'}">{pet_image(kind)}<span>{esc(t['petNames'][i])}</span><small>{esc(t['included'] if i==0 else t['optional'])}</small></button>''' for i,kind in enumerate(KINDS))
    return f'''
<section class="hero wrap" aria-labelledby="hero-title">
<div class="hero-copy"><p class="eyebrow"><span aria-hidden="true">✳</span> {esc(t['eyebrow'])}</p><h1 id="hero-title">{esc(t['heroLines'][0])}<br><span>{esc(t['heroLines'][1])}</span></h1><p class="hero-intro">{esc(t['intro'])}</p>
<a class="button primary" href="#companions">{esc(t['pets'])}<span aria-hidden="true">↗</span></a>
<div class="release"><span class="status-dot" aria-hidden="true"></span><strong>{esc(t['coming'])}</strong><span>{esc(t['release'])}</span></div></div>
<div class="preview" data-asset-base="{asset('pets/')}" data-greeting="{esc(t['greeting'])}" data-playing="{esc(t['playing'])}">
<div class="preview-top"><span>{esc(t['preview'])}</span><button type="button" class="motion-toggle" data-pause="{esc(t['pause'])}" data-resume="{esc(t['resume'])}" aria-label="{esc(t['pause'])}" aria-pressed="false"><span aria-hidden="true">Ⅱ</span></button></div>
<div class="pet-stage"><div class="sun" aria-hidden="true"></div><span class="spark spark-one" aria-hidden="true">✦</span><span class="spark spark-two" aria-hidden="true">✧</span><p class="speech" role="status" aria-live="polite" aria-atomic="true">{esc(t['petNames'][0])}</p>{pet_image('cat','hero-pet',size=256)}<div class="ground" aria-hidden="true"></div></div>
<div class="preview-controls"><button class="button small" type="button" data-action="greet">{esc(t['hello'])} <span aria-hidden="true">♡</span></button><button class="text-button" type="button" data-action="play">{esc(t['play'])} <span aria-hidden="true">↗</span></button></div><p class="preview-hint">{esc(t['previewHint'])}</p>
</div></section>
<div class="facts wrap"><span>{esc(t['requirement'])}</span><span aria-hidden="true">✦</span><span>{esc(t['free'])}</span><span aria-hidden="true">✦</span><span>English · 中文 · 日本語 · 한국어 · Français · Deutsch</span></div>
<section class="companions wrap section" id="companions" aria-labelledby="meet-title"><p class="eyebrow">01 / DesktopPet</p><div class="section-heading"><h2 id="meet-title">{esc(t['meetTitle'])}</h2><p>{esc(t['meetIntro'])}</p></div><div class="pet-picker" role="group" aria-label="{esc(t['pets'])}">{picker}</div><div class="purchase-copy"><h3>{esc(t['purchaseTitle'])}</h3>{para(desc[1])}</div></section>
<section class="bond section" aria-labelledby="bond-title"><div class="wrap split"><div class="bond-art" aria-hidden="true"><span class="pixel-heart">♥</span>{pet_image('corgi','bond-corgi',size=224)}{pet_image('cat','bond-cat',pose='affection',size=192)}<span class="tiny-flower">✳</span><div class="friend-line"></div></div><div><p class="eyebrow">02 / {esc(t['bondLabel'])}</p><h2 id="bond-title">{esc(t['bondTitle'])}</h2>{para(desc[2])}</div></div></section>
<section class="quiet section wrap split" aria-labelledby="quiet-title"><div><p class="eyebrow">03 / {esc(t['quietLabel'])}</p><h2 id="quiet-title">{esc(t['quietTitle'])}</h2>{para(desc[0])}{para(desc[3])}<a class="inline-link" href="{href(lang,'support')}">{esc(t['support'])} <span aria-hidden="true">↗</span></a></div><figure class="app-capture"><img src="{asset(f'settings-{lang}.webp')}" alt="{esc(t['screenshot'])}" width="495" height="640" loading="lazy"><figcaption>{esc(t['screenshot'])}</figcaption></figure></section>
<section class="privacy-banner wrap"><div><p class="eyebrow">♡ / DesktopPet</p><h2>{esc(t['privacyTitle'])}</h2>{para(t['privacyIntro'])}<a class="button primary" href="{href(lang,'privacy')}">{esc(t['readPrivacy'])} <span aria-hidden="true">↗</span></a></div>{pet_image('rabbit','privacy-rabbit',pose='sleep',size=176)}</section>'''

def support(lang):
    t=LOCALES[lang]
    faqs=''.join(f'<details><summary>{esc(q)}<span aria-hidden="true">+</span></summary><div>{para(a)}</div></details>' for q,a in t['faqs'])
    return f'''<section class="page-head wrap"><p class="eyebrow">DesktopPet / {esc(t['support'])}</p><h1>{esc(t['supportTitle'])}</h1>{para(t['supportIntro'])}<a class="button primary" href="{ISSUES}">{esc(t['contact'])} <span aria-hidden="true">↗</span></a><p class="contact-note">{esc(t['publicNote'])}</p>{pet_image('shiba','page-pet',size=160)}</section>
<section class="support-layout wrap section"><h2>{esc(t['faqTitle'])}</h2><div class="faq">{faqs}<div class="support-after">{para(t['issueNote'])}<a class="inline-link" href="{APPLE}">{esc(t['appleHelp'])} ↗</a></div></div></section>'''

def privacy(lang):
    t=LOCALES[lang]
    paragraphs=(ROOT/f'content/privacy/{lang}.md').read_text().strip().split('\n\n')[1:]
    return f'''<section class="page-head wrap"><p class="eyebrow">DesktopPet / {esc(t['privacy'])}</p><h1>{esc(t['privacyTitlePage'])}</h1><p>{esc(t['effective'])}</p>{pet_image('rabbit','page-pet',pose='sleep',size=160)}</section>
<article class="policy wrap section"><section><h2>{esc(t['policyApp'])}</h2>{''.join(para(p) for p in paragraphs)}<a class="inline-link" href="{APPLE_PRIVACY}">{esc(t['applePolicy'])} ↗</a></section><section><h2>{esc(t['policyWebsite'])}</h2>{para(t['websitePolicy'])}<a class="inline-link" href="{GH_PRIVACY}">{esc(t['githubPolicy'])} ↗</a></section><section>{para(t['privacyContact'])}<a class="button primary" href="{href(lang,'support')}">{esc(t['support'])} ↗</a></section></article>'''

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT/'assets',OUT/'assets')
    urls=[]
    for lang in LOCALES:
        for page,render in [('',home),('support',support),('privacy',privacy)]:
            path=OUT/route(lang,page).lstrip('/')/'index.html'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(shell(lang,page,render(lang)))
            urls.append(SITE+route(lang,page))
    t=LOCALES['en']
    body=f'<section class="page-head wrap"><h1>{esc(t["notFound"])}</h1>{para(t["notFoundText"])}<a class="button primary" href="{href("en")}">{esc(t["back"])}</a></section>'
    (OUT/'404.html').write_text(shell('en','',body))
    (OUT/'.nojekyll').touch()
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{xml_escape(u)}</loc></url>' for u in urls)+'</urlset>\n')
    print(f'Rendered {len(urls)} localized pages and 404.html for {SITE}')

if __name__=='__main__': build()
