# MILUJ Sanctuary – odovzdanie na pokračovanie (stav 23. 10. 2026)

Tento dokument stačí na pokračovanie v novej relácii. **Zdroj pravdy je GitHub repozitár** `martinsiladi-spec/miluj-web`. Starý artefakt-prototyp je už len archív a náčrtník.

---

## 1. Kontext

- **Klient:** Martin (martin.siladi@gmail.com).
  - Komunikácia **po slovensky**. **Od 24. 10. je smerodajná slovenská verzia webu**; angličtina a španielčina sa z nej prekladajú.
  - Starý web má aj verzie `/sk` a `/es`.
- **Projekt:** MILUJ Sanctuary, healing & retreat centrum na Bali (Karangasem):
  - Ascension Pyramid a podzemná zvuková sála;
  - 22 Temple Houses („coded accommodation“), každý s iným zameraním na liečenie;
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
- **`sk/index.html` a `sk/water/index.html` sú zdroj (od 24. 10.).** Všetky zmeny textu aj kódu sa robia **len tu**.
- `index.html`, `water/index.html` (angličtina, koreň webu) a `es/index.html`, `es/water/index.html` sa **generujú zo slovenčiny. Needitovať ručne.**
- `tools/i18n_strings.py` (úvodná stránka) a `tools/i18n_water.py` (podstránka voda): preklady, riadok = (angličtina, **slovenčina presne ako na stránke = kľúč**, španielčina). Ak sa rovnaký slovenský text na jednej stránke prekladá dvoma spôsobmi, treba slovenčinu rozlíšiť (napr. „Pure“ = „Prečistená“, „Clean“ = „Čistá“).
- `tools/build_i18n.py`: generátor. Po každej zmene slovenského textu doplniť/upraviť riadok (EN a ES preložiť kvalitne, nie strojovo) a spustiť `python3 tools/build_i18n.py`. Skript vypíše všetko, čo nie je preložené (a skončí chybou), aj riadky, ktoré už na stránke nie sú.
- `tools/jsstrings.py`: pomocník, vypíše texty zo skriptu stránky.
- `CNAME` (`miluj.julimvision.com`, od 24. 10.), `404.html` (presmeruje na úvod v jazyku adresy) a `temple-houses/`, `sk/temple-houses/`, `es/temple-houses/` (staré adresy z ChatGPT Sites → sekcia `#grounds`).

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
4. Overiť naživo v paneli prehliadača: najprv `request_access` na `https://miluj.julimvision.com` (po prepnutí DNS; dovtedy github.io presmeruje na starý web), potom `navigate`. Workspace sám na github.io nedosiahne.

## 3. Úvodná stránka (`index.html`): poradie sekcií

**Jazyky (23. 10.):** hore vpravo v hero je prepínač **EN · SK · ES** (`.lang`). EN = `/`, SK = `/sk/`, ES = `/es/`. V hlavičke sú `hreflang` odkazy s plnou adresou `https://martinsiladi-spec.github.io/miluj-web/…` – **pri prepnutí domény ich treba zmeniť** v `index.html` a znova spustiť generátor. Podstránka o vode je tiež v troch jazykoch (`/water/`, `/sk/water/`, `/es/water/`), prepínač má v hornej lište vedľa „Back to MILUJ“ (na mobile len prepínač). Vlastné mená ostávajú: MILUJ, Temple House(s), Ascension Pyramid, Vinyasa, Breathwork, Gene Keys. SK vykanie, ES tykanie.

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

23. 10. (večer) preusporiadaná podľa Martinovho zadania do **8 krokov s jasnou postupnosťou**. Hlavná myšlienka hneď v úvode: **v MILUJ sa štruktúrovanie vody a obohatenie molekulárnym vodíkom vždy prepájajú – jedna voda na pitie aj do bazéna.** Vodík je vysvetlený PRED animáciou pitia. Pod hero je **sticky navigácia** (`.wnav`, 8 položiek, zvýrazňuje aktuálnu sekciu; pinned scény majú `top: var(--navh)`).

0. **Hero:** `w1_spring.webp`, nad nadpisom štítok „What makes water alive?“, nadpis **„We are water.“**, lead „And we become the water we drink…“ (~2 h, Péronnet 2012) + prečo štruktúrovaná a vodíková voda. Ľavá strana fotky stmavená kvôli čitateľnosti.
1. **Filozofia** (`#philosophy`): „One water. Two qualities.“ Dva piliere s veľkými fotkami s mäkkým okrajom: Structured = vír `w4_vortex`, Hydrogen-rich = Martinova fotka fľaše s bublinkami `p_hydrogen`. Dve použitia: To drink (`p_drink`, výrez z `w3_glass`), To bathe in (`p_pool`, výrez z `t11_h2pool`). Všetko klikateľné na príslušné kroky.
2. **Prečo voda** (`#body`): 99 % molekúl (Freitas) + veta, prečo MILUJ začína vodou.
3. **Krok 1 · Štruktúrovanie** (`#structure` → `#atoms` → `#order`): grafit/diamant, 3D častice; potom „Structured water that gathers itself.“ – 6 myšlienok s malými zlatými symbolmi (250 px, tmavé čiary na #C2A25E), aj pri 05 špirála. Box „How to read this“ Martin 24. 10. zrušil; texty sekcií „Why water“, „Same atoms“ a „Structured water“ prepísané podľa neho. Sekcia Vodík (24. 10.): nadpis „Molecular hydrogen, its effects and its stability in water.“, odsek o •OH a blok „What the studies showed“ (`.h2-studies`, 7 overených štúdií s odkazmi v Research context). Parkinson (Yoritaka 2013) vynechaný, lebo veľká štúdia (178 pacientov) účinok nepotvrdila; kognitívna štúdia 2021 sa nedala dohľadať. Čaká sa na čiernobielu fotku Viktora Schaubergera (dodá Martin) do bloku „In motion · Viktor Schauberger“.
4. **Krok 2 · Vodík** (`#hydrogen`): H₂O vs H₂ (symbol), 3 karty (najmenšia molekula / rýchlo uniká / systém MILUJ ho drží – patentovaný retenčný systém, podľa dodávateľa až 24 h), graf.
5. **Spojenie** (`#process`, svetlé pozadie): Clean → Structured → Hydrogen-rich → To drink / To bathe in.
6. **Voda, ktorú pijeme** (`#drink` + `#journey` + `#journeyScene`): pohár `w3_glass` (Pure / Structured / Hydrogen-saturated, „Where you find it“), potom animácia cesty pohára (postava → fascie → bunka → mitochondria).
7. **Voda, do ktorej vstupujeme** (`#pool`): `t11_h2pool`, 3 body (rovnaká voda, vodíková časť, súčasť dňa), „Through the skin, not the gut.“ + štúdia 2023 (H₂ z kúpeľa v krvi do 2 min, zvieratá, ●●○).
8. **Zhrnutie** (`#science`, svetlé): „What MILUJ brings together.“ (6 bodov), tri šošovky (tretia = „MILUJ approach“), zdroje v `<details>`, záver.

Kód: CSS bloky `/* step navigation */`, `/* 1 · philosophy */` … `/* 8 · summary list */`; symboly generované ako inline SVG 500×500.

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
- **Opis vybavenia bez „budeme merať/overovať“** (Martin 23. 10.): web opisuje, čo MILUJ má a ako to funguje; vedecký výskum ostáva ako vysvetľujúci kontext so šošovkami.
- **Bez zdravotných sľubov.** Silné tvrdenia („zázraky“, „neštruktúrovaná voda berie energiu“, „živá voda“) sa podávajú ako pohľad Schaubergera alebo MILUJ, ktorý sa bude **merať a nezávisle overovať**.
- **24 h retencia H₂** je vždy uvedená ako špecifikácia dodávateľa.
- **EZ voda a štvrté skupenstvo:** pozorovania Pollackovho labu, vo vede diskutované.
- **Vedome vynechané** z Martinových podkladov (video „Lekce 1“):
  - „hlavnou úlohou nervov je vedenie zvuku“ (len menšinová hypotéza, Heimburg a Jackson);
  - rakovinové bunky a cymatika;
  - hudba omladzuje krvinky;
  - myšlienky menia vodu v tele;
  - fascie sa natiahnu o 70 %.
  - Chladniho obrazce a frekvencie by sa hodili skôr k izbám na úvodnej stránke.
- **Stránka dianasiswartonova.cz** blokuje automatické čítanie (robots). Ak ju chceme použiť, Martin musí vložiť text.

## 8. Doména: prepnutie z ChatGPT Sites na GitHub Pages (spustené 24. 10.)

**V repe hotové 24. 10.:** `CNAME`, `hreflang` a `og:image` s plnou adresou `https://miluj.julimvision.com/…`, presmerovania starých adres, `404.html`. Od tejto chvíle `martinsiladi-spec.github.io/miluj-web/` presmeruje na `miluj.julimvision.com`.
**24. 10. večer:** DNS vo WEDOS prepnuté (zóna 2026102402, `miluj CNAME martinsiladi-spec.github.io`, ChatGPT TXT zmazané). Web beží na `http://miluj.julimvision.com/` vo všetkých jazykoch, presmerovania aj 404 fungujú. **Zostáva:** po vydaní certifikátu zaškrtnúť **Enforce HTTPS** v GitHub → Settings → Pages.
**Problém (24. 10., 23:40):** jeden DNS server WEDOS (odpovedá z IP `75.2.92.86`) stále posiela starú zónu `2026100302` (CNAME na ChatGPT), druhý (`45.138.106.1`) novú `2026102402`. Návštevníci náhodne vidia starý alebo nový web a GitHub nevie vydať certifikát. Martin má kontaktovať podporu WEDOS (vynútiť synchronizáciu zóny). Overenie: `dns.google/resolve?name=julimvision.com&type=SOA&cd=1` opakovane, porovnať serial a „Comment“. Starý web na ChatGPT Sites zatiaľ nevypínať.

**DNS je vo WEDOS (`julimvision.com`). Dnes:**
- `miluj CNAME custom-domains.chatgpt.site`;
- TXT `_openai-site-verification.miluj`;
- TXT `_cf-custom-hostname.miluj`.

**Postup:**
1. V repo pridať súbor `CNAME` s obsahom `miluj.julimvision.com` (alebo nastaviť Custom domain v GitHub → Settings → Pages).
2. Vo WEDOS zmeniť `miluj CNAME` na `martinsiladi-spec.github.io`.
3. Zmazať oba ChatGPT TXT záznamy.
4. Po overení zapnúť v GitHube „Enforce HTTPS“.
5. ~~Zmeniť `hreflang` adresy~~ (hotové 24. 10.).
6. Pozor na relatívne cesty: dnes web beží pod `/miluj-web/`, po prepnutí v koreni domény. Odkazy sú relatívne (`water/`, `../`, `assets/`), takže fungujú v oboch prípadoch.

## 9. Otvorené úlohy

1. ~~Prerobiť `/temple-houses`~~: Martin 23. 10. rozhodol, že **podstránku Temple Houses zatiaľ nerobíme**, stačí sekcia Grounds na úvodnej stránke.
2. ~~SK/ES verzie úvodnej stránky~~: hotové 23. 10. (generátor `tools/build_i18n.py`). Podstránka `/water` preložená tiež (23. 10. večer).
3. **Doména prepnutá** 24. 10. (bod 8); zostáva Enforce HTTPS po vydaní certifikátu.
4. Odpovede od Martina (23. 10., zapracované na webe):
   - **všetkých 22 domov sú Temple Houses**, každý s iným zameraním na liečenie;
   - **bazén** je zásobený vodou systému, jeho časť je vodíková, liečenie prebieha aj cez pokožku pri pobyte v bazéne;
   - **soli = minerálne soli** na doplnenie minerálov v tele (karta v Science track prepísaná, ●●● Established physiology).;
   - stále otvorené: roky do časovej osi „Journey“, masterplan vo vyššom rozlíšení (≥ 4 000 px).
   - obrázok `sc2_salt` vymenený za sypajúcu sa minerálnu soľ (Higgsfield 9ea4ee39).
5. Ponúknuté a neurobené: prelet celým areálom (skica → 3D → realita).
6. Neskôr možno: investorská prezentácia namiesto formulára; Chladni / frekvencie k izbám.

## Výkon (24. 10.)
- Merané Lighthouse a vlastným testom plynulosti (scroll na simulovanom slabšom telefóne, CPU ×4). Skripty nie sú v repe; postup: lokálny `python3 -m http.server`, Lighthouse 12, Playwright.
- Videá na úvode sa nesťahujú pri štarte: `film.mp4` až po udalosti `load`, `crowd.mp4` až keď je sekcia misie do 2 obrazoviek.
- Slova okolo domu (`buildRings`) sa merajú až keď sa blíži sekcia `#grounds`.
- Hlavná slučka úvodu preskakuje sekcie ďaleko od obrazovky a CSS premenné zapisuje len pri zmene.
- Plátna (canvas) na mobile (šírka < 700 px) kreslia v rozlíšení 1,5× namiesto 2×.
- Podstránka voda: postava v animácii (`assets/j_body.webp`, 768 × 1152, čierne pozadie) sa načíta až pri priblížení a jej čierne pozadie sa po kúskoch premení na priehľadnosť; vinetácia okrajov animácie je CSS (`.j-canvas::after`, jednotky `cqmin`), nie kreslenie v každom snímku.

## 10. Nový úvod a neverejná kópia (25. 10.)

- **Nový úvod je na zverejnenom webe** (všetky jazyky, zdroj `sk/index.html`): pyramída viditeľná hneď (malý vložený náhľad `.hero .bg::before`, ostrá fotka sa prelína cez ňu), nadpis sa odhaľuje pomaly slovo po slove s rozostrením (slová rozdeľuje prehliadač, takže preklady nadpisu ostávajú celé; kým sa nerozdelí, je skrytý cez `.js .hero h1:not(.split)`), text pod ním ~3,5 s, tlačidlo ~4,3 s, výzva ~5,1 s.
- **Matné sklo v štýle Apple** nad filmom a scénou misie (`.glass`, `.pill` „Pripravujeme film / scénu“, EN „Preparing the film / scene“, ES „Preparando la película / escena“): videá sa sťahujú s priebehom, sklo sa čistí podľa stiahnutého podielu a pri načítaní zmizne. Film štartuje až po načítaní fotky pyramídy (najneskôr po 2,5 s), dav hneď po filme alebo skôr, ak je návštevník blízko.
- Martin to vybral v slepom teste A/B (verzia so sklom) a schválil na neverejnej kópii.
- **Neverejná kópia na kontrolu pred zverejnením:** `python3 tools/make_staging.py VÝSTUP` → `VÝSTUP/site/…` (aktuálny stav repa, noindex, odkazy na priečinky → `index.html`) a publikovať ako súkromný artefakt (rozcestník + `site/…`). Doterajšia kópia: https://claude.ai/artifact/P57c4BNTKxYBPn3QmCTcEF.
- **Kópia na hostingu WEDOS** (`julimvision.com/miluj-web/miluj/`) je statická – nový úvod tam bude až po nahraní nového ZIPu.
