"""Build the English and Spanish pages from the Slovak ones.

    python3 tools/build_i18n.py

The Slovak pages are the only source:  sk/index.html  and  sk/water/index.html  (edit only these).
This script writes  index.html, water/index.html  (English, the site root)  and  es/index.html, es/water/index.html:
it translates every text listed in tools/i18n_strings.py and tools/i18n_water.py, fixes the asset paths for the
folder depth, and sets the language switcher and <html lang>. Each row there is (English, Slovak, Spanish);
the Slovak text is the key and must match the Slovak page exactly. It lists anything it could not translate
(and exits with an error), so new Slovak text is never silently left behind: add a row and run it again.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n_strings import T as T_HOME
from i18n_water import T as T_WATER
from jsstrings import scan, human

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, KEY = 'sk', 1                       # source language and its column in the rows
TARGETS = {'en': 0, 'es': 2}
PAGES = ['', 'water/']                       # page folders, relative to the site root
ATTRS = r'(alt|aria-label|content|title|placeholder)'
SUBSTRINGS = []
SUBSTRINGS_EN = ["p[2] + ' at MILUJ'", '} of 08: ${', 'alt="${c[1]} at MILUJ"']   # text inside longer JS templates
IGNORE = {'(prefers-reduced-motion: reduce)', '(hover: hover) and (pointer: fine)', 'POST', 'Content-Type', 'Accept', 'send failed',
          '"Noto Serif Armenian", Sylfaen, "Arial Unicode MS", serif', '500 22px Jost, sans-serif', 'MILUJ Sanctuary · new investor request',
          '0110 MILUJ 1001 ✦ 0101 LOVE 1100 ◇ 0011 LIGHT 1010 △ 0111 HEART 1001 ○ 1101 TRUTH 0100 ', 'Vinyasa', 'Breathwork', 'Gene Keys',
          'IntersectionObserver', 'Nature Medicine', 'Nanomedicine', 'EZ', 'arXiv ↗', '-45% 0px -50% 0px', '0px 0px -8% 0px', '150% 0px', '200% 0px'}
SKIP_TEXT = re.compile(r'^@@NOTE[\d\s@NOTE]*@@$|^\d+ (min|h)$|^[\d\s.,:%·€→↗×–+-]*$|^MILUJ( Sanctuary| Bali)?$|^(EN|SK|ES)$'
                       r'|^(H|O|H₂|H₂O|EZ|C)$|^H₂ \+ 2 •OH → 2 H₂O$|^≈ 20 min$|^[A-Z][\w .,/]*↗$|^Nature Medicine, 2007 ↗$')

def text_nodes(fragment, d, missing):
    """translate the text between tags of an HTML fragment"""
    def node(m):
        lead, text, trail = re.match(r'(\s*)(.*?)(\s*)$', m.group(1), re.S).groups()
        if text in d: return '>' + lead + d[text] + trail + '<'
        if text and re.search(r'[A-Za-z]{2,}', text) and '${' not in text and '`' not in text and not SKIP_TEXT.match(text) and text not in IGNORE: missing.add(text)
        return m.group(0)
    return re.sub(r'>([^<>]+)<', node, fragment)

def translate_html(chunk, d, missing):
    out = []
    for tok in re.split(r'(<[^>]+>)', chunk):
        if tok.startswith('<'):
            def attr(m):
                v = m.group(2)
                if v in d: return f'{m.group(1)}="{d[v]}"'
                if re.search(r'[A-Za-z]{2,} [A-Za-z]', v) and not v.startswith('width=') and v not in IGNORE: missing.add(v)
                return m.group(0)
            out.append(re.sub(ATTRS + r'="([^"]*)"', attr, tok))
        else:
            out.append(text_nodes('>' + tok + '<', d, missing)[1:-1])
    return ''.join(out)

def translate_js(js, d, missing):
    out, last = [], 0
    for st, en, q, t in scan(js):
        plain = t.replace("\\'", "'"); new = None
        if plain in d: new = d[plain]
        else:
            body = t
            if re.search(r'<[a-z]', body):                       # HTML inside a string: translate its text nodes
                body = text_nodes(body, d, missing)
            for k in SUBSTRINGS:
                if k in body: body = body.replace(k, d[k])
            if body != t: new = body.replace("\\'", "'")
            elif human(plain) and plain not in IGNORE and '${' not in plain and not SKIP_TEXT.match(plain): missing.add(plain)
        if new is None: continue
        if q == "'": new = new.replace("'", "\\'")
        out.append(js[last:st + 1] + new); last = en - 1
    out.append(js[last:])
    return ''.join(out)

def switcher(s, lang, page):
    up = '../' * (page.count('/') + (lang != 'en'))   # from this page back to the site root (English lives at the root)
    href = {code: up + ('' if code == 'en' else code + '/') + page for code in ('en', 'sk', 'es')}
    href[lang] = './'
    def link(m):
        code = m.group(1)
        cur = ' aria-current="true"' if code == lang else ''
        return f'<a href="{href[code] or "./"}" hreflang="{code}" lang="{code}"{cur}>{code.upper()}</a>'
    return re.sub(r'<a href="[^"]*" hreflang="(en|sk|es)" lang="(?:en|sk|es)"(?: aria-current="true")?>(?:EN|SK|ES)</a>', link, s)

def build(lang, page, d):
    src = os.path.join(ROOT, SRC, page, 'index.html')
    s = open(src, encoding='utf-8').read()
    notes = re.findall(r'<aside class="note.*?</aside>', s, re.S)   # hidden working notes stay as they are
    for i, n in enumerate(notes): s = s.replace(n, f'@@NOTE{i}@@')
    missing = set()
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
    for i, p in enumerate(parts):
        if p.startswith('<script'): parts[i] = translate_js(p, d, missing)
        elif not p.startswith('<style'): parts[i] = translate_html(p, d, missing)
    s = ''.join(parts)
    for i, n in enumerate(notes): s = s.replace(f'@@NOTE{i}@@', n)
    if lang == 'en': s = re.sub(r'(["\'`(])\.\./((?:\.\./)*)assets/', r'\1\2assets/', s)   # English sits one folder higher
    s = s.replace(f'<html lang="{SRC}">', f'<html lang="{lang}">', 1)
    s = switcher(s, lang, page)
    out = os.path.join(ROOT, '' if lang == 'en' else lang, page, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)
    return out, sorted(missing)

if __name__ == '__main__':
    ok = True
    for lang, col in TARGETS.items():
        for page in PAGES:
            # the page's own rows win over the other file's, so the same Slovak text may read differently on each page
            rows = (T_WATER + T_HOME) if page == '' else (T_HOME + T_WATER)
            d = {r[KEY]: r[col] for r in rows}
            en2sk = {r[0]: r[KEY] for r in rows}
            for k in SUBSTRINGS_EN: d[en2sk.get(k, k)] = {r[0]: r[col] for r in rows}.get(k, k)
            SUBSTRINGS[:] = [en2sk.get(k, k) for k in SUBSTRINGS_EN]
            out, missing = build(lang, page, d)
            print(os.path.relpath(out, ROOT), 'written')
            for m in missing: print(f'  not translated: {m[:110]}'); ok = False
    sources = ''.join(open(os.path.join(ROOT, SRC, p, 'index.html'), encoding='utf-8').read() for p in PAGES).replace("\\'", "'")
    for r in T_HOME + T_WATER:
        if r[KEY] not in sources: print(f'unused row (no longer on any page): {r[KEY][:100]}')
    sys.exit(0 if ok else 1)
