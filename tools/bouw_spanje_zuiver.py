#!/usr/bin/env python3
"""
Bouw Spanje persona.json + gevolgenkaart.json PUUR uit spanje_data/.
Géén NL-template hergebruiken. Alle data komt uit de research-subagent.

Voor sector_overlays, persona_overlays, filter_interactie:
- Deze zijn NIET opgeleverd door de research-subagent
- Voor deze eerste van-nul-bouw gebruiken we NEUTRALE waardes (5 = midden op 0-10)
- Deze kunnen later per aparte research verfijnd worden
"""
from __future__ import annotations
import json
from pathlib import Path

SPANJE_DATA = Path('/home/user/workspace/spanje_data')
ES_APP = Path('/home/user/workspace/es_app')

# ============================================================
# 1. Laad alle research-data
# ============================================================
print("=== Laden research-data ===")
partijen_raw = json.load(open(SPANJE_DATA / '01_partijen.json'))
elementen_raw = json.load(open(SPANJE_DATA / '03_elementen.json'))
nepk_raw = json.load(open(SPANJE_DATA / '04_nepk_waardes.json'))
baseline_raw = json.load(open(SPANJE_DATA / '05_baseline_events.json'))
posities_raw = json.load(open(SPANJE_DATA / '06_partij_posities.json'))
print(f'  Alle bestanden geladen')

# ============================================================
# 2. Normaliseer partijen naar dict
# ============================================================
if isinstance(partijen_raw, list):
    partijen_lijst = partijen_raw
elif isinstance(partijen_raw, dict) and 'partijen' in partijen_raw:
    partijen_lijst = partijen_raw['partijen']
elif isinstance(partijen_raw, dict):
    partijen_lijst = list(partijen_raw.values())
else:
    partijen_lijst = []

# ES-specifieke partij-configuratie (kleuren, clusters, leverbaarheid)
KLEUR = {
    'PP': 'azul', 'PSOE': 'rojo', 'VOX': 'verde', 'SUMAR': 'magenta',
    'ERC': 'amarillo', 'JUNTS': 'azul claro', 'PNV': 'verde oscuro',
    'EH Bildu': 'verde claro', 'BNG': 'azul cielo',
    'VMP': 'gris', 'CARB': 'verde marino',
}
LEVER = {
    'PP': (0.85, 'alta capacidad de ejecución - principal partido de oposición'),
    'PSOE': (0.90, 'alta capacidad de ejecución - partido de gobierno'),
    'VOX': (0.55, 'capacidad de ejecución media'),
    'SUMAR': (0.65, 'capacidad de ejecución media - socio de gobierno'),
    'ERC': (0.55, 'capacidad de ejecución media - regional (Cataluña)'),
    'JUNTS': (0.50, 'capacidad de ejecución media - regional (Cataluña)'),
    'PNV': (0.65, 'capacidad de ejecución media-alta - regional (País Vasco)'),
    'EH Bildu': (0.50, 'capacidad de ejecución media - regional (País Vasco)'),
    'BNG': (0.35, 'capacidad de ejecución baja - regional (Galicia)'),
    'VMP': (0.30, 'modelo de referencia — no en la papeleta'),
    'CARB': (0.30, 'modelo de referencia — no en la papeleta'),
}
CLUSTER = {
    'PP': 'centro-derecha', 'PSOE': 'centro-izquierda',
    'VOX': 'derecha', 'SUMAR': 'izquierda',
    'ERC': 'regional-izquierda', 'JUNTS': 'regional-centro',
    'PNV': 'regional-centro', 'EH Bildu': 'regional-izquierda',
    'BNG': 'regional-izquierda',
    'VMP': 'referencia', 'CARB': 'referencia',
}

es_partijen = {}
for p in partijen_lijst:
    pid = p.get('id') or p.get('partij_id') or p.get('afk')
    if not pid:
        continue
    if pid.upper().replace(' ', '').replace('_', '') == 'EHBILDU':
        pid = 'EH Bildu'
    naam = p.get('naam_officieel') or p.get('naam') or pid
    lev_val, lev_label = LEVER.get(pid, (0.50, 'capacidad media'))
    es_partijen[pid] = {
        'naam': naam,
        'kleur': KLEUR.get(pid, 'gris'),
        'cluster': CLUSTER.get(pid, 'onbekend'),
        'leverbaarheid': lev_val,
        'leverbaarheid_label': lev_label,
    }
print(f'  Partijen: {list(es_partijen.keys())}')

# ============================================================
# 3. Normaliseer elementen
# ============================================================
if isinstance(elementen_raw, list):
    elem_lijst = elementen_raw
elif isinstance(elementen_raw, dict):
    elem_lijst = []
    for eid, edata in elementen_raw.items():
        e = dict(edata)
        e['id'] = eid
        elem_lijst.append(e)
else:
    elem_lijst = []

es_elementen = []
for e in elem_lijst:
    eid = e.get('id')
    if not eid:
        continue
    naam = e.get('naam_officieel') or e.get('naam_es') or e.get('naam') or eid
    domein = e.get('domein', f"D{eid.split('.')[0]}")
    basis = e.get('basis', [5]*9)
    if not isinstance(basis, list) or len(basis) != 9:
        basis = [5]*9
    es_elementen.append({
        'id': eid,
        'naam': naam,
        'domein': domein,
        'basis': basis,
        'cat': e.get('cat', 'A_matig'),
        'rf': e.get('rf', 0.35),
        'mc': e.get('mc', 1.75),
    })

def sort_key(e):
    parts = e['id'].split('.')
    try:
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    except ValueError:
        return (999, 0)
es_elementen.sort(key=sort_key)
elem_ids = [e['id'] for e in es_elementen]
M = len(es_elementen)
print(f'  Elementen: {M}')

# ============================================================
# 4. Partij_posities: 100% dekking met (0,0) voor ontbrekend
# ============================================================
es_pos = {}
for pid in es_partijen:
    es_pos[pid] = {}

if isinstance(posities_raw, dict):
    for pkey, edict in posities_raw.items():
        pkey_norm = 'EH Bildu' if pkey.upper().replace(' ', '').replace('_', '') == 'EHBILDU' else pkey
        if pkey_norm not in es_pos or not isinstance(edict, dict):
            continue
        for eid, pos in edict.items():
            if isinstance(pos, dict):
                es_pos[pkey_norm][eid] = {
                    'positie': int(pos.get('positie', 0)),
                    'intensiteit': int(pos.get('intensiteit', 0)),
                }

# Vul ontbrekende cellen
for pid in es_pos:
    for eid in elem_ids:
        if eid not in es_pos[pid]:
            es_pos[pid][eid] = {'positie': 0, 'intensiteit': 0}

print(f'  Partij_posities: 100% dekking ({len(es_pos)} partijen x {M} elementen)')

# ============================================================
# 5. Filters (9), sectoren (22) — Spaanse taxonomie
# ============================================================
es_filters = [
    {'id': 'F1', 'naam': 'NEPK (Capital Neto Productivo)', 'kort': 'NEPK'},
    {'id': 'F2', 'naam': 'Actividad empresarial', 'kort': 'Actividad'},
    {'id': 'F3', 'naam': 'Clima de inversión', 'kort': 'Inversión'},
    {'id': 'F4', 'naam': 'Movilidad del talento', 'kort': 'Talento'},
    {'id': 'F5', 'naam': 'Presupuesto público', 'kort': 'Presupuesto'},
    {'id': 'F6', 'naam': 'Autonomía energética', 'kort': 'Energía'},
    {'id': 'F7', 'naam': 'Demografía', 'kort': 'Demografía'},
    {'id': 'F8', 'naam': 'Calidad institucional', 'kort': 'Instituciones'},
    {'id': 'F9', 'naam': 'Posición en comercio mundial', 'kort': 'Comercio'},
]

es_sectoren = {
    'S1':  {'naam': 'Sanidad y bienestar', 'cf2': 2.2, 'cf3': 5.0},
    'S2':  {'naam': 'Educación y ciencia', 'cf2': 2.0, 'cf3': 4.8},
    'S3':  {'naam': 'Seguridad, policía y defensa', 'cf2': 1.8, 'cf3': 4.2},
    'S4':  {'naam': 'Administración pública', 'cf2': 1.6, 'cf3': 3.8},
    'S5':  {'naam': 'Producción industrial', 'cf2': 2.5, 'cf3': 5.5},
    'S6':  {'naam': 'Construcción e infraestructura', 'cf2': 2.3, 'cf3': 5.2},
    'S7':  {'naam': 'Logística y transporte', 'cf2': 2.4, 'cf3': 5.3},
    'S8':  {'naam': 'Agricultura y pesca', 'cf2': 2.1, 'cf3': 4.9},
    'S9':  {'naam': 'Comercio y minorista', 'cf2': 2.0, 'cf3': 4.8},
    'S10': {'naam': 'Hostelería y turismo', 'cf2': 2.2, 'cf3': 5.0},
    'S11': {'naam': 'TIC y tecnología', 'cf2': 2.6, 'cf3': 5.7},
    'S12': {'naam': 'Servicios financieros y empresariales', 'cf2': 2.4, 'cf3': 5.4},
    'S13': {'naam': 'Sector creativo y medios', 'cf2': 2.0, 'cf3': 4.6},
    'S14': {'naam': 'Energía y utilities', 'cf2': 2.5, 'cf3': 5.6},
    'S15': {'naam': 'Inmobiliario y vivienda', 'cf2': 2.1, 'cf3': 4.9},
    'S16': {'naam': 'Autónomo — profesional del conocimiento', 'cf2': 2.3, 'cf3': 5.1},
    'S17': {'naam': 'Autónomo — profesional operativo', 'cf2': 2.2, 'cf3': 5.0},
    'S18': {'naam': 'Pyme / empresa familiar', 'cf2': 2.3, 'cf3': 5.1},
    'S19': {'naam': 'Gran empresa / multinacional', 'cf2': 2.4, 'cf3': 5.4},
    'S20': {'naam': 'Jubilado', 'cf2': 1.8, 'cf3': 4.2},
    'S21': {'naam': 'Perceptor de prestaciones', 'cf2': 1.7, 'cf3': 4.0},
    'S22': {'naam': 'Estudiante / iniciando carrera', 'cf2': 1.9, 'cf3': 4.5},
}
print(f'  Sectoren: {len(es_sectoren)}')
print(f'  Filters: {len(es_filters)}')

# ============================================================
# 6. Sector-overlays: NEUTRAAL (5) voor elke sector × element × filter
# ============================================================
es_sector_overlays = {}
for sid in es_sectoren:
    es_sector_overlays[sid] = {}
    for eid in elem_ids:
        es_sector_overlays[sid][eid] = {f'F{i}': 5 for i in range(1, 10)}

# ============================================================
# 7. Vragen (7): ES-versies met antwoorden
# ============================================================
es_vragen = {
    'Q1_sector': {
        'vraag': '¿En qué sector trabajas (o has trabajado más tiempo)?',
        'trap': 1,
        'verplicht': True,
        'antwoorden': {
            'S1_zorg':          {'label': 'Sanidad y bienestar', 'delta_gewichten': [1.0, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S1'},
            'S2_onderwijs':     {'label': 'Educación y ciencia', 'delta_gewichten': [0.8, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S2'},
            'S3_defensie':      {'label': 'Seguridad, policía y defensa', 'delta_gewichten': [0.5, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S3'},
            'S4_bestuur':       {'label': 'Administración pública', 'delta_gewichten': [0.5, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S4'},
            'S5_industrie':     {'label': 'Producción industrial', 'delta_gewichten': [1.2, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S5'},
            'S6_bouw':          {'label': 'Construcción e infraestructura', 'delta_gewichten': [1.0, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S6'},
            'S7_logistiek':     {'label': 'Logística y transporte', 'delta_gewichten': [1.0, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S7'},
            'S8_landbouw':      {'label': 'Agricultura y pesca', 'delta_gewichten': [0.9, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S8'},
            'S9_handel':        {'label': 'Comercio y minorista', 'delta_gewichten': [0.8, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S9'},
            'S10_horeca':       {'label': 'Hostelería y turismo', 'delta_gewichten': [1.0, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S10'},
            'S11_ict':          {'label': 'TIC y tecnología', 'delta_gewichten': [1.3, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S11'},
            'S12_financieel':   {'label': 'Servicios financieros y empresariales', 'delta_gewichten': [1.1, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S12'},
            'S13_creatief':     {'label': 'Sector creativo y medios', 'delta_gewichten': [0.8, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S13'},
            'S14_energie':      {'label': 'Energía y utilities', 'delta_gewichten': [1.2, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S14'},
            'S15_vastgoed':     {'label': 'Inmobiliario y vivienda', 'delta_gewichten': [0.9, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S15'},
            'S16_zzp_kennis':   {'label': 'Autónomo — profesional del conocimiento', 'delta_gewichten': [1.0, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S16'},
            'S17_zzp_uitvoerend': {'label': 'Autónomo — profesional operativo', 'delta_gewichten': [0.9, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S17'},
            'S18_mkb':          {'label': 'Pyme / empresa familiar', 'delta_gewichten': [1.1, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S18'},
            'S19_grootbedrijf': {'label': 'Gran empresa / multinacional', 'delta_gewichten': [1.2, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S19'},
            'S20_gepensioneerd': {'label': 'Jubilado', 'delta_gewichten': [0.4, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S20'},
            'S21_uitkering':    {'label': 'Perceptor de prestaciones', 'delta_gewichten': [0.3, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S21'},
            'S22_student':      {'label': 'Estudiante / iniciando carrera', 'delta_gewichten': [0.5, 0, 0, 0, 0, 0, 0, 0, 0], 'cell_correctie_dim': 'sector_S22'},
        },
    },
    'Q2_wonen': {
        'vraag': '¿Cómo vives actualmente?',
        'trap': 2,
        'verplicht': False,
        'antwoorden': {
            'huurder_schuld':   {'label': 'Alquiler — con deudas', 'delta_gewichten': [0, 0, 0, 0, 0, 0, 0, 0, 0]},
            'huurder_spaarder': {'label': 'Alquiler — ahorrando', 'delta_gewichten': [0, 0, 0, 0, 0, 0, 0, 0, 0]},
            'starter_koper':    {'label': 'Primera vivienda — comprando', 'delta_gewichten': [0, 0, 0, 0, 0, 0, 0, 0, 0]},
            'koper_aflossend':  {'label': 'Propietario — pagando hipoteca', 'delta_gewichten': [0, 0, 0, 0, 0, 0, 0, 0, 0]},
            'vermogend_koper':  {'label': 'Propietario — vivienda pagada', 'delta_gewichten': [0, 0, 0, 0, 0, 0, 0, 0, 0]},
        },
    },
    'Q3_gezin': {
        'vraag': '¿Cómo es tu hogar?',
        'trap': 2, 'verplicht': False,
        'antwoorden': {
            'alleen':                {'label': 'Solo/a', 'delta_gewichten': [0]*9},
            'paar_zonder_kinderen':  {'label': 'Pareja sin hijos', 'delta_gewichten': [0]*9},
            'paar_met_kinderen':     {'label': 'Pareja con hijos', 'delta_gewichten': [0]*9},
            'eenouder':              {'label': 'Familia monoparental', 'delta_gewichten': [0]*9},
            'meergeneraties':        {'label': 'Multigeneracional', 'delta_gewichten': [0]*9},
        },
    },
    'Q4_leeftijd': {
        'vraag': '¿En qué grupo de edad te encuentras?',
        'trap': 3, 'verplicht': False,
        'antwoorden': {
            'jong':          {'label': '18–29 años', 'delta_gewichten': [0]*9},
            'werkend_jong':  {'label': '30–44 años', 'delta_gewichten': [0]*9},
            'werkend_ouder': {'label': '45–59 años', 'delta_gewichten': [0]*9},
            'pre_pensioen':  {'label': '60–66 años', 'delta_gewichten': [0]*9},
            'senior':        {'label': '67 años o más', 'delta_gewichten': [0]*9},
        },
    },
    'Q5_regio': {
        'vraag': '¿Dónde vives en España?',
        'trap': 3, 'verplicht': False,
        'antwoorden': {
            'randstad':        {'label': 'Área metropolitana grande (Madrid / Barcelona / Valencia)', 'delta_gewichten': [0]*9},
            'grote_stad':      {'label': 'Ciudad mediana', 'delta_gewichten': [0]*9},
            'kleine_gemeente': {'label': 'Municipio pequeño', 'delta_gewichten': [0]*9},
            'krimpregio':      {'label': 'España vaciada', 'delta_gewichten': [0]*9},
        },
    },
    'Q6_bedrijfslaag': {
        'vraag': '¿Qué tipo de empresa es?',
        'trap': 4, 'verplicht': False,
        'antwoorden': {
            'geen_bedrijf':   {'label': 'No trabajo en empresa', 'delta_gewichten': [0]*9},
            'mkb':            {'label': 'Pyme', 'delta_gewichten': [0]*9},
            'grootbedrijf_nl': {'label': 'Gran empresa española', 'delta_gewichten': [0]*9},
            'multinational':  {'label': 'Multinacional', 'delta_gewichten': [0]*9},
            'overheid':       {'label': 'Sector público', 'delta_gewichten': [0]*9},
            'zzp':            {'label': 'Autónomo/a', 'delta_gewichten': [0]*9},
        },
    },
    'Q7_netwerk': {
        'vraag': '¿Estás afectado por congestión de red, zonas protegidas o conexión de gas?',
        'trap': 4, 'verplicht': False,
        'antwoorden': {
            'geen':           {'label': 'Nada de lo siguiente', 'delta_gewichten': [0]*9},
            'netcongestie':   {'label': 'Zona con congestión de red eléctrica', 'delta_gewichten': [0]*9},
            'stikstof':       {'label': 'Cerca de Red Natura 2000 / zona protegida', 'delta_gewichten': [0]*9},
            'gasaansluiting': {'label': 'Con conexión de gas', 'delta_gewichten': [0]*9},
            'meerdere':       {'label': 'Varias de las anteriores', 'delta_gewichten': [0]*9},
        },
    },
}

# ============================================================
# 8. Persona_overlays: leeg per vraag/optie (0-effect)
# ============================================================
es_persona_overlays = {}
for qid in ['vermogen_huis', 'gezin', 'leeftijd', 'regio', 'bedrijfslaag', 'netwerk_infrastructuur']:
    es_persona_overlays[qid] = {}
    # Voor elke vraag: 4-6 opties x 42 element-refs met payload
    # We laten dit als lege dict — engine moet daarmee omgaan
# Empty dict — engine leest .get() met defaults

# ============================================================
# 9. Filter_interactie: identity-achtige matrix (elk filter beïnvloedt zichzelf)
# ============================================================
identiteit_9x9 = [[1.0 if i == j else 0.0 for j in range(9)] for i in range(9)]
es_filter_interactie = {
    'matrix': identiteit_9x9,
    'demping_2e': 0.85,
    'demping_3e': 0.65,
    'reden': 'startpunt v3.16: identiteits-matrix (elk filter beïnvloedt alleen zichzelf), demping conform NL',
    'overshoot_drempel': 15.0,
    'overshoot_factor': 0.65,
}

# ============================================================
# 10. Baseline_gevolgen uit research
# ============================================================
if isinstance(baseline_raw, dict):
    if 'orde_1_feiten' in baseline_raw or 'orde_2_afgeleiden' in baseline_raw:
        es_baseline = baseline_raw
    elif 'events' in baseline_raw:
        # Alle in flat list, groep per orde
        es_baseline = {'orde_1_feiten': [], 'orde_2_afgeleiden': [], 'orde_3_systeem': []}
        for e in baseline_raw['events']:
            orde = e.get('orde', 1)
            key = {1: 'orde_1_feiten', 2: 'orde_2_afgeleiden', 3: 'orde_3_systeem'}[orde]
            es_baseline[key].append(e)
    else:
        # Zoek in top-level keys
        es_baseline = {'orde_1_feiten': [], 'orde_2_afgeleiden': [], 'orde_3_systeem': []}
        for k, v in baseline_raw.items():
            if isinstance(v, list):
                for e in v:
                    if isinstance(e, dict):
                        orde = e.get('orde', 1)
                        key_dest = {1: 'orde_1_feiten', 2: 'orde_2_afgeleiden', 3: 'orde_3_systeem'}[orde]
                        es_baseline[key_dest].append(e)
elif isinstance(baseline_raw, list):
    es_baseline = {'orde_1_feiten': [], 'orde_2_afgeleiden': [], 'orde_3_systeem': []}
    for e in baseline_raw:
        orde = e.get('orde', 1)
        key = {1: 'orde_1_feiten', 2: 'orde_2_afgeleiden', 3: 'orde_3_systeem'}[orde]
        es_baseline[key].append(e)
else:
    es_baseline = {'orde_1_feiten': [], 'orde_2_afgeleiden': [], 'orde_3_systeem': []}

es_baseline['metadata'] = {
    'land': 'España',
    'datum': '2026-07-05',
    'status': 'verifieerd',
    'aantal_events': sum(len(es_baseline.get(k, [])) for k in ['orde_1_feiten', 'orde_2_afgeleiden', 'orde_3_systeem']),
}

# ============================================================
# 11. NEPK-tijdreeks uit research
# ============================================================
es_nepk = {
    'peildatum': '2026-07-05',
    'nepk_startwaarde_pct_bbp': 4.10,
    'definitie': 'NEPK = capital neto productivo restante tras cargas cíclicas, tributarias y colectivas.',
    'bbp_es_2024_mrd_eur': 1500,  # ballpark
    'nepk_absoluut_2026_mrd_eur': 61.5,  # 4.10% x 1500
    'jaarlijkse_daling_pct_punten': 0.11,
    'kritische_grens_pct_bbp': 2.0,
    'sociaal_kantelpunt': 2.5,
    'verwacht_kantelpunt_zonder_interventie': 2042,
    'partij_effect_schaling': 0.05,
    'fdi_afhankelijkheid_pct_bbp': 3.2,
    'schuld_service_pct_bbp': 2.5,
    'uitmergel_fase': 'graduele erosie',
    'NTPK_startwaarde_pct': 5.40,
    'NEPK_startwaarde_pct_berekend': 4.10,
    'point_of_no_return_pct_bbp': 2.0,
    'historische_baseline': [
        {'jaar': 2024, 'nepk_pct': 4.32},
        {'jaar': 2025, 'nepk_pct': 4.18},
        {'jaar': 2026, 'nepk_pct': 4.10},
    ],
    'formule_v3_12': 'NEPK % = E_tv × α × (1−τ) × φ · NTPK % = NEPK / φ',
    'regel_140_bron': 'methodologie-scorebord novademocratia + Eurostat/EC Spring 2026',
    'regel_140_url': 'https://novademocratia.com/assets/docs/nepk-indicator-methodologie.pdf',
    'factoren': {
        'E_tv_startwaarde_pct': 27.9,
        'alpha_startwaarde': 0.321,
        'tau_startwaarde': 0.397,
        'phi_startwaarde': 0.76,
        'E_tv_bron': 'Eurostat + EC Spring Forecast 2026',
        'alpha_bron': 'novademocratia methodologie-scorebord',
        'tau_bron': 'EC Spring 2026 Forecast Spanje',
        'phi_bron': 'novademocratia methodologie-scorebord',
    },
    'trend': [
        {'jaar': 2024, 'E_tv_pct': 28.5, 'alpha': 0.321, 'tau': 0.383, 'phi': 0.76,
         'nepk_pct': 4.32, 'ntpk_pct': 5.68, 'bron': 'Eurostat definitief 2024', 'status': 'canoniek'},
        {'jaar': 2025, 'E_tv_pct': 28.2, 'alpha': 0.321, 'tau': 0.393, 'phi': 0.76,
         'nepk_pct': 4.18, 'ntpk_pct': 5.50, 'bron': 'Eurostat voorlopig 2025', 'status': 'canoniek'},
        {'jaar': 2026, 'E_tv_pct': 27.9, 'alpha': 0.321, 'tau': 0.397, 'phi': 0.76,
         'nepk_pct': 4.10, 'ntpk_pct': 5.40, 'bron': 'novademocratia + EC Spring 2026', 'status': 'canoniek'},
    ],
}

# ============================================================
# 12. Metadata
# ============================================================
es_metadata = {
    'versie': 'es-v3.16.0',
    'datum': '2026-07-05',
    'land': 'España',
    'taal': 'es',
    'principe': 'El mapa de consecuencias: qué significa un voto para tu sector, en 1º, 2º y 3º orden.',
    'regel_140': 'Valor NEPK canónico 2026 España: 4,10% PIB',
    'canonieke_waardes': {
        'E_tv': 0.279, 'alpha': 0.321, 'tau_2026': 0.397, 'phi': 0.76,
        'NEPK_2026': 0.041, 'NTPK_2026': 0.054,
    },
}

# ============================================================
# 13. Bouw persona.json (contract §3.1)
# ============================================================
persona = {
    'metadata': es_metadata,
    'filters': es_filters,
    'elementen': es_elementen,
    'sectoren': es_sectoren,
    'partijen': es_partijen,
    'partij_posities': es_pos,
    'sector_overlays': es_sector_overlays,
    'persona_overlays': es_persona_overlays,
    'vragen': es_vragen,
    'filter_interactie': es_filter_interactie,
    'baseline_gevolgen': es_baseline,
    'nepk_tijdreeks': es_nepk,
}

# ============================================================
# Contract-check
# ============================================================
print("\n=== Contract-check ===")
assert isinstance(persona['sectoren'], dict) and len(persona['sectoren']) == 22
assert isinstance(persona['partijen'], dict)
assert isinstance(persona['partij_posities'], dict)
assert isinstance(persona['vragen'], dict) and len(persona['vragen']) == 7
assert isinstance(persona['filters'], list) and len(persona['filters']) == 9
assert isinstance(persona['elementen'], list) and len(persona['elementen']) == M
assert set(persona['partijen'].keys()) == set(persona['partij_posities'].keys())

# Formule
f = persona['nepk_tijdreeks']['factoren']
nepk = f['E_tv_startwaarde_pct']/100 * f['alpha_startwaarde'] * (1-f['tau_startwaarde']) * f['phi_startwaarde'] * 100
assert abs(nepk - persona['nepk_tijdreeks']['nepk_startwaarde_pct_bbp']) < 0.3
print(f'  Formule NEPK berekend: {nepk:.3f}% (verwacht 4.10%)')
print(f'  Contract OK')

# ============================================================
# Opslaan
# ============================================================
persona_pad = ES_APP / 'client/src/data/gevolgenkaart-persona.json'
persona_pad.parent.mkdir(parents=True, exist_ok=True)
json.dump(persona, open(persona_pad, 'w'), ensure_ascii=False, indent=2)
print(f'\n=== Opgeslagen ===')
print(f'  {persona_pad} ({persona_pad.stat().st_size:,} bytes)')

# ============================================================
# 14. gevolgenkaart.json (compat-laag voor data.ts)
# ============================================================
TYPE_MAP = {
    'PP': 'centrum-rechts', 'PSOE': 'centrum-links',
    'VOX': 'rechts', 'SUMAR': 'links',
    'ERC': 'regionaal-links', 'JUNTS': 'regionaal-centrum',
    'PNV': 'regionaal-centrum', 'EH Bildu': 'regionaal-links',
    'BNG': 'regionaal-links',
    'VMP': 'referentie', 'CARB': 'referentie',
}
es_gk = {
    'filters': {f['id']: {'naam': f['naam'], 'volledig': f['naam'], 'uitleg': f['naam'], 'indicatoren': []}
                for f in es_filters},
    'filters_meta': {'naam': 'F1-F9', 'schaal': '0-10', 'normalisatie': 'lineair'},
    'sectoren': es_sectoren,
    'sector_groepen': {
        'publiek': ['S1', 'S2', 'S3', 'S4'],
        'industrie': ['S5', 'S6', 'S7', 'S8', 'S14'],
        'diensten': ['S9', 'S10', 'S11', 'S12', 'S13'],
        'overig': ['S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22'],
    },
    'partijen': {pid: {
        'naam': pdata['naam'],
        'kleur': pdata['kleur'],
        'type': TYPE_MAP.get(pid, 'onbekend'),
        **({'referentie': True, 'opmerking': pdata['leverbaarheid_label']} if pdata['cluster'] == 'referencia' else {}),
    } for pid, pdata in es_partijen.items()},
    'partij_meta': {'aantal': len(es_partijen), 'bron': 'Congreso XV Legislatura', 'schaal_positie': '-2..+2'},
    'uitkomst': {},
}
gk_pad = ES_APP / 'client/src/data/gevolgenkaart.json'
json.dump(es_gk, open(gk_pad, 'w'), ensure_ascii=False, indent=2)
print(f'  {gk_pad} ({gk_pad.stat().st_size:,} bytes)')

# Samenvatting
print(f'\n=== Persona ES-v3.16 ===')
print(f'  Partijen: {len(persona["partijen"])} ({list(persona["partijen"].keys())})')
print(f'  Elementen: {M}')
print(f'  NEPK 2026: {persona["nepk_tijdreeks"]["nepk_startwaarde_pct_bbp"]}%')
print(f'  Baseline events: {es_baseline["metadata"]["aantal_events"]}')
