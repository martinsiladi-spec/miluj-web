"""Build test/index.html: a hidden copy of the Slovak homepage with the intro reveal and the glass loading veil.

    python3 tools/make_test_intro.py

The live pages are not touched. test/ is not linked from anywhere and is marked noindex.
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'sk', 'index.html'), encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (a[:70], s.count(a))
    s = s.replace(a, b)

# ---- head: hidden test page ----
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">')
s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n', '', s)

# ---- CSS ----
CSS = r'''
/* ===== TEST: intro reveal + glass loading veil ===== */
.hero h1 .w{display:inline-block;opacity:0;filter:blur(14px);transform:translateY(.32em);animation:wIn 1.2s cubic-bezier(.23,1,.32,1) forwards}
@keyframes wIn{to{opacity:1;filter:blur(0);transform:none}}
.hero p.lead,.hero .ctas,.hero .cue{opacity:0;animation:fadeUp 1.1s cubic-bezier(.23,1,.32,1) forwards}
.hero p.lead{animation-delay:1.55s}.hero .ctas{animation-delay:1.95s}.hero .cue{animation-delay:2.5s}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){.hero h1 .w,.hero p.lead,.hero .ctas,.hero .cue{animation:none;opacity:1;filter:none;transform:none}}

/* frosted glass over a scrub video until it has downloaded; it clears as the download progresses */
.glass{--gb:28px;position:absolute;inset:0;pointer-events:none;
  -webkit-backdrop-filter:blur(var(--gb)) saturate(1.55) brightness(1.04);backdrop-filter:blur(var(--gb)) saturate(1.55) brightness(1.04);
  background:linear-gradient(135deg,rgba(255,255,255,.11) 0%,rgba(255,255,255,.025) 42%,rgba(255,255,255,.07) 100%);
  transition:opacity 1.1s ease,-webkit-backdrop-filter .9s ease,backdrop-filter .9s ease}
.glass::before{content:"";position:absolute;inset:-20% -60%;background:linear-gradient(105deg,transparent 42%,rgba(255,255,255,.10) 50%,transparent 58%);animation:sheen 4.8s ease-in-out infinite;mix-blend-mode:screen}
@keyframes sheen{from{transform:translateX(-35%)}to{transform:translateX(35%)}}
.glass::after{content:"";position:absolute;inset:0;opacity:.05;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.glass.done{opacity:0}
.pill{position:absolute;z-index:3;left:50%;bottom:clamp(64px,10vh,96px);transform:translateX(-50%);display:flex;align-items:center;gap:12px;padding:.75em 1.25em;border-radius:999px;
  background:rgba(255,255,255,.08);-webkit-backdrop-filter:blur(18px) saturate(1.6);backdrop-filter:blur(18px) saturate(1.6);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.28),inset 0 -1px 0 rgba(255,255,255,.06),0 10px 30px rgba(0,0,0,.25);
  font:400 13px/1 var(--body);letter-spacing:.06em;color:rgba(245,239,226,.86);white-space:nowrap}
.pill i{position:relative;display:block;width:64px;height:2px;border-radius:2px;background:rgba(245,239,226,.18);overflow:hidden}
.pill i b{position:absolute;inset:0;transform-origin:0 50%;transform:scaleX(var(--p,0));background:var(--gold-2);transition:transform .6s ease}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.glass{background:rgba(11,14,12,.62)}.pill{background:rgba(11,14,12,.7)}}
.pill{transition:opacity .8s ease}.pill.done{opacity:0}
@media (prefers-reduced-motion: reduce){.glass::before{animation:none;display:none}}
'''
rep('<style>body{margin:0}.note{display:none!important}</style>', '<style>' + CSS + '</style>\n<style>body{margin:0}.note{display:none!important}</style>')

# ---- hero headline: words reveal one by one ----
m = re.search(r'<h1>(.*?)<em class="g">(.*?)</em></h1>', s)
plain, gold = m.group(1).split(), m.group(2).split()
d, parts = .35, []
for w in plain:
    parts.append(f'<span class="w" style="animation-delay:{d:.2f}s">{w}</span>'); d += .16
d += .12
gold_html = ' '.join(f'<span class="w" style="animation-delay:{d + i * .2:.2f}s">{w}</span>' for i, w in enumerate(gold))
s = s.replace(m.group(0), '<h1>' + ' '.join(parts) + ' <em class="g">' + gold_html + '</em></h1>', 1)

# ---- glass veil inside the film and mission scenes ----
VEIL = '<div class="glass" id="{id}" aria-hidden="true"></div><span class="pill" id="{id}Pill" aria-hidden="true"><span class="lbl">{lbl}</span><i><b></b></i><span class="pct">0 %</span></span>'
rep('data-src="../assets/film.mp4"></video>', 'data-src="../assets/film.mp4"></video>\n    ' + VEIL.format(id='filmGlass', lbl='Pripravujeme film'))
rep('data-src="../assets/crowd.mp4"></video>', 'data-src="../assets/crowd.mp4"></video>\n    ' + VEIL.format(id='crowdGlass', lbl='Pripravujeme scénu'))

# ---- JS: streamed download with progress, film first, crowd right after ----
old_load = s[s.index('  const loadScrub = (v, onDur) => {'):s.index('  { const mio = new IntersectionObserver')]
new_load = '''  const loadScrub = (v, onDur, glass) => {
    const url = v.dataset.src, pill = glass && document.getElementById(glass.id + 'Pill'), pct = pill && pill.querySelector('.pct');
    let shownStep = -1;
    const prog = p => { if (!glass) return; const step = Math.min(25, Math.floor(p * 25)); if (step === shownStep) return; shownStep = step;
      const q = step / 25; glass.style.setProperty('--gb', (2 + 26 * Math.pow(1 - q, 1.4)).toFixed(1) + 'px'); pill.style.setProperty('--p', q.toFixed(2)); pct.textContent = Math.round(q * 100) + ' %'; };
    const clear = () => { if (glass) { prog(1); setTimeout(() => { glass.classList.add('done'); pill.classList.add('done'); }, 250); } };
    const set = () => { if (v.duration && isFinite(v.duration)) onDur(v.duration); };
    v.addEventListener('loadedmetadata', set); v.addEventListener('durationchange', set);
    v.addEventListener('loadeddata', clear, { once: true });
    const direct = () => { v.src = url; v.load(); };
    const done = fetch(url).then(async r => {
      if (!r.ok) throw r.status;
      const total = +r.headers.get('content-length') || 0;
      if (!r.body || !total) return r.blob();
      const reader = r.body.getReader(), chunks = []; let got = 0;
      for (;;) { const { done, value } = await reader.read(); if (done) break; chunks.push(value); got += value.length; prog(got / total); }
      return new Blob(chunks, { type: 'video/mp4' });
    }).then(b => { v.src = URL.createObjectURL(b); v.load(); }).catch(direct);
    return done;
  };
'''
s = s.replace(old_load, new_load, 1)
old_mio = s[s.index('  { const mio = new IntersectionObserver'):s.index('\n', s.index('    mio.observe(mission); }')) + 1]
s = s.replace(old_mio, '', 1)
old_go = s[s.index('  { const go = () => (window.requestIdleCallback'):s.index('\n', s.index("if (document.readyState === 'complete') go();")) + 1]
s = s.replace(old_go, '''  /* TEST: start at once, film first, then the crowd (or earlier if the visitor is already close to it) */
  { let crowdStarted = false;
    const crowd = () => { if (crowdStarted) return; crowdStarted = true; loadScrub(cvid, d => { cDur = d; }, $('#crowdGlass')); };
    let filmStarted = false;
    const film0 = () => { if (filmStarted) return; filmStarted = true; loadScrub(vid, d => { dur = d; }, $('#filmGlass')).then(crowd, crowd); };
    // the first view comes first: the film waits until the pyramid photo is on screen (at most 2.5 s), so it never steals bandwidth from it
    const heroImg = document.querySelector('.hero .bg img');
    if (heroImg.complete) setTimeout(film0, 150); else { heroImg.addEventListener('load', () => setTimeout(film0, 150), { once: true }); heroImg.addEventListener('error', film0, { once: true }); setTimeout(film0, 2500); }
    const mio = new IntersectionObserver(es => { if (es[0].isIntersecting) { mio.disconnect(); film0(); crowd(); } }, { rootMargin: '100% 0px' });
    mio.observe(mission);
    const fio = new IntersectionObserver(es => { if (es[0].isIntersecting) { fio.disconnect(); film0(); } }, { rootMargin: '50% 0px' });
    fio.observe(film); }
''', 1)
assert 'fio.observe(film); }' in s and "loadScrub(vid, d => { dur = d; }, $('#filmGlass'))" in s

os.makedirs(os.path.join(ROOT, 'test'), exist_ok=True)
open(os.path.join(ROOT, 'test', 'index.html'), 'w', encoding='utf-8').write(s)
print('test/index.html written', len(s))
