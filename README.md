# MILUJ Sanctuary

Úvodná stránka webu MILUJ Sanctuary (healing & retreat sanctuary, Bali).

- `index.html` – celá stránka (HTML, CSS, JavaScript)
- `assets/` – obrázky a videá
- `water/index.html` – podstránka /water
- `sk/` – **slovenská verzia je zdroj**, edituje sa len ona. Angličtina (koreň webu) a `es/` sa z nej generujú: `python3 tools/build_i18n.py` (preklady v `tools/i18n_strings.py` a `tools/i18n_water.py`)
- Hosting: GitHub Pages (vetva `main`, koreň repozitára) – https://martinsiladi-spec.github.io/miluj-web/
- Odovzdanie pre novú reláciu: `HANDOFF.md`
