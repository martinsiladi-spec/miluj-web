# MILUJ Sanctuary – odovzdanie na pokračovanie (stav 23. 10. 2026)

Tento dokument stačí na pokračovanie v novej relácii. **Zdroj pravdy je GitHub repozitár** `martinsiladi-spec/miluj-web`. Starý artefakt-prototyp je už len archív a náčrtník.

---

## 1. Kontext

- **Klient:** Martin (martin.siladi@gmail.com).
  - Komunikácia **po slovensky**, obsah webu **po anglicky**.
  - Starý web má aj verzie `/sk` a `/es`.
- **Projekt:** MILUJ Sanctuary, healing & retreat centrum na Bali (Karangasem):
  - Ascension Pyramid a podzemná zvuková sála;
  - 21 Temple Houses („coded accommodation“);
  - vegetariánska reštaurácia s komunitnou halou;
  - štruktúrovaná a vodíková voda;
  - valuácia €5,7 M.
- **Cieľ redizajnu:**
  - menej textu, viac obrazov a pohybu viazaného na scroll;
  - vyzerať prémiovo, no rozprávať poctivo (pozri bod 7).
- **Martinov štýl spolupráce:**
  - Chce rýchle iterácie a krátke odpovede v slovenčine.
  - Nové obrázky chce najprv vidieť a schváliť, až potom ich animovať.
  - Často posiela doplnenia počas práce, treba ich zapracovať priebežne.

## 2. Kde čo žije

| Čo | Kde |
|---|---|
| Repozitár (verejný) | https://github.com/martinsiladi-spec/miluj-web (vetva `main`) |
| Živý web (GitHub Pages) | https://martinsiladi-spec.github.io/miluj-web/ |
| Podstránka voda | https://martinsiladi-spec.github.io/miluj-web/water/ |
| Pôvodný web (ChatGPT Sites) | https://miluj.julimvision.com (+ `/temple-houses`, `/water`, `/sk/…`, `/es/…`) |
| Archívny prototyp (artefakt, v27) | https://claude.ai/artifact/KeD92XWG3mGW5zy2Zns8EW |

**Štruktúra repozitára**
- `index.html`: celá úvodná stránka (HTML + CSS + JS v jednom súbore).
- `water/index.html`: podstránka /water; assety sa načítajú cez `../assets/`.
- `assets/`: všetky obrázky a videá (webp/mp4, spolu ~15 MB).
- `.nojekyll`, `README.md`, `HANDOFF.md` (tento súbor).
- Súbor `CNAME` zatiaľ **nie je**. Pridá sa až pri prepnutí domény (bod 8).

**Ako pokračovať v novej relácii**
1. Pripojiť repo: `add_repo` (owner `martinsiladi-spec`, repo `miluj-web`, access `push`) → naklonovať → `register_repo_root`. Claude GitHub App je u Martina nainštalovaná.
2. Upravovať súbory a lokálne ich skontrolovať:
   - `python3 -m http.server` a Playwright;
   - desktop 1440×900 aj mobil 390×844;
   - bez chýb v konzole a bez horizontálneho pretečenia.
3. Commitnúť a pushnúť:
   - `git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit …`
   - správy písať po slovensky;
   - `git push origin HEAD:main`;
   - GitHub Pages sa nasadí do ~1 min.
4. Overiť naživo v paneli prehliadača: najprv `request_access` na `https://martinsiladi-spec.github.io`, potom `navigate`. Workspace sám na github.io nedosiahne.

## 3. Úvodná stránka (`index.html`): poradie sekcií

1. **Hero:** logo `x_logo_hero.webp`, nadpis „Welcome home to *the New Earth*“. Jediné tlačidlo „Investor overview“ **len posúva** na `#invest`. „Plan a stay“ bolo odstránené.
2. **Film „Od skice k realite“** (`#film`): scroll-scrub video `film.mp4`, 45 s.
3. **Misia 100 000** (`#mission`): scroll-scrub `crowd.mp4` + logaritmické počítadlo, potom riadok Body / Emotion / Spirit.
4. **Praktiky** (`#practices`): marquee sprava doľava, 10 kariet `s00–s09`. Varianty `_v2`: breathwork (sediaci, viditeľný prúd vzduchu), dance, kundalini.
5. **Grounds** (`#grounds`), jedna pinned scéna:
   - masterplan s 22 obrysmi domov;
   - zoom do domu;
   - **Anatomy of a Temple House**, vrstvy:
     1. Natural construction;
     2. **Sacred symbols & words**: Flower of Life v strede, okolo kruhy arménskeho textu, ktorý sa rozvíja zo stredu von. Kreslí sa na plátnach otáčaných kompozítorom, preto je pohyb plynulý; zmienka o Gene Keys je odstránená;
     3. Crystal energy;
     4. Frequencies;
     5. Aromatherapy;
     6. Light & rhythm.
   - Preblikávanie mapy je opravené: zápisy štýlov len pri zmene, `will-change`, žiadne prekresľovanie v pokoji.
6. **Reštaurácia a komunita** (`#table`): Martinova fotka `r0_restaurant`. Ráno, poludnie a večer (`r1–r3`) sa striedajú v tom istom ráme.
7. **Voda** (`#water`):
   - karty „Structured water“ (`t12_alchemy`) a „Hydrogen immersion“ (`t11_h2pool`: vonkajší H₂ bazén pred pyramídou, nízky pohľad, ľudia v bazéne);
   - graf H₂;
   - tlačidlo „What makes water alive? Read the deep dive →“ na `water/`.
8. **Science track** (`#science`): horizontálny pás, 8 kariet `sc0–sc7` s úrovňou dôkazov.
9. **Measure** → **Journey** → **Investícia** (`#invest`, €5,7 M). Tri prázdne bloky (use of funds, participation, timeline) sú **odstránené**. Tlačidlo otvára investorský formulár.
10. **Záver:** „Investor overview ↗“ (`data-inv-open`) otvára formulár. „Plan a stay“ je odstránené.

### Investorský formulár (FormSubmit, aktivovaný a otestovaný)
- `<dialog id="invDialog">`, polia: meno, e-mail, krajina, správa a honeypot `_honey`.
- POST JSON na `https://formsubmit.co/ajax/hello.julimvillas@gmail.com`:
  - `_cc` = `martin.siladi@gmail.com` (skrytá kópia, zákazník ju nevidí);
  - `_template: table`, `_captcha: false`;
  - `_autoresponse` = uvítací text s pozvánkou na krátky hovor.
- Formulár otvárajú len tlačidlá dole (investícia + záver). Hero tlačidlo iba posúva.
- CSS: `.inv-form[hidden],.inv-done[hidden],.inv-error[hidden]{display:none!important}`.

### Graf „How long does H₂ stay in the water?“ (na oboch stránkach)
- Časová os má **dve pásma**:
  - minúty 0–20 min na prvých ~18 % šírky (na mobile 32 %), sqrt mierka, značky 1 / 5 / 20 min;
  - potom lineárne hodiny 6 / 12 / 18 / 24 h;
  - medzi pásmami značka prerušenia `//`.
- Krivky:
  - bežná H₂ voda klesne na ~12 % pri 20 min a na 0 do 2 h;
  - MILUJ (cieľ dodávateľa) 100 → 82 % za 24 h, čiarkovaná zlatá.
- Text pod grafom vždy hovorí, že 24 h je **cieľ dodávateľa** a krivka je ilustračná.

## 4. Podstránka `/water` (`water/index.html`): „What makes water alive?“

Sekcie v poradí:
1. **Hero:** `w1_spring.webp` (prameň s vírom v džungli), logo, „← Back to MILUJ“.
2. **How much of you is water?** **Len údaj 99 % všetkých molekúl** (Freitas, *Nanomedicine*, 1999). Martin si **neželá** percentá podľa hmotnosti (muži, ženy, novorodenci).
3. **Same atoms. Different order.**
   - Obrázok `w2_carbon.webp` (ceruzka a diamant).
   - Pinned 3D canvas: jedna sada 72 častíc sa mení grafit → diamant → bežná voda (s vodíkovými väzbami) → **štruktúrovaná/EZ voda ako mriežka rovnaká ako pri diamante** (kyslíky v tetraédrickej mriežke ako ľad, 2 vodíky na kyslík, zlaté vodíkové väzby).
   - Popisok pod animáciou poctivo hovorí, čo je reálna geometria a čo zjednodušenie.
4. **Purity vs. structure:** citát.
5. **Štvrté skupenstvo (Pollack)** (`#fourth-phase`):
   - SVG diagram: povrch → usporiadaná zóna (−) → bežná voda (+) → IR svetlo;
   - 4 karty: vodomilné povrchy, náboj ako batéria a LED, prúdenie bez pumpy (Nafion, 2013), vodný most v elektrickom poli (Fuchs, TU Graz, 2007);
   - boxy: Mu Shik Jhon (hypotéza) a „How to read this“ (diskusia, difúzioforéza).
6. **Schauberger** (`#schauberger`):
   - text a box „Living vs. dead water“ (jeho pohľad, ktorý chce MILUJ zmerať);
   - box o Schwenkovi (*Sensitive Chaos*, 1962; *Wirbel* = stavec aj vír);
   - canvas s vírom a pod ním statický diagram „víry vo víroch“ (SVG).
7. **Mitochondrie** (`#mitochondria`): „Life runs on hydrogen and water.“
   - Canvas diagram vnútornej membrány:
     - elektróny (zlaté) tunelujú cez komplexy I, III a IV;
     - protóny (svetlo modrosivé) idú po vodných reťaziach (Grotthuss);
     - ATP syntáza sa otáča;
     - z kyslíka vzniká voda (**sýto modrá #3D8BFF**);
     - •OH a H₂.
   - Častice sú zväčšené.
   - Pod diagramom 5 krokov a boxy „H₂ (emerging research, Ohsawa 2007)“ a „Why this matters to MILUJ“.
8. **Vodík a graf** (`#hydrogen`), pozri vyššie.
9. **Jeden pohár** (`#glass`): `w3_glass.webp`, Pure / Structured / Hydrogen-saturated, „How we will check it“.
10. **Fascie: „Rivers inside you.“** (`#fascia`):
    - intersticium 2018 a hyaluronan;
    - Schleip 2012;
    - „na akej vode záleží“ (pohľad MILUJ + meranie bioimpedanciou);
    - SVG sieť riečišť s tečúcimi kvapkami;
    - čísla ≈ 10 L / ≈ 3 h / 1 web;
    - karty Guimberteau, tensegrita, zmyslová sieť;
    - box „Drinking alone is not enough“ (pohyb).
11. **Tri šošovky + zdroje** (`#science`, svetlé pozadie). Odkazy: NCBI, Freitas, PMC štruktúra vody, arXiv EZ review, Pollack lab 2013, TU Graz vodný most, PKS Schauberger, Page 1999 tunelovanie, MRC ATP syntáza, Ohsawa 2007, NIH H₂ review, Benias 2018, fascia/hyaluronan.
12. **Záver:** „Water is the medium of life.“ + tlačidlo späť na úvodnú stránku.

## 5. Dizajn systém

- **Farby:**
  - `--night #0B0E0C`, `--forest #121813`, `--ivory #F5EFE2`, `--paper #FBF8F1`, `--gold #C2A25E`, `--gold-2 #E3CC94`;
  - voda a vodík `#9FC7D2`, sea `#0A1B22`, reštaurácia `#17110C`, mitochondrie `#0D1311`.
- **Fonty:** Cormorant Garamond (display) + Jost (text); Noto Serif Armenian pre kruhy textu.
- **Typografia:**
  - `--fs-h2: clamp(40px,5vw,72px)`, `--fs-h3: clamp(28px,2.6vw,38px)`;
  - lead 20, text 17 (mobil 16), malý 14, nič pod 13 px;
  - štítky v sentence case (15 px); zlatá kurzíva len v hero h1.
- **Easing:** `--ease-out: cubic-bezier(.23,1,.32,1)`.
- **Výkonnostné pravidlá (dodržiavať):**
  - zapisovať štýly a text len pri zmene (žiadne `textContent` každý frame);
  - tlmenie nezávislé od fps: `k = 1 - Math.exp(-dt*7.7)`;
  - animovať len transform a opacity;
  - canvasy kresliť len keď sú viditeľné (IntersectionObserver);
  - podporovať `prefers-reduced-motion`;
  - `[hidden]` vynútiť cez `!important`;
  - scroll-scrub videá načítať cez `fetch → blob → objectURL`;
  - kódovanie scrub videí: `-g 6 -keyint_min 6 -sc_threshold 0 -an -movflags +faststart`.

## 6. Higgsfield (Martinov účet je pripojený)

- **Obrázky:** model `gpt_image_2_5`, quality high, 2k.
  - Štýl: teplé zlaté svetlo, prírodné materiály, fotoreal, film grain, tváre odvrátené, bez textu a log.
- **Videá:** `minimax_h3_max` so start/end frame, 5 s. Treba `declined_preset_id: 24bae836-2c4a-48e0-89b6-49fcc0b21612`.
- **Prenos do workspace:**
  - `sandbox_exec` s `image_paths` (≤ 512 KiB na volanie);
  - lokálny blob v `tool-results/` → overiť sha256 → webp.
  - Upload z workspace do Higgsfield je zablokovaný proxy.
- **ID novších obrázkov:**
  - `w1_spring` afab1193, `w2_carbon` 0598e2ba, `w3_glass` df48cebd;
  - ostatné (H₂ bazén, praktiky v2, reštaurácia r1–r3, logo) nájdeš cez `show_generations` (19.–23. 10.).
- **Staršie ID** (filmy, praktiky, science track) sú v pôvodnom odovzdaní z 19. 10.:
  - film master upload `a713fc56-d52c-46f9-9a2f-b44850a5a3bb`;
  - 100 000 master `6935771c-467b-42ae-9e09-f56a98d9cf5f`;
  - praktiky: Vinyasa 13a064bb, Breathwork 985159c5, Sound a8422ea6, Dance c2a98a8e, Energy 8d479339, Constellations e2832d02, Shadow 2bc8e463, Kundalini 8cbd4b11, Cacao d07e41c8, Gene Keys 7013e59f;
  - science track: Hydrogen a2efd228, Mud c51d99f5, Salt 01dd43a2, Sound e6fc1fa1, Healy 25730954, Light c8c2dd8e, Dark 243216e5, Blood 8781cb6f.

## 7. Poctivý jazyk (dohodnuté pravidlá)

- **Tri šošovky:**
  - ●●● Established physiology;
  - ●●○ Emerging research;
  - ●○○ MILUJ exploration.
- **Bez zdravotných sľubov.** Silné tvrdenia („zázraky“, „neštruktúrovaná voda berie energiu“, „živá voda“) sa podávajú ako pohľad Schaubergera alebo MILUJ, ktorý sa bude **merať a nezávisle overovať**.
- **24 h retencia H₂** je vždy „supplier-stated target“.
- **EZ voda a štvrté skupenstvo:** pozorovania Pollackovho labu, vo vede diskutované.
- **Vedome vynechané** z Martinových podkladov (video „Lekce 1“):
  - „hlavnou úlohou nervov je vedenie zvuku“ (len menšinová hypotéza, Heimburg a Jackson);
  - rakovinové bunky a cymatika;
  - hudba omladzuje krvinky;
  - myšlienky menia vodu v tele;
  - fascie sa natiahnu o 70 %.
  - Chladniho obrazce a frekvencie by sa hodili skôr k izbám na úvodnej stránke.
- **Stránka dianasiswartonova.cz** blokuje automatické čítanie (robots). Ak ju chceme použiť, Martin musí vložiť text.

## 8. Doména: prepnutie z ChatGPT Sites na GitHub Pages (zatiaľ NEROBIŤ)

Spraviť až keď budú hotové všetky podstránky.

**DNS je vo WEDOS (`julimvision.com`). Dnes:**
- `miluj CNAME custom-domains.chatgpt.site`;
- TXT `_openai-site-verification.miluj`;
- TXT `_cf-custom-hostname.miluj`.

**Postup:**
1. V repo pridať súbor `CNAME` s obsahom `miluj.julimvision.com` (alebo nastaviť Custom domain v GitHub → Settings → Pages).
2. Vo WEDOS zmeniť `miluj CNAME` na `martinsiladi-spec.github.io`.
3. Zmazať oba ChatGPT TXT záznamy.
4. Po overení zapnúť v GitHube „Enforce HTTPS“.
5. Pozor na relatívne cesty: dnes web beží pod `/miluj-web/`, po prepnutí v koreni domény. Odkazy sú relatívne (`water/`, `../`, `assets/`), takže fungujú v oboch prípadoch.

## 9. Otvorené úlohy

1. **Prerobiť `/temple-houses`** v štýle úvodnej stránky (pôvodný obsah prečítať v paneli prehliadača).
2. Rozhodnúť o **SK/ES verziách** (`/sk`, `/es`) a prípadne preložiť.
3. **Prepnúť doménu** (bod 8).
4. Otvorené otázky od Martina:
   - ktorý z 22 domov na mape nie je Temple House (web hovorí 21);
   - funkcia bazéna (bod 2 mapy);
   - roky do časovej osi „Journey“;
   - čo presne znamenajú „soli“;
   - masterplan vo vyššom rozlíšení (≥ 4 000 px).
5. Ponúknuté a neurobené: prelet celým areálom (skica → 3D → realita).
6. Neskôr možno: investorská prezentácia namiesto formulára; Chladni / frekvencie k izbám.
