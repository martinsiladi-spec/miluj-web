"""Build the Slovak and Spanish homepages from the English one.

    python3 tools/build_i18n.py

index.html (English) is the only source. This script copies it to sk/index.html and es/index.html,
translates every text it finds in tools/i18n_strings.py, points asset and page links one folder up,
and sets the language switcher. It lists anything it could not translate, so new English text is
never silently left behind: add a row to i18n_strings.py and run it again.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from i18n_strings import T
from jsstrings import scan, human

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = {'sk': 1, 'es': 2}
ATTRS = r'(alt|aria-label|content|title|placeholder)'
SUBSTRINGS = ['up to 24 h (target)', '<b>How it works</b>', '} of 08: ${', 'alt="${c[1]} at MILUJ"']          # text that sits inside a longer JS template
IGNORE = {'(prefers-reduced-motion: reduce)', '(hover: hover) and (pointer: fine)', 'POST', 'Content-Type', 'Accept', 'send failed',
          '"Noto Serif Armenian", Sylfaen, "Arial Unicode MS", serif', '500 22px Jost, sans-serif', 'MILUJ Sanctuary · new investor request',
          '0110 MILUJ 1001 ✦ 0101 LOVE 1100 ◇ 0011 LIGHT 1010 △ 0111 HEART 1001 ○ 1101 TRUTH 0100 ', 'Vinyasa', 'Breathwork', 'Gene Keys'}
SKIP_TEXT = re.compile(r'^@@NOTE[\d\s@NOTE]*@@$|^\d+ (min|h)$|^[\d\s.,:%·€→↗×–+-]*$|^MILUJ( Sanctuary| Bali)?$|^(EN|SK|ES)$')

def translate_html(chunk, d, missing):
    out = []
    for tok in re.split(r'(<[^>]+>)', chunk):
        if tok.startswith('<'):
            def attr(m):
                v = m.group(2)
                if v in d: return f'{m.group(1)}="{d[v]}"'
                if re.search(r'[A-Za-z]{2,} [A-Za-z]', v) and not v.startswith('width=') and v not in IGNORE:
                    missing.add(v)
                return m.group(0)
            out.append(re.sub(ATTRS + r'="([^"]*)"', attr, tok))
        else:
            m = re.match(r'(\s*)(.*?)(\s*)$', tok, re.S); text = m.group(2)
            if text in d: out.append(m.group(1) + d[text] + m.group(3))
            else:
                if text and re.search(r'[A-Za-z]{2,}', text) and not SKIP_TEXT.match(text): missing.add(text)
                out.append(tok)
    return ''.join(out)

def translate_js(js, d, missing):
    out, last = [], 0
    for st, en, q, t in scan(js):
        plain = t.replace("\\'", "'")
        new = None
        if plain in d: new = d[plain]
        elif q == '`':
            for k in SUBSTRINGS:
                if k in t: t = t.replace(k, d[k]); new = t
        if new is None:
            if human(plain) and plain not in IGNORE and '${' not in plain and not SKIP_TEXT.match(plain): missing.add(plain)
            continue
        if q == "'": new = new.replace("'", "\\'")
        out.append(js[last:st + 1] + new); last = en - 1
    out.append(js[last:])
    return ''.join(out)

def build(lang):
    col = LANGS[lang]
    d = {row[0]: row[col] for row in T}
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    # the notes in the source are hidden working notes; they never need translating
    notes = re.findall(r'<aside class="note.*?</aside>', s, re.S)
    for i, n in enumerate(notes): s = s.replace(n, f'@@NOTE{i}@@')
    missing = set()
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
    for i, p in enumerate(parts):
        if p.startswith('<script'): parts[i] = translate_js(p, d, missing)
        elif p.startswith('<style'): pass
        else: parts[i] = translate_html(p, d, missing)
    s = ''.join(parts)
    for i, n in enumerate(notes): s = s.replace(f'@@NOTE{i}@@', n)
    # one folder down: assets and the water page are one level up
    s = re.sub(r'(["\'`(])assets/', r'\1../assets/', s)
    s = s.replace('href="water/"', 'href="../water/"')
    s = s.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    # language switcher as seen from /<lang>/
    sw = {'en': '../', 'sk': '../sk/', 'es': '../es/'}
    def link(m):
        code = m.group(2)
        cur = ' aria-current="true"' if code == lang else ''
        return f'<a href="{sw[code]}" hreflang="{code}" lang="{code}"{cur}>{code.upper()}</a>'
    s = re.sub(r'<a href="[^"]*" hreflang="(en|sk|es)" lang="(en|sk|es)"(?: aria-current="true")?>(?:EN|SK|ES)</a>',
               lambda m: link(m), s)
    os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
    open(os.path.join(ROOT, lang, 'index.html'), 'w', encoding='utf-8').write(s)
    unused = [k for k in d if k not in open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read().replace("\\'", "'")]
    return sorted(missing), unused

if __name__ == '__main__':
    ok = True
    for lang in LANGS:
        missing, unused = build(lang)
        print(f'{lang}/index.html written')
        for m in missing: print(f'  not translated: {m[:110]}'); ok = False
        for u in unused: print(f'  unused row (no longer on the page): {u[:110]}')
    sys.exit(0 if ok else 1)
