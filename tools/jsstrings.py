"""List (or rewrite) the string literals inside the homepage <script>, so translations can target them exactly."""
import re

def scan(js):
    """yield (start, end, quote, text) for every '…', "…" and `…` literal; skips comments and regex-free code well enough for this page"""
    i, n = 0, len(js)
    while i < n:
        c = js[i]
        if c == '/' and js[i + 1:i + 2] == '/':
            i = js.find('\n', i); i = n if i < 0 else i; continue
        if c == '/' and js[i + 1:i + 2] == '*':
            i = js.find('*/', i) + 2; continue
        if c in '\'"`':
            j = i + 1
            while j < n and js[j] != c:
                if js[j] == '\\': j += 1
                elif c == '`' and js[j:j + 2] == '${':          # skip a template expression
                    depth = 1; j += 2
                    while j < n and depth:
                        if js[j] == '{': depth += 1
                        elif js[j] == '}': depth -= 1
                        j += 1
                    continue
                j += 1
            yield i, j + 1, c, js[i + 1:j]
            i = j + 1; continue
        i += 1

def human(t):
    if re.search(r'rgba?\(|var\(--|\bpx\b|=>|querySelector|^[#.][\w-]|\.(webp|mp4|png)|cubic-bezier|https?:|^\s*$|<\/?[a-z]', t): return False
    return bool(re.search(r'[A-Za-zÀ-ž]{2,}', t)) and (' ' in t.strip() or t[:1].isupper())

if __name__ == '__main__':
    s = open('index.html', encoding='utf-8').read()
    a = s.index('<script>'); b = s.index('</script>', a)
    out = []
    for st, en, q, t in scan(s[a:b]):
        if human(t) and t not in out: out.append(t)
    for t in out: print(repr(t))
    print(len(out))
