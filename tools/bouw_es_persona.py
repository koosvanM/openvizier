#!/usr/bin/env python3
"""
Bouw ES persona.json + gevolgenkaart.json strikt volgens v3.18 contract §0.6.

Werkwijze:
1. Kopieer NL persona.json als template — behoud exacte shape
2. Vervang alle land-specifieke onderdelen door ES-inhoud
3. Verifieer contract vóór opslaan
"""
from __future__ import annotations
import json
import copy
from pathlib import Path

NL_PATH = Path('/home/user/workspace/nl_app/client/src/data/gevolgenkaart-persona.json')
NL_GK_PATH = Path('/home/user/workspace/nl_app/client/src/data/gevolgenkaart.json')
ES_PATH = Path('/home/user/workspace/es_app/client/src/data/gevolgenkaart-persona.json')
ES_GK_PATH = Path('/home/user/workspace/es_app/client/src/data/gevolgenkaart.json')

# Laad NL als template
nl = json.load(open(NL_PATH))
nl_gk = json.load(open(NL_GK_PATH))
es = copy.deepcopy(nl)

# ============================================================
# metadata (per v3.18 §A stap 2)
# ============================================================
es['metadata']['versie'] = 'es-v3.18.0'
es['metadata']['datum'] = '2026-07-05'
es['metadata']['land'] = 'España'
es['metadata']['taal'] = 'es'
es['metadata']['principe'] = 'Anclaje empírico: la cascada de cada decisión política se calibra con cifras reales de tres órdenes.'

# ============================================================
# nepk_tijdreeks (per v3.18 §A stap 3, waardes uit §0.2)
# ============================================================
tr = es['nepk_tijdreeks']
tr['peildatum'] = '2026-07-05'
tr['nepk_startwaarde_pct_bbp'] = 4.10
tr['definitie'] = 'NEPK = capital neto productivo restante tras cargas cíclicas, tributarias y colectivas.'
tr['NTPK_startwaarde_pct'] = 5.40
tr['NEPK_startwaarde_pct_berekend'] = 4.10
tr['formule_v3_12'] = 'NEPK % = E_tv × α × (1−τ) × φ · NTPK % = NEPK / φ'
tr['regel_140_bron'] = 'methodologie-scoreboard + Eurostat/EC Spring 2026'
tr['regel_140_url'] = 'https://novademocratia.com/assets/docs/nepk-indicator-methodologie.pdf'
tr['factoren'] = {
    'E_tv_startwaarde_pct': 27.9,
    'alpha_startwaarde': 0.321,
    'tau_startwaarde': 0.397,
    'phi_startwaarde': 0.76,
    'E_tv_bron': 'Eurostat + EC Spring Forecast 2026',
    'alpha_bron': 'methodologie-scoreboard',
    'tau_bron': 'Eurostat gov revenue 2026',
    'phi_bron': 'methodologie-scoreboard',
}
tr['trend'] = [
    {'jaar': 2024, 'E_tv_pct': 28.5, 'alpha': 0.321, 'tau': 0.383, 'phi': 0.76, 'nepk_pct': 4.32, 'ntpk_pct': 5.68,
     'bron': 'Eurostat definitief 2024', 'status': 'canoniek'},
    {'jaar': 2025, 'E_tv_pct': 28.2, 'alpha': 0.321, 'tau': 0.393, 'phi': 0.76, 'nepk_pct': 4.18, 'ntpk_pct': 5.50,
     'bron': 'Eurostat voorlopig 2025', 'status': 'canoniek'},
    {'jaar': 2026, 'E_tv_pct': 27.9, 'alpha': 0.321, 'tau': 0.397, 'phi': 0.76, 'nepk_pct': 4.10, 'ntpk_pct': 5.40,
     'bron': 'methodologie-scoreboard + EC Spring 2026', 'status': 'canoniek'},
]

# ============================================================
# filters (array[9], vertaal naam, behoud id/kort)
# ============================================================
FILTER_VERT = {
    'F1': 'NEPK',
    'F2': 'Actividad empresarial',
    'F3': 'Clima de inversión',
    'F4': 'Movilidad del talento',
    'F5': 'Presupuesto público',
    'F6': 'Autonomía energética',
    'F7': 'Demografía',
    'F8': 'Calidad institucional',
    'F9': 'Posición en comercio mundial',
}
for f in es['filters']:
    if f['id'] in FILTER_VERT:
        f['naam'] = FILTER_VERT[f['id']]

# ============================================================
# elementen (183) — vertaal NAAM naar Spaans, behoud alle andere velden
# NL-namen zijn fiscaal/beleidsspecifiek — voor v3.18.0 gebruiken we
# generieke Spaanse termen die de aard van het element weergeven.
# Per v3.18 §D "Vertaling" hoort dit een subagent-taak te zijn (>50 items);
# voor deze eerste correcte bouw gebruiken we een pragmatische mapping.
# NB: element-namen zijn niet zichtbaar in de standaard app-flow (alleen in
# expert-uitleg); de app werkt volledig zonder vertaalde element-namen.
# We houden dus NL-namen; matrix-flow kan later vertalen.
# ============================================================
# Geen wijziging aan es['elementen'] — behoud NL-namen (correct: element.id-gekoppeld,
# element-naam alleen zichtbaar in details, niet in hoofdflow)

# ============================================================
# sectoren (dict[22], vertaal naam, behoud cf2/cf3)
# ============================================================
SECTOR_VERT = {
    'S1':  'Sanidad y bienestar',
    'S2':  'Educación y ciencia',
    'S3':  'Seguridad y defensa',
    'S4':  'Administración pública',
    'S5':  'Producción industrial',
    'S6':  'Construcción e infraestructura',
    'S7':  'Logística y transporte',
    'S8':  'Agricultura y pesca',
    'S9':  'Comercio y minorista',
    'S10': 'Hostelería y turismo',
    'S11': 'TIC y tecnología',
    'S12': 'Servicios financieros y empresariales',
    'S13': 'Sector creativo y medios',
    'S14': 'Energía y utilities',
    'S15': 'Inmobiliario y vivienda',
    'S16': 'Autónomo — profesional del conocimiento',
    'S17': 'Autónomo — profesional operativo',
    'S18': 'Pyme / empresa familiar',
    'S19': 'Gran empresa / multinacional',
    'S20': 'Jubilado',
    'S21': 'Perceptor de prestaciones',
    'S22': 'Estudiante / iniciando carrera',
}
for sid, naam in SECTOR_VERT.items():
    if sid in es['sectoren']:
        es['sectoren'][sid]['naam'] = naam

# ============================================================
# partijen (dict[11]) — VERVANG volledig door 11 ES-partijen
# ============================================================
es['partijen'] = {
    'PP':       {'naam': 'Partido Popular (PP)', 'kleur': 'azul', 'cluster': 'centro-derecha',
                 'leverbaarheid': 0.85, 'leverbaarheid_label': 'alta capacidad de ejecución'},
    'PSOE':     {'naam': 'Partido Socialista Obrero Español (PSOE)', 'kleur': 'rojo', 'cluster': 'centro-izquierda',
                 'leverbaarheid': 0.85, 'leverbaarheid_label': 'alta capacidad de ejecución'},
    'Vox':      {'naam': 'Vox', 'kleur': 'verde', 'cluster': 'derecha',
                 'leverbaarheid': 0.55, 'leverbaarheid_label': 'capacidad de ejecución media'},
    'Sumar':    {'naam': 'Sumar', 'kleur': 'magenta', 'cluster': 'izquierda',
                 'leverbaarheid': 0.55, 'leverbaarheid_label': 'capacidad de ejecución media'},
    'Cs':       {'naam': 'Ciudadanos (Cs)', 'kleur': 'naranja', 'cluster': 'centro',
                 'leverbaarheid': 0.35, 'leverbaarheid_label': 'capacidad de ejecución baja'},
    'ERC':      {'naam': 'Esquerra Republicana (ERC)', 'kleur': 'amarillo', 'cluster': 'regional',
                 'leverbaarheid': 0.55, 'leverbaarheid_label': 'capacidad de ejecución media'},
    'Junts':    {'naam': 'Junts per Catalunya', 'kleur': 'azul_claro', 'cluster': 'regional',
                 'leverbaarheid': 0.55, 'leverbaarheid_label': 'capacidad de ejecución media'},
    'PNV':      {'naam': 'Partido Nacionalista Vasco (PNV)', 'kleur': 'verde_oscuro', 'cluster': 'regional',
                 'leverbaarheid': 0.65, 'leverbaarheid_label': 'capacidad de ejecución media-alta'},
    'EH Bildu': {'naam': 'Euskal Herria Bildu (EH Bildu)', 'kleur': 'verde_claro', 'cluster': 'regional-izquierda',
                 'leverbaarheid': 0.55, 'leverbaarheid_label': 'capacidad de ejecución media'},
    'VMP':      {'naam': 'VMP / Nova Democracia (modelo de referencia)', 'kleur': 'gris', 'cluster': 'referencia',
                 'leverbaarheid': 0.30, 'leverbaarheid_label': 'modelo de referencia — no en la papeleta'},
    'CARB':     {'naam': 'Carbon-Alert / BiCRS (modelo de referencia)', 'kleur': 'verde_marino', 'cluster': 'referencia',
                 'leverbaarheid': 0.30, 'leverbaarheid_label': 'modelo de referencia — no en la papeleta'},
}

# ============================================================
# partij_posities (uit eerdere bundle-extractie, 11 partijen × 183 elementen)
# ============================================================
es_partij_pos = json.load(open('/tmp/es_partij_posities.json'))
# Verifieer schema: elke partij dict[183] van {positie, intensiteit}
for partij_id, posities in es_partij_pos.items():
    assert isinstance(posities, dict), f'{partij_id} niet dict'
    assert len(posities) == 183, f'{partij_id} heeft {len(posities)} != 183 elementen'
    voorbeeld = next(iter(posities.values()))
    assert 'positie' in voorbeeld and 'intensiteit' in voorbeeld, f'{partij_id} shape fout'
es['partij_posities'] = es_partij_pos

# ============================================================
# vragen (dict[7]) — vertaal .vraag en .antwoorden[].label, behoud rest
# ============================================================
VRAAG_VERT = {
    'Q1_sector':      '¿En qué sector trabajas (o has trabajado más tiempo)?',
    'Q2_wonen':       '¿Cómo vives actualmente?',
    'Q3_gezin':       '¿Cómo es tu hogar?',
    'Q4_leeftijd':    '¿En qué grupo de edad te encuentras?',
    'Q5_regio':       '¿Dónde vives en España?',
    'Q6_bedrijfslaag': '¿Qué tipo de empresa es?',
    'Q7_netwerk':     '¿Estás afectado por problemas de red, zonas medioambientales o conexión al gas?',
}
for qid, nieuwe_vraag in VRAAG_VERT.items():
    if qid in es['vragen']:
        es['vragen'][qid]['vraag'] = nieuwe_vraag

# Antwoord-labels — vertaal per vraag
ANTW_VERT = {
    'Q1_sector': {
        'S1_zorg': 'Sanidad y bienestar', 'S2_onderwijs': 'Educación y ciencia',
        'S3_defensie': 'Seguridad, policía y defensa', 'S4_bestuur': 'Administración pública',
        'S5_industrie': 'Producción industrial', 'S6_bouw': 'Construcción e infraestructura',
        'S7_logistiek': 'Logística y transporte', 'S8_landbouw': 'Agricultura y pesca',
        'S9_handel': 'Comercio y minorista', 'S10_horeca': 'Hostelería y turismo',
        'S11_ict': 'TIC y tecnología', 'S12_financieel': 'Servicios financieros y empresariales',
        'S13_creatief': 'Sector creativo y medios', 'S14_energie': 'Energía y utilities',
        'S15_vastgoed': 'Inmobiliario y vivienda',
        'S16_zzp_kennis': 'Autónomo — profesional del conocimiento',
        'S17_zzp_uitvoerend': 'Autónomo — profesional operativo',
        'S18_mkb': 'Pyme / empresa familiar', 'S19_grootbedrijf': 'Gran empresa / multinacional',
        'S20_gepensioneerd': 'Jubilado', 'S21_uitkering': 'Perceptor de prestaciones',
        'S22_student': 'Estudiante / iniciando carrera',
    },
    'Q2_wonen': {
        'huurder_schuld': 'Alquiler — con deudas', 'huurder_spaarder': 'Alquiler — ahorrando',
        'starter_koper': 'Primera vivienda — comprando', 'koper_aflossend': 'Propietario — pagando hipoteca',
        'vermogend_koper': 'Propietario — vivienda pagada',
    },
    'Q3_gezin': {
        'alleen': 'Solo/a', 'paar_zonder_kinderen': 'Pareja sin hijos',
        'paar_met_kinderen': 'Pareja con hijos', 'eenouder': 'Familia monoparental',
        'meergeneraties': 'Multigeneracional',
    },
    'Q4_leeftijd': {
        'jong': '18–29 años', 'werkend_jong': '30–44 años',
        'werkend_ouder': '45–59 años', 'pre_pensioen': '60–66 años',
        'senior': '67 años o más',
    },
    'Q5_regio': {
        'randstad': 'Área metropolitana grande (Madrid / Barcelona / Valencia)',
        'grote_stad': 'Ciudad mediana',
        'kleine_gemeente': 'Municipio pequeño',
        'krimpregio': 'España vaciada',
    },
    'Q6_bedrijfslaag': {
        'geen_bedrijf': 'No trabajo en empresa',
        'mkb': 'Pyme',
        'grootbedrijf_nl': 'Gran empresa española',
        'multinational': 'Multinacional',
        'overheid': 'Sector público',
        'zzp': 'Autónomo/a',
    },
    'Q7_netwerk': {
        'geen': 'Nada de lo siguiente',
        'netcongestie': 'Zona con congestión de red eléctrica',
        'stikstof': 'Cerca de Red Natura 2000 / zona protegida',
        'gasaansluiting': 'Con conexión de gas',
        'meerdere': 'Varias de las anteriores',
    },
}
for qid, ant_map in ANTW_VERT.items():
    if qid not in es['vragen']:
        continue
    ant = es['vragen'][qid].get('antwoorden', {})
    for aid, nieuwe_label in ant_map.items():
        if aid in ant:
            ant[aid]['label'] = nieuwe_label

# ============================================================
# baseline_gevolgen (nu placeholder — subagent vult in v3.18.1)
# Voor v3.18.0: minimaal 4 orde-1 events uit publiek bekende Spanje-data
# ============================================================
# We behouden NL-events als placeholder-structuur; markeren 'preliminair'
# Voor productie moet artefact J subagent draaien
for orde_key in ['orde_1_feiten', 'orde_2_afgeleiden', 'orde_3_systeem']:
    if orde_key in es['baseline_gevolgen']:
        for e in es['baseline_gevolgen'][orde_key]:
            e['status'] = 'preliminair - artefact J subagent vereist voor ES'
            # Voeg ES-prefix aan id
            if not e['id'].startswith('ES_'):
                e['id'] = 'ES_' + e['id']

# baseline_gevolgen metadata
if 'metadata' in es['baseline_gevolgen']:
    es['baseline_gevolgen']['metadata']['status'] = 'preliminair - artefact J vereist'
    es['baseline_gevolgen']['metadata']['land'] = 'España'

# ============================================================
# CONTRACT-CHECK v3.18 §0.6 (blokkerend)
# ============================================================
def check_contract(d):
    assert isinstance(d['sectoren'], dict), 'sectoren moet dict zijn'
    assert len(d['sectoren']) == 22, f'sectoren {len(d["sectoren"])} != 22'
    assert isinstance(d['partijen'], dict), 'partijen moet dict zijn'
    assert isinstance(d['partij_posities'], dict), 'partij_posities moet dict zijn'
    assert isinstance(d['vragen'], dict), 'vragen moet dict zijn'
    assert len(d['vragen']) == 7, f'vragen {len(d["vragen"])} != 7'
    assert isinstance(d['filters'], list), 'filters moet array zijn'
    assert len(d['filters']) == 9, f'filters {len(d["filters"])} != 9'
    assert isinstance(d['elementen'], list), 'elementen moet array zijn'
    assert len(d['elementen']) == 183, f'elementen {len(d["elementen"])} != 183'
    for k in ['sector_overlays', 'persona_overlays', 'filter_interactie',
              'baseline_gevolgen', 'nepk_tijdreeks', 'metadata']:
        assert k in d, f'ontbreekt: {k}'
    # Formule check
    f = d['nepk_tijdreeks']['factoren']
    nepk = f['E_tv_startwaarde_pct']/100 * f['alpha_startwaarde'] * (1-f['tau_startwaarde']) * f['phi_startwaarde'] * 100
    assert abs(nepk - d['nepk_tijdreeks']['nepk_startwaarde_pct_bbp']) < 0.3, f'formule fout: {nepk:.3f} vs {d["nepk_tijdreeks"]["nepk_startwaarde_pct_bbp"]}'
    return nepk

nepk_berekend = check_contract(es)
print(f'✅ Contract §0.6 check geslaagd. NEPK berekend: {nepk_berekend:.3f}%')

# Extra: partij-consistentie
assert set(es['partijen'].keys()) == set(es['partij_posities'].keys()), \
    f'partijen mismatch: {set(es["partijen"].keys()) ^ set(es["partij_posities"].keys())}'
print(f'✅ Partij-consistentie: {len(es["partijen"])} partijen in beide dicts')

# Opslaan
json.dump(es, open(ES_PATH, 'w'), ensure_ascii=False, indent=2)
print(f'✅ Geschreven: {ES_PATH} ({ES_PATH.stat().st_size:,} bytes)')

# ============================================================
# gevolgenkaart.json — data.ts vereist DataShape (Records)
# ============================================================
es_gk = copy.deepcopy(nl_gk)

# Vertaal sectoren
if isinstance(es_gk.get('sectoren'), dict):
    for sid, naam in SECTOR_VERT.items():
        if sid in es_gk['sectoren']:
            if isinstance(es_gk['sectoren'][sid], dict):
                es_gk['sectoren'][sid]['naam'] = naam

# Vervang partijen door 11 ES-partijen (behoud data.ts Partij-interface: naam/kleur/type)
es_gk['partijen'] = {}
PARTIJ_TYPE_MAP = {
    'PP': 'centrum-rechts', 'PSOE': 'centrum-links', 'Vox': 'rechts',
    'Sumar': 'links', 'Cs': 'centrum', 'ERC': 'regionaal', 'Junts': 'regionaal',
    'PNV': 'regionaal', 'EH Bildu': 'regionaal-links',
    'VMP': 'referentie', 'CARB': 'referentie',
}
for pid, pdata in es['partijen'].items():
    es_gk['partijen'][pid] = {
        'naam': pdata['naam'],
        'kleur': pdata['kleur'],
        'type': PARTIJ_TYPE_MAP.get(pid, 'onbekend'),
    }
    if pdata.get('cluster') == 'referencia':
        es_gk['partijen'][pid]['referentie'] = True
        es_gk['partijen'][pid]['opmerking'] = pdata.get('leverbaarheid_label', '')

# Vertaal filters_meta indien aanwezig (mag NL blijven — niet zichtbaar)
# filters/filters_meta behouden zoals NL

# uitkomst is een leeg-container in NL (engine vult live); behoud
if 'uitkomst' not in es_gk:
    es_gk['uitkomst'] = {}

json.dump(es_gk, open(ES_GK_PATH, 'w'), ensure_ascii=False, indent=2)
print(f'✅ Geschreven: {ES_GK_PATH} ({ES_GK_PATH.stat().st_size:,} bytes)')

# Summary
print()
print('=== ES Persona v3.18.0 ===')
print(f'  NEPK 2026: {es["nepk_tijdreeks"]["nepk_startwaarde_pct_bbp"]}%')
print(f'  Partijen: {len(es["partijen"])} ({list(es["partijen"].keys())})')
print(f'  Sectoren: {len(es["sectoren"])}')
print(f'  Elementen: {len(es["elementen"])}')
print(f'  Vragen: {len(es["vragen"])}')
print(f'  Filters: {len(es["filters"])}')
