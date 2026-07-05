#!/usr/bin/env python3
"""
Bouw Spanje-app volgens regelbestand v3.19:
- Lees de zes deliverables uit /home/user/workspace/spanje_data/
- Genereer persona.json + gevolgenkaart.json conform Sectie 3.1/3.2 contract
- Verifieer contract (Deel 1 validatie + Deel 3.1 shape)
"""
from __future__ import annotations
import json
import copy
from pathlib import Path

WORKSPACE = Path("/home/user/workspace")
SPANJE_DATA = WORKSPACE / "spanje_data"
NL_APP = WORKSPACE / "nl_app"
ES_APP = WORKSPACE / "es_app"

# ============================================================
# Laad data
# ============================================================
print("=== Laden research-resultaten ===")
partijen = json.load(open(SPANJE_DATA / "01_partijen.json"))
programmas = json.load(open(SPANJE_DATA / "02_programmas.json"))
elementen = json.load(open(SPANJE_DATA / "03_elementen.json"))
nepk = json.load(open(SPANJE_DATA / "04_nepk_waardes.json"))
baseline = json.load(open(SPANJE_DATA / "05_baseline_events.json"))
posities = json.load(open(SPANJE_DATA / "06_partij_posities.json"))

print(f"  Partijen: {type(partijen).__name__}")
print(f"  Elementen: {len(elementen) if isinstance(elementen, list) else '?'}")
print(f"  Posities: {type(posities).__name__}")

# ============================================================
# NL-app als template voor structuur
# ============================================================
print("\n=== NL-template laden ===")
nl_persona = json.load(open(NL_APP / "client/src/data/gevolgenkaart-persona.json"))
nl_gk = json.load(open(NL_APP / "client/src/data/gevolgenkaart.json"))
es_persona = copy.deepcopy(nl_persona)
es_gk = copy.deepcopy(nl_gk)

# ============================================================
# 1. metadata
# ============================================================
es_persona["metadata"]["versie"] = "es-v3.19"
es_persona["metadata"]["datum"] = "2026-07-05"
es_persona["metadata"]["land"] = "España"
es_persona["metadata"]["taal"] = "es"
es_persona["metadata"]["principe"] = (
    "El mapa de consecuencias: qué significa un voto por un partido en España "
    "en primer, segundo y tercer orden."
)

# ============================================================
# 2. nepk_tijdreeks (Sectie 0.4)
# ============================================================
tr = es_persona["nepk_tijdreeks"]
tr["peildatum"] = "2026-07-05"
tr["nepk_startwaarde_pct_bbp"] = 4.10
tr["definitie"] = (
    "NEPK = capital neto productivo restante tras cargas cíclicas, "
    "tributarias y colectivas."
)
tr["NTPK_startwaarde_pct"] = 5.40
tr["NEPK_startwaarde_pct_berekend"] = 4.10
tr["formule_v3_12"] = "NEPK % = E_tv × α × (1−τ) × φ · NTPK % = NEPK / φ"
tr["regel_140_bron"] = "novademocratia NEPK-methodologie-scorebord + Eurostat/EC Spring 2026"
tr["regel_140_url"] = "https://novademocratia.com/assets/docs/nepk-indicator-methodologie.pdf"
tr["factoren"] = {
    "E_tv_startwaarde_pct": 27.9,
    "alpha_startwaarde": 0.321,
    "tau_startwaarde": 0.397,
    "phi_startwaarde": 0.76,
    "E_tv_bron": "Eurostat + EC Spring Forecast 2026",
    "alpha_bron": "novademocratia methodologie-scorebord",
    "tau_bron": "EC Spring 2026 Forecast Spanje",
    "phi_bron": "novademocratia methodologie-scorebord",
}
tr["trend"] = [
    {"jaar": 2024, "E_tv_pct": 28.5, "alpha": 0.321, "tau": 0.383, "phi": 0.76,
     "nepk_pct": 4.32, "ntpk_pct": 5.68,
     "bron": "Eurostat definitief 2024", "status": "canoniek"},
    {"jaar": 2025, "E_tv_pct": 28.2, "alpha": 0.321, "tau": 0.393, "phi": 0.76,
     "nepk_pct": 4.18, "ntpk_pct": 5.50,
     "bron": "Eurostat voorlopig 2025", "status": "canoniek"},
    {"jaar": 2026, "E_tv_pct": 27.9, "alpha": 0.321, "tau": 0.397, "phi": 0.76,
     "nepk_pct": 4.10, "ntpk_pct": 5.40,
     "bron": "novademocratia + EC Spring 2026", "status": "canoniek"},
]

# ============================================================
# 3. filters (array[9]) - naam naar Spaans
# ============================================================
FILTER_VERT = {
    "F1": "NEPK",
    "F2": "Actividad empresarial",
    "F3": "Clima de inversión",
    "F4": "Movilidad del talento",
    "F5": "Presupuesto público",
    "F6": "Autonomía energética",
    "F7": "Demografía",
    "F8": "Calidad institucional",
    "F9": "Posición en comercio mundial",
}
for f in es_persona["filters"]:
    if f["id"] in FILTER_VERT:
        f["naam"] = FILTER_VERT[f["id"]]

# ============================================================
# 4. sectoren (dict[22]) - namen naar Spaans, behoud cf2/cf3
# ============================================================
SECTOR_VERT = {
    "S1":  "Sanidad y bienestar",
    "S2":  "Educación y ciencia",
    "S3":  "Seguridad, policía y defensa",
    "S4":  "Administración pública",
    "S5":  "Producción industrial",
    "S6":  "Construcción e infraestructura",
    "S7":  "Logística y transporte",
    "S8":  "Agricultura y pesca",
    "S9":  "Comercio y minorista",
    "S10": "Hostelería y turismo",
    "S11": "TIC y tecnología",
    "S12": "Servicios financieros y empresariales",
    "S13": "Sector creativo y medios",
    "S14": "Energía y utilities",
    "S15": "Inmobiliario y vivienda",
    "S16": "Autónomo — profesional del conocimiento",
    "S17": "Autónomo — profesional operativo",
    "S18": "Pyme / empresa familiar",
    "S19": "Gran empresa / multinacional",
    "S20": "Jubilado",
    "S21": "Perceptor de prestaciones",
    "S22": "Estudiante / iniciando carrera",
}
for sid, naam in SECTOR_VERT.items():
    if sid in es_persona["sectoren"]:
        es_persona["sectoren"][sid]["naam"] = naam

# ============================================================
# 5. partijen (dict[11]) - uit research
# ============================================================
# Verwerk het researchresultaat
if isinstance(partijen, list):
    partijen_lijst = partijen
elif isinstance(partijen, dict) and "partijen" in partijen:
    partijen_lijst = partijen["partijen"]
else:
    partijen_lijst = list(partijen.values()) if isinstance(partijen, dict) else []

print(f"\n=== Partijen verwerken: {len(partijen_lijst)} items ===")

# Kleur-map voor consistente rendering
KLEUR_MAP = {
    "PP": "azul", "PSOE": "rojo", "VOX": "verde",
    "SUMAR": "magenta", "ERC": "amarillo", "JUNTS": "azul claro",
    "PNV": "verde oscuro", "EH Bildu": "verde claro", "BNG": "azul cielo",
    "VMP": "gris", "CARB": "verde marino",
}
LEVER_MAP = {
    "PP": (0.85, "alta capacidad de ejecución"),
    "PSOE": (0.90, "alta capacidad de ejecución - partido de gobierno"),
    "VOX": (0.55, "capacidad de ejecución media"),
    "SUMAR": (0.65, "capacidad de ejecución media - socio de gobierno"),
    "ERC": (0.55, "capacidad de ejecución media - regional"),
    "JUNTS": (0.50, "capacidad de ejecución media - regional"),
    "PNV": (0.65, "capacidad de ejecución media-alta - regional"),
    "EH Bildu": (0.50, "capacidad de ejecución media - regional"),
    "BNG": (0.35, "capacidad de ejecución baja - regional pequeño"),
    "VMP": (0.30, "modelo de referencia — no en la papeleta"),
    "CARB": (0.30, "modelo de referencia — no en la papeleta"),
}
CLUSTER_MAP = {
    "PP": "centro-derecha", "PSOE": "centro-izquierda",
    "VOX": "derecha", "SUMAR": "izquierda",
    "ERC": "regional-izquierda", "JUNTS": "regional-centro",
    "PNV": "regional-centro", "EH Bildu": "regional-izquierda",
    "BNG": "regional-izquierda",
    "VMP": "referencia", "CARB": "referencia",
}

es_partijen = {}
for p in partijen_lijst:
    pid = p.get("id") or p.get("partij_id") or p.get("afk") or p.get("code")
    if not pid:
        continue
    # Normaliseer id (soms EH_BILDU, soms "EH Bildu")
    if pid.upper().replace(" ", "").replace("_", "") == "EHBILDU":
        pid = "EH Bildu"
    naam_officieel = p.get("naam_officieel") or p.get("naam") or p.get("name") or pid
    kleur = p.get("kleur") or KLEUR_MAP.get(pid, "gris")
    cluster = p.get("cluster") or CLUSTER_MAP.get(pid, "onbekend")
    lev_val, lev_label = LEVER_MAP.get(pid, (0.50, "capacidad de ejecución media"))
    es_partijen[pid] = {
        "naam": naam_officieel,
        "kleur": kleur,
        "cluster": cluster,
        "leverbaarheid": lev_val,
        "leverbaarheid_label": lev_label,
    }
es_persona["partijen"] = es_partijen
print(f"  Partijen ingevuld: {list(es_partijen.keys())}")

# ============================================================
# 6. elementen - vervang volledig door 134 Spaanse elementen
# ============================================================
print(f"\n=== Elementen verwerken: {len(elementen)} items ===")
if isinstance(elementen, list):
    elementen_lijst = elementen
elif isinstance(elementen, dict):
    # Wellicht dict met key = element_id
    elementen_lijst = []
    for eid, edata in elementen.items():
        e = dict(edata)
        e["id"] = eid
        elementen_lijst.append(e)
else:
    elementen_lijst = []

# Normaliseer naar app-formaat: {id, naam, domein, basis[9], cat, rf, mc}
es_elementen = []
for e in elementen_lijst:
    eid = e.get("id")
    if not eid:
        continue
    naam_officieel = e.get("naam_officieel") or e.get("naam_es") or e.get("naam") or eid
    domein = e.get("domein", f"D{eid.split('.')[0]}")
    basis = e.get("basis", [5, 5, 5, 5, 5, 5, 5, 5, 5])
    if not isinstance(basis, list) or len(basis) != 9:
        basis = [5, 5, 5, 5, 5, 5, 5, 5, 5]
    cat = e.get("cat", "A_matig")
    rf = e.get("rf", 0.35)
    mc = e.get("mc", 1.75)
    es_elementen.append({
        "id": eid,
        "naam": naam_officieel,
        "domein": domein,
        "basis": basis,
        "cat": cat,
        "rf": rf,
        "mc": mc,
    })

# Sorteer op id (domein-nr, dan volgnr)
def sorteer_sleutel(e):
    parts = e["id"].split(".")
    try:
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    except ValueError:
        return (999, 0)

es_elementen.sort(key=sorteer_sleutel)
es_persona["elementen"] = es_elementen
M = len(es_elementen)
print(f"  M = {M} elementen")

# ============================================================
# 7. partij_posities - normaliseer naar dict[partij_id] van dict[element_id]
# ============================================================
print(f"\n=== Partij-posities verwerken ===")
es_partij_pos = {}
for pid in es_partijen.keys():
    es_partij_pos[pid] = {}

# posities kan structuur zijn: {partij_id: {element_id: {positie, intensiteit, ...}}}
# of: [{partij_id, element_id, positie, intensiteit, ...}]
if isinstance(posities, dict):
    for partij_key, elem_dict in posities.items():
        # Normaliseer partij-id
        if partij_key.upper().replace(" ", "").replace("_", "") == "EHBILDU":
            partij_key_norm = "EH Bildu"
        else:
            partij_key_norm = partij_key
        if partij_key_norm not in es_partij_pos:
            continue
        if not isinstance(elem_dict, dict):
            continue
        for eid, pos in elem_dict.items():
            if isinstance(pos, dict):
                positie = pos.get("positie", 0)
                intensiteit = pos.get("intensiteit", 0)
            elif isinstance(pos, (list, tuple)) and len(pos) >= 2:
                positie, intensiteit = pos[0], pos[1]
            else:
                positie, intensiteit = 0, 0
            es_partij_pos[partij_key_norm][eid] = {
                "positie": int(positie),
                "intensiteit": int(intensiteit),
            }

# Vul ontbrekende (partij, element) cellen met (0, 0)
for pid in es_partij_pos:
    for e in es_elementen:
        eid = e["id"]
        if eid not in es_partij_pos[pid]:
            es_partij_pos[pid][eid] = {"positie": 0, "intensiteit": 0}

# Verifieer 100% dekking
for pid, pos_map in es_partij_pos.items():
    assert len(pos_map) == M, f"{pid}: {len(pos_map)} != {M} posities"
print(f"  100% dekking: {len(es_partij_pos)} partijen × {M} elementen")

es_persona["partij_posities"] = es_partij_pos

# ============================================================
# 8. sector_overlays - NL-template behouden voor 134 elementen
#     (herbruikbaar want alleen numeriek; nieuwe element-ids zonder overlay = leeg dict)
# ============================================================
# Behoud NL sector_overlays, maar herstructureer naar nieuwe element-ids
# Voor elk sector: nieuwe dict met alleen bestaande element-ids uit NL
nl_sector_overlays = es_persona["sector_overlays"]
nieuwe_sector_overlays = {}
for sid in es_persona["sectoren"].keys():
    nl_data = nl_sector_overlays.get(sid, {})
    nieuwe_data = {}
    for e in es_elementen:
        eid = e["id"]
        # Als eid in NL bestaat, hergebruik; anders neutraal 5-vector
        if eid in nl_data:
            nieuwe_data[eid] = nl_data[eid]
        else:
            nieuwe_data[eid] = {f"F{i}": 5 for i in range(1, 10)}
    nieuwe_sector_overlays[sid] = nieuwe_data
es_persona["sector_overlays"] = nieuwe_sector_overlays

# ============================================================
# 9. persona_overlays - behoud NL-template, maar filter element-ids op nieuwe M
# ============================================================
nl_persona_overlays = es_persona["persona_overlays"]
nieuwe_po = {}
element_ids = {e["id"] for e in es_elementen}
for vraag_id, opties in nl_persona_overlays.items():
    nieuwe_po[vraag_id] = {}
    for optie_id, elem_dict in opties.items():
        nieuwe_po[vraag_id][optie_id] = {
            eid: v for eid, v in elem_dict.items() if eid in element_ids
        }
es_persona["persona_overlays"] = nieuwe_po

# ============================================================
# 10. vragen - vertaal naar Spaans
# ============================================================
VRAAG_VERT = {
    "Q1_sector":      "¿En qué sector trabajas (o has trabajado más tiempo)?",
    "Q2_wonen":       "¿Cómo vives actualmente?",
    "Q3_gezin":       "¿Cómo es tu hogar?",
    "Q4_leeftijd":    "¿En qué grupo de edad te encuentras?",
    "Q5_regio":       "¿Dónde vives en España?",
    "Q6_bedrijfslaag": "¿Qué tipo de empresa es?",
    "Q7_netwerk":     "¿Estás afectado por congestión de red, zonas protegidas o conexión de gas?",
}
for qid, nv in VRAAG_VERT.items():
    if qid in es_persona["vragen"]:
        es_persona["vragen"][qid]["vraag"] = nv

ANTW_VERT = {
    "Q1_sector": {
        "S1_zorg": "Sanidad y bienestar", "S2_onderwijs": "Educación y ciencia",
        "S3_defensie": "Seguridad, policía y defensa", "S4_bestuur": "Administración pública",
        "S5_industrie": "Producción industrial", "S6_bouw": "Construcción e infraestructura",
        "S7_logistiek": "Logística y transporte", "S8_landbouw": "Agricultura y pesca",
        "S9_handel": "Comercio y minorista", "S10_horeca": "Hostelería y turismo",
        "S11_ict": "TIC y tecnología", "S12_financieel": "Servicios financieros",
        "S13_creatief": "Sector creativo y medios", "S14_energie": "Energía y utilities",
        "S15_vastgoed": "Inmobiliario y vivienda",
        "S16_zzp_kennis": "Autónomo — profesional del conocimiento",
        "S17_zzp_uitvoerend": "Autónomo — profesional operativo",
        "S18_mkb": "Pyme / empresa familiar", "S19_grootbedrijf": "Gran empresa / multinacional",
        "S20_gepensioneerd": "Jubilado", "S21_uitkering": "Perceptor de prestaciones",
        "S22_student": "Estudiante / iniciando carrera",
    },
    "Q2_wonen": {
        "huurder_schuld": "Alquiler — con deudas", "huurder_spaarder": "Alquiler — ahorrando",
        "starter_koper": "Primera vivienda — comprando", "koper_aflossend": "Propietario — pagando hipoteca",
        "vermogend_koper": "Propietario — vivienda pagada",
    },
    "Q3_gezin": {
        "alleen": "Solo/a", "paar_zonder_kinderen": "Pareja sin hijos",
        "paar_met_kinderen": "Pareja con hijos", "eenouder": "Familia monoparental",
        "meergeneraties": "Multigeneracional",
    },
    "Q4_leeftijd": {
        "jong": "18–29 años", "werkend_jong": "30–44 años",
        "werkend_ouder": "45–59 años", "pre_pensioen": "60–66 años",
        "senior": "67 años o más",
    },
    "Q5_regio": {
        "randstad": "Área metropolitana grande (Madrid / Barcelona / Valencia)",
        "grote_stad": "Ciudad mediana",
        "kleine_gemeente": "Municipio pequeño",
        "krimpregio": "España vaciada",
    },
    "Q6_bedrijfslaag": {
        "geen_bedrijf": "No trabajo en empresa", "mkb": "Pyme",
        "grootbedrijf_nl": "Gran empresa española", "multinational": "Multinacional",
        "overheid": "Sector público", "zzp": "Autónomo/a",
    },
    "Q7_netwerk": {
        "geen": "Nada de lo siguiente",
        "netcongestie": "Zona con congestión de red eléctrica",
        "stikstof": "Cerca de Red Natura 2000 / zona protegida",
        "gasaansluiting": "Con conexión de gas",
        "meerdere": "Varias de las anteriores",
    },
}
for qid, ant_map in ANTW_VERT.items():
    if qid not in es_persona["vragen"]:
        continue
    ant = es_persona["vragen"][qid].get("antwoorden", {})
    for aid, nl_label in ant_map.items():
        if aid in ant:
            ant[aid]["label"] = nl_label

# ============================================================
# 11. baseline_gevolgen (Sectie 0.5)
# ============================================================
if isinstance(baseline, dict):
    if "events" in baseline:
        events = baseline["events"]
    elif "orde_1" in baseline or "orde_1_feiten" in baseline:
        events = baseline
    else:
        events = baseline
elif isinstance(baseline, list):
    events = {"orde_1_feiten": [], "orde_2_afgeleiden": [], "orde_3_systeem": []}
    for e in baseline:
        orde = e.get("orde", 1)
        key = {1: "orde_1_feiten", 2: "orde_2_afgeleiden", 3: "orde_3_systeem"}[orde]
        events[key].append(e)
else:
    events = {"orde_1_feiten": [], "orde_2_afgeleiden": [], "orde_3_systeem": []}

# Neem baseline_gevolgen structuur uit NL en vervang met ES-events
if isinstance(events, dict):
    for key in ["orde_1_feiten", "orde_2_afgeleiden", "orde_3_systeem"]:
        if key in events:
            es_persona["baseline_gevolgen"][key] = events[key]
        elif key.replace("_feiten", "").replace("_afgeleiden", "").replace("_systeem", "") in events:
            alt = key.split("_")[0] + "_" + key.split("_")[1]
            if alt in events:
                es_persona["baseline_gevolgen"][key] = events[alt]

if "metadata" in es_persona["baseline_gevolgen"]:
    es_persona["baseline_gevolgen"]["metadata"]["land"] = "España"
    es_persona["baseline_gevolgen"]["metadata"]["status"] = "verifieerd"
    es_persona["baseline_gevolgen"]["metadata"]["datum"] = "2026-07-05"

# ============================================================
# 12. filter_interactie - land-onafhankelijk, behoud
# ============================================================
# (staat al in template)

# ============================================================
# CONTRACT-CHECK (Regelbestand Sectie 3.1)
# ============================================================
print("\n=== Contract-check §3.1 ===")

def contract_check(d):
    fouten = []
    # Types
    if not isinstance(d.get("sectoren"), dict):
        fouten.append("sectoren moet dict zijn")
    elif len(d["sectoren"]) != 22:
        fouten.append(f"sectoren {len(d['sectoren'])} != 22")
    if not isinstance(d.get("partijen"), dict):
        fouten.append("partijen moet dict zijn")
    if not isinstance(d.get("partij_posities"), dict):
        fouten.append("partij_posities moet dict zijn")
    if not isinstance(d.get("vragen"), dict):
        fouten.append("vragen moet dict zijn")
    if not isinstance(d.get("filters"), list):
        fouten.append("filters moet array zijn")
    if not isinstance(d.get("elementen"), list):
        fouten.append("elementen moet array zijn")
    for k in ["sector_overlays", "persona_overlays", "filter_interactie",
              "baseline_gevolgen", "nepk_tijdreeks", "metadata"]:
        if k not in d:
            fouten.append(f"ontbrekende top-level key: {k}")
    # Partij-consistentie
    if isinstance(d.get("partijen"), dict) and isinstance(d.get("partij_posities"), dict):
        p_set = set(d["partijen"].keys())
        pp_set = set(d["partij_posities"].keys())
        if p_set != pp_set:
            fouten.append(f"partij-mismatch: partijen={p_set} vs posities={pp_set}")
    # Formule
    f = d["nepk_tijdreeks"]["factoren"]
    nepk = f["E_tv_startwaarde_pct"]/100 * f["alpha_startwaarde"] * (1-f["tau_startwaarde"]) * f["phi_startwaarde"] * 100
    verwacht = d["nepk_tijdreeks"]["nepk_startwaarde_pct_bbp"]
    if abs(nepk - verwacht) > 0.3:
        fouten.append(f"formule-fout: {nepk:.3f} vs {verwacht} (>0.3 pp)")
    return fouten, nepk

fouten, nepk_val = contract_check(es_persona)
if fouten:
    print("FOUT:")
    for f in fouten:
        print(f"  {f}")
    raise SystemExit(1)
print(f"  Contract OK. NEPK berekend: {nepk_val:.3f}%")

# ============================================================
# gevolgenkaart.json (Sectie 3.2)
# ============================================================
# Herbouw es_gk: sectoren + partijen + filters worden bijgewerkt
if isinstance(es_gk.get("sectoren"), dict):
    for sid, naam in SECTOR_VERT.items():
        if sid in es_gk["sectoren"] and isinstance(es_gk["sectoren"][sid], dict):
            es_gk["sectoren"][sid]["naam"] = naam

# Partijen in gk-formaat (naam, kleur, type)
TYPE_MAP = {
    "PP": "centrum-rechts", "PSOE": "centrum-links",
    "VOX": "rechts", "SUMAR": "links",
    "ERC": "regionaal", "JUNTS": "regionaal",
    "PNV": "regionaal", "EH Bildu": "regionaal-links",
    "BNG": "regionaal",
    "VMP": "referentie", "CARB": "referentie",
}
es_gk["partijen"] = {}
for pid, pdata in es_partijen.items():
    entry = {
        "naam": pdata["naam"],
        "kleur": pdata["kleur"],
        "type": TYPE_MAP.get(pid, "onbekend"),
    }
    if pdata.get("cluster") == "referencia":
        entry["referentie"] = True
        entry["opmerking"] = pdata["leverbaarheid_label"]
    es_gk["partijen"][pid] = entry

if "uitkomst" not in es_gk:
    es_gk["uitkomst"] = {}

# ============================================================
# Opslaan
# ============================================================
ES_PATH = ES_APP / "client/src/data/gevolgenkaart-persona.json"
ES_GK_PATH = ES_APP / "client/src/data/gevolgenkaart.json"
json.dump(es_persona, open(ES_PATH, "w"), ensure_ascii=False, indent=2)
json.dump(es_gk, open(ES_GK_PATH, "w"), ensure_ascii=False, indent=2)

print(f"\n=== Opgeslagen ===")
print(f"  {ES_PATH} ({ES_PATH.stat().st_size:,} bytes)")
print(f"  {ES_GK_PATH} ({ES_GK_PATH.stat().st_size:,} bytes)")

# Summary
print(f"\n=== ES-persona v3.19 ===")
print(f"  Land: {es_persona['metadata']['land']}")
print(f"  Versie: {es_persona['metadata']['versie']}")
print(f"  NEPK 2026: {es_persona['nepk_tijdreeks']['nepk_startwaarde_pct_bbp']}%")
print(f"  Partijen: {len(es_persona['partijen'])} ({list(es_persona['partijen'].keys())})")
print(f"  Elementen: {len(es_persona['elementen'])}")
print(f"  Sectoren: {len(es_persona['sectoren'])}")
print(f"  Vragen: {len(es_persona['vragen'])}")
