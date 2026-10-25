"""Build a private copy of the whole site with the new intro, for review before it goes live.

    python3 tools/make_staging.py OUT_DIR

Writes OUT_DIR/site/... (all six pages in three languages + assets). The homepages get the new intro
(tools/make_test_intro.apply_intro); folder links point at index.html so the copy also works on hosts
without directory index (a private claude.ai page). Nothing in the repository's live pages changes.
"""
import os, re, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from make_test_intro import apply_intro
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {'index.html': 'en', 'sk/index.html': 'sk', 'es/index.html': 'es',
         'water/index.html': None, 'sk/water/index.html': None, 'es/water/index.html': None}

def explicit_index(s):
    # href="sk/" → "sk/index.html", "../" → "../index.html", "./" → "index.html"; anchors and absolute URLs stay
    def fix(m):
        h = m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|#|/)', h) or not (h.endswith('/') or h in ('.', '..')): return m.group(0)
        h = 'index.html' if h in ('./', '.') else h + ('index.html' if h.endswith('/') else '/index.html')
        return f'{m.group(1)}="{h}"'
    return re.sub(r'(href)="([^"]*)"', fix, s)

def build(out):
    site = os.path.join(out, 'site'); shutil.rmtree(site, ignore_errors=True)
    for rel, lang in PAGES.items():
        s = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        s = apply_intro(s, lang) if lang else s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
        s = explicit_index(s)
        p = os.path.join(site, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(s)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(site, 'assets'))
    return site

if __name__ == '__main__':
    print(build(sys.argv[1]))
