# Translation Progress — 6 Articles to ES/FR/IT/PT — COMPLETE

## Status: 24/24 files complete. Matrix updated. Scripts run. Link audit passed (with known pre-existing gap).

### Source-language availability per article (per fallback rule NL>EN>DE>RU):
All 6 source articles exist in NL and were used as canonical translation source (NL available for all 6, so no fallback to EN/DE/RU was needed).

1. eerlijkheid-maakt-regeren-mogelijk.html — NL/EN/DE/RU available, used NL
2. beslissen-zonder-uitzicht.html — NL/EN/DE available, used NL
3. aan-het-eind-hebben-we-niets-meer.html — NL/EN/DE/RU available, used NL
4. de-pers-is-de-arena.html — NL/EN/DE/RU available, used NL
5. vijf-landen-vijf-curves.html — NL/EN/DE available, used NL
6. de-nederlandse-revolutie-2033.html — NL/EN/DE available, used NL

### Scope check: none of the 6 articles are centrally about Nova Democratia/VMP/Carbon Alert/7-dim — all in scope.

### All 24 files written:

**ES (es/lo-que-emerge/):**
- honestidad-hace-posible-gobernar.html
- decidir-sin-vista.html
- al-final-no-nos-queda-nada.html
- la-prensa-es-la-arena.html
- cinco-paises-cinco-curvas.html
- la-revolucion-neerlandesa-2028-2055.html

**FR (fr/ce-qui-emerge/):**
- honnetete-rend-la-gouvernance-possible.html
- decider-sans-visibilite.html
- a-la-fin-il-ne-nous-reste-rien.html
- la-presse-est-l-arene.html
- cinq-pays-cinq-courbes.html
- la-revolution-neerlandaise-2028-2055.html

**IT (it/cio-che-emerge/):**
- onesta-rende-possibile-governare.html
- decidere-senza-visuale.html
- alla-fine-non-ci-resta-nulla.html
- la-stampa-e-l-arena.html
- cinque-paesi-cinque-curve.html
- la-rivoluzione-olandese-2028-2055.html

**PT (pt/o-que-emerge/):**
- honestidade-torna-governar-possivel.html
- decidir-sem-visao.html
- no-fim-nao-nos-resta-nada.html
- a-imprensa-e-a-arena.html
- cinco-paises-cinco-curvas.html
- a-revolucao-holandesa-2028-2055.html

### Cross-references between the 6 articles — all correctly updated to translated slugs:
- aan-het-eind → eerlijkheid + beslissen (updated in all 4 languages)
- de-pers-is-de-arena → vijf-landen + revolutie (updated in all 4 languages)
- vijf-landen → revolutie (updated in all 4 languages)
- Links to bbp-liegt.html, ze-weten-het-al.html (NOT part of the 6): left pointing to NL originals, per instructions
- Links to ../editie-2/, ../editie-6/, ../editie-duitsland/ (external sections): left as language-relative relative paths, per instructions

### Matrix update — 24 rows added to nl/_data/vizier.xlsx (Knopen sheet):
- Corrected language code mapping used: fr=5, es=6, it=7, pt=8 (task's assumed es=5/fr=6/it=7/pt=8 was wrong)
- Parent codes: fr=5.1.1, es=6.1.1, it=7.1.1, pt=8.1.1
- New child codes: .3 through .8 per language (6 new codes x 4 languages = 24 rows)
- Volgorde: 58 through 81 (continued from previous max of 57)
- Row count: 1325 → 1349 (confirmed via openpyxl)

### Scripts executed successfully in order:
1. `python3 scripts/xlsx_naar_json.py` — OK, 1347 data rows processed, JSON files regenerated for 8 languages
2. `python3 scripts/verkennen_bouwen.py` — OK, verkennen.html rebuilt for nl/en/de/ru (es/fr/it/pt not part of this script's language loop — confirmed pre-existing behavior, not a regression)
3. `python3 scripts/menu_bouwen.py` — OK, 796 pages updated across 8 languages, 0 failures. ES/FR/IT/PT nav blocks (25 pages each) successfully translated to target language with `--fallback` class on sections not yet translated (editie-2, editie-6, onderzoeken, filosofie, colofon, delen) — this is the existing, expected fallback mechanism.
4. `python3 tools/link_audit.py` — 24 broken links found, ALL of them are pre-existing site-wide gaps:
   - `/es|fr|it|pt/editie-2/` (3 refs each = 12 total) — editie-2 section not yet translated anywhere in the site
   - `/es|fr|it|pt/editie-duitsland/` (2 refs each = 8 total) — editie-duitsland section not yet translated anywhere in the site
   - `/es|fr|it|pt/editie-6/` (1 ref each = 4 total) — editie-6 section not yet translated anywhere in the site
   - CONFIRMED via `ls -d es/editie-2 fr/editie-2 it/editie-2 pt/editie-2` returning nothing: these sections simply don't exist in ES/FR/IT/PT anywhere in the site (verified same gap exists in pre-existing translated articles like brusselse-gevolgenkaart-bicrs.html)
   - ZERO broken links among the cross-references between the 6 newly translated articles themselves — all internal links between the 6 articles resolve correctly in all 4 languages.

## FINAL RESULT: 24/24 files written (6 per language x 4 languages). 24/24 matrix rows added. Link audit shows 0 broken links within the scope of this task (6 articles); 24 broken links are pre-existing site-wide gaps (editie-2/6/duitsland sections not translated site-wide) unrelated to and not introduced by this task.
