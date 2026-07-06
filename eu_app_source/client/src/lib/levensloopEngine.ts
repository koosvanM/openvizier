// ============================================================================
// LEVENSLOOP-ENGINE
// ----------------------------------------------------------------------------
// Projecteer voor de gebruiker over 15-25 jaar een inkomensindex (basis 100)
// onder:
//   - het computer-advies (vaste partij)
//   - de eigen keuze (vaste partij)
//   - "herkozen bij elke sprong": automatisch de optimale partij per levensfase
// Met onzekerheidsband die lineair groeit van 0% (jaar 0) naar ±25% (jaar 15+).
// ============================================================================

import personaData from '../data/gevolgenkaart-persona.json';
import type { Antwoorden } from './personaEngine';
import { berekenPartij } from './personaEngine';

export type Leeftijdsfase = 'student' | 'starter' | 'midcarriere' | 'senior' | 'preret' | 'pensioen';
export type EconomischeStatus = 'werkend' | 'werkloos' | 'omscholing' | 'inactief';
export interface State { fase: Leeftijdsfase; status: EconomischeStatus; }

// Sector → cluster mapping voor herkeuze-tabel
const SECTOR_CLUSTER: Record<string, string> = {
  S1: 'publiek', S2: 'publiek', S3: 'publiek', S4: 'publiek',
  S5: 'industrie', S6: 'industrie', S7: 'industrie', S8: 'industrie', S14: 'industrie',
  S9: 'diensten', S10: 'diensten', S11: 'diensten', S12: 'diensten', S13: 'diensten',
  S15: 'overig', S16: 'overig', S17: 'overig', S18: 'overig', S19: 'overig', S20: 'overig', S21: 'overig',
  S22: 'student',
};

// Welke partij is optimaal voor (fase, sector-cluster)?
// Gebaseerd op cascade-output gemiddeld voor dat persona.
// EU-VARIANT: gebaseerd op fractie-portfolio's in EP 2024-2029
// - Student/starter: Greens/EFA en S&D vanwege sociaal-progressieve prioriteiten
// - Mid-carrière/senior in industrie/diensten: EPP en Renew Europe (interne markt)
// - Pensioen: EPP (behoud koopkracht, gezondheidszorg via nationale competentie)
const OPTIMAAL: Record<string, string> = {
  'student|student':   'Greens/EFA',
  'student|publiek':   'S&D',
  'student|industrie': 'S&D',
  'student|diensten':  'Renew Europe',
  'student|overig':    'S&D',
  'starter|publiek':   'S&D',
  'starter|industrie': 'EPP',
  'starter|diensten':  'Renew Europe',
  'starter|student':   'S&D',
  'starter|overig':    'S&D',
  'midcarriere|publiek':   'S&D',
  'midcarriere|industrie': 'EPP',
  'midcarriere|diensten':  'Renew Europe',
  'midcarriere|student':   'S&D',
  'midcarriere|overig':    'EPP',
  'senior|publiek':   'EPP',
  'senior|industrie': 'EPP',
  'senior|diensten':  'EPP',
  'senior|student':   'S&D',
  'senior|overig':    'EPP',
  'preret|publiek':   'EPP',
  'preret|industrie': 'EPP',
  'preret|diensten':  'EPP',
  'preret|student':   'EPP',
  'preret|overig':    'EPP',
  'pensioen|publiek':   'EPP',
  'pensioen|industrie': 'EPP',
  'pensioen|diensten':  'EPP',
  'pensioen|student':   'EPP',
  'pensioen|overig':    'EPP',
};

function besteVoor(state: State, sector: string): string {
  const cluster = SECTOR_CLUSTER[sector] || 'diensten';
  return OPTIMAAL[`${state.fase}|${cluster}`] || 'PP';
}

// Bepaal start-state uit de antwoorden (leeftijd + sector + status)
export function startStateUitAntwoorden(antwoorden: Antwoorden): State {
  const sector = antwoorden.Q1_sector || '';
  const leeftijd = antwoorden.Q4_leeftijd || '';
  if (sector === 'S22_student') return { fase: 'student', status: 'inactief' };
  if (leeftijd.includes('22') || leeftijd.includes('29')) return { fase: 'starter', status: 'werkend' };
  if (leeftijd.includes('30') || leeftijd.includes('49')) return { fase: 'midcarriere', status: 'werkend' };
  if (leeftijd.includes('50') || leeftijd.includes('60')) return { fase: 'senior', status: 'werkend' };
  if (leeftijd.includes('67') && leeftijd.includes('-')) return { fase: 'preret', status: 'werkend' };
  if (leeftijd.includes('67') || leeftijd.includes('AOW') || leeftijd.includes('pensioen')) {
    return { fase: 'pensioen', status: 'inactief' };
  }
  return { fase: 'midcarriere', status: 'werkend' };
}

// Anker-inkomensindex per state. Schaal: een midcarriere-werkend = 6.0,
// daarvan wordt jaar 0 van de gebruiker basis 100 (genormaliseerd).
// De relatieve verhoudingen bepalen hoe groot de sprong tussen levensfasen is.
// De studenten-sprong is in werkelijkheid groot, maar voor visualisatie dempen we
// dat naar een redelijkere factor (~2.5×) zodat de grafiek leesbaar blijft.
const STATE_NIVEAU: Record<string, number> = {
  'student|inactief':  0.40,
  'student|werkend':   0.95,
  'student|werkloos':  0.30,
  'student|omscholing': 0.50,
  'starter|werkend':   1.80,
  'starter|werkloos':  1.00,
  'starter|omscholing': 1.10,
  'starter|inactief':  0.55,
  'midcarriere|werkend':  3.00,
  'midcarriere|werkloos': 1.65,
  'midcarriere|omscholing': 1.80,
  'midcarriere|inactief': 0.70,
  'senior|werkend':   3.70,
  'senior|werkloos':  1.95,
  'senior|omscholing': 2.15,
  'senior|inactief':  0.85,
  'preret|werkend':   4.00,
  'preret|werkloos':  2.05,
  'preret|omscholing': 1.95,
  'preret|inactief':  1.80,
  'pensioen|inactief': 1.45,
  'pensioen|werkend':  1.85,
  'pensioen|werkloos': 1.45,
  'pensioen|omscholing': 1.45,
};

function nivVoor(state: State): number {
  return STATE_NIVEAU[`${state.fase}|${state.status}`] || 5.0;
}

// Volgende fase-overgang
const VOLGENDE_FASE: Record<Leeftijdsfase, Leeftijdsfase> = {
  student: 'starter',
  starter: 'midcarriere',
  midcarriere: 'senior',
  senior: 'preret',
  preret: 'pensioen',
  pensioen: 'pensioen',
};

// Gemiddelde fase-duur (jaren)
const FASE_DUUR: Record<Leeftijdsfase, number> = {
  student: 4, starter: 8, midcarriere: 20, senior: 10, preret: 5, pensioen: 20,
};

// Modaal traject: voor één state-pad over de tijd
function modaalPad(start: State, jaren: number): State[] {
  const pad: State[] = [start];
  let huidig = start;
  let jaren_in_fase = 0;
  for (let j = 1; j <= jaren; j++) {
    jaren_in_fase++;
    const duur = FASE_DUUR[huidig.fase];
    if (jaren_in_fase >= duur && huidig.fase !== 'pensioen') {
      const nieuwe_fase = VOLGENDE_FASE[huidig.fase];
      const nieuwe_status: EconomischeStatus = nieuwe_fase === 'pensioen' ? 'inactief' : 'werkend';
      huidig = { fase: nieuwe_fase, status: nieuwe_status };
      jaren_in_fase = 0;
    }
    pad.push(huidig);
  }
  return pad;
}

// Partij-effect per jaar op inkomensindex (relatieve groei).
// Gebaseerd op cascade-output van die partij voor de gebruiker. Per orde een tijdsenvelop.
function partijGroeiPerJaar(
  antwoorden: Antwoorden,
  partij: string,
  jaren: number,
  filterSubset?: number[],
): number[] {
  // Bereken cascade-output voor deze partij.
  // filterSubset: optionele lijst van filter-indices (0..8) om alleen die filters
  //   mee te nemen. undefined = alle 9 filters (persoonlijk/algemeen effect).
  //   [0,1,2] = NEPK + Bedrijvigheid + Investering (productieve kern, landsniveau).
  let v1 = 0, v2 = 0, v3 = 0;
  try {
    const r = berekenPartij(partij, antwoorden);
    if (filterSubset && filterSubset.length > 0) {
      v1 = filterSubset.reduce((s, i) => s + (r.v1[i] || 0), 0);
      v2 = filterSubset.reduce((s, i) => s + (r.v2[i] || 0), 0);
      v3 = filterSubset.reduce((s, i) => s + (r.v3[i] || 0), 0);
    } else {
      v1 = r.eerste_orde;
      v2 = r.tweede_orde;
      v3 = r.derde_orde;
    }
  } catch (e) {
    return new Array(jaren+1).fill(0);
  }

  // Convert cascade-score → jaarlijkse groei %. Schalen zodat realistische bandbreedte:
  // v1 van bv. +300 → ~+2.5% per jaar gedurende 1e orde-venster
  const groei = new Array(jaren+1).fill(0);
  for (let j = 0; j <= jaren; j++) {
    // v3.20.14 — Envelope teruggezet naar v3.20.11-vorm. De knik-fix zit nu
    // fundamenteel elders (cubic-fit door 3 ankerpunten, zie Regel 144).
    // 1e orde tijdsenvelop: piek jaar 1, dempt uit jaar 5
    const env1 = j === 0 ? 0 : Math.max(0, 1 - j/5);
    // 2e orde tijdsenvelop: klokvormig piek jaar 3
    const env2 = j === 0 ? 0 : Math.exp(-Math.pow((j-3)/3, 2));
    // 3e orde tijdsenvelop: oplopend vanaf jaar 5, blijvend
    const env3 = j < 3 ? 0 : Math.min(1, (j-3)/6);
    // Effect per orde, conservatief geschaald: max ±3% per jaar bij sterke cascade.
    // Cascade-score van ~500 (sterk positief) levert ~0.5% jaarlijkse groei.
    // v3.20.11 — orde-multipliers voor VMP en CARB (referentie-modellen).
    // 1e orde: normaal (langzame startfase). 2e/3e orde: extreem oplopend, want
    // deze modellen zetten volledig door op systeem-hervorming (CARB > VMP).
    const isVMP = partij === 'VMP';
    const isCARB = partij === 'CARB';
    const mult2 = isCARB ? 1.8 : (isVMP ? 1.4 : 1.0);
    const mult3 = isCARB ? 2.5 : (isVMP ? 1.8 : 1.0);
    const eff1 = (v1 / 5000) * env1;
    const eff2 = (v2 / 5000) * env2 * mult2;
    const eff3 = (v3 / 5000) * env3 * mult3;
    groei[j] = eff1 + eff2 + eff3;
  }
  return groei;
}

// Regel 103 v3.9 — baseline-drift model
// De nullijn is niet vlak 100 maar volgt de structurele beweging van de
// Nederlandse economie zonder partij-interventie. Elk feit heeft een eigen
// curve-vorm en tijdsprofiel; alle bijdragen worden per jaar geintegreerd.
export type CurveType = 'immediate_plateau' | 'rise_plateau' | 'spike' | 'delayed_onset' | 'cumulative';

export interface BaselineDriftItem {
  beschrijving: string;
  bron_url: string;
  bron_datum: string;
  delta_pct: number;
  filter_index?: number;
  orde?: 1 | 2 | 3;
  piek_jaar: number;
  afloop_jaar: number;
  curve_type: CurveType;
}

export interface BaselineDriftResultaat {
  drift_index: number[];
  drift_orde1: number[];
  drift_orde2: number[];
  drift_orde3: number[];
  som_orde1_pct: number;
  som_orde2_pct: number;
  som_orde3_pct: number;
  aantal_items: { orde1: number; orde2: number; orde3: number };
  peildatum: string;
}

function curveWaarde(j: number, piek: number, afloop: number, curve: CurveType): number {
  if (j <= 0) return curve === 'immediate_plateau' ? 1 : 0;
  if (curve === 'immediate_plateau') return j >= afloop ? 0 : 1;
  if (curve === 'rise_plateau') {
    if (j <= piek) return j / piek;
    if (j <= afloop) return 1;
    return 0;
  }
  if (curve === 'spike') {
    if (j <= piek) return j / piek;
    if (j >= afloop) return 0;
    return 1 - (j - piek) / Math.max(1, afloop - piek);
  }
  if (curve === 'delayed_onset') {
    if (j <= piek) return Math.pow(j / piek, 2);
    if (j <= afloop) return 1;
    return 0;
  }
  if (curve === 'cumulative') {
    return Math.min(1, j / Math.max(1, afloop));
  }
  return 0;
}

export function berekenBaselineDrift(jaren: number = 15): BaselineDriftResultaat {
  const bg: any = (personaData as any).baseline_gevolgen || {};
  const orde1: BaselineDriftItem[] = bg.orde_1_feiten || [];
  const orde2: BaselineDriftItem[] = bg.orde_2_afgeleiden || [];
  const orde3: BaselineDriftItem[] = bg.orde_3_systeem || [];

  const drift_orde1 = new Array(jaren + 1).fill(0);
  const drift_orde2 = new Array(jaren + 1).fill(0);
  const drift_orde3 = new Array(jaren + 1).fill(0);
  const drift_index = new Array(jaren + 1).fill(100);

  // v3.20.4: piek_jaar en afloop_jaar zijn kalenderjaren (bv. 2020, 2023).
  // De projectie start op peildatum (bv. 2026). Zet om naar jaar-indices 0..jaren.
  // Events die volledig vóór peildatum liggen krijgen tijdsvenster [0,0] — geen bijdrage.
  const nt: any = (personaData as any).nepk_tijdreeks || {};
  const peildatum = new Date(nt.peildatum || '2026-07-04');
  const start_kalenderjaar = peildatum.getFullYear();

  function verwerk(items: BaselineDriftItem[], doel: number[]) {
    for (const it of items) {
      const delta = it.delta_pct || 0;
      const piek_raw = it.piek_jaar || 5;
      const afloop_raw = it.afloop_jaar || jaren;
      // Detecteer of het kalenderjaar (≥ 2000) of relatief-index (< 100) is
      const piek_kalendar = piek_raw >= 2000;
      const afloop_kalendar = afloop_raw >= 2000;
      const piek_idx = piek_kalendar ? piek_raw - start_kalenderjaar : piek_raw;
      const afloop_idx = afloop_kalendar ? afloop_raw - start_kalenderjaar : afloop_raw;
      // v3.20.8: Als het event volledig in het verleden ligt: skip.
      // Voorheen (v3.20.4) skipten we alleen `afloop_idx < 0`, waardoor events met
      // afloop = peildatum (idx = 0) door glipten. Bij piek_kalendar < peildatum werd
      // piek_idx geclampt naar 0; met curve 'cumulative' en afloop=0 leverde dat
      // curveWaarde=1 op vanaf jaar 1 — dus historische events zoals NextGenerationEU
      // (afloop 2026) sprongen als volle bijdrage in jaar 1 van de projectie.
      // Correcte regel: event hoort alleen als afloop STRIKT NA peildatum ligt.
      if (afloop_idx <= 0) continue;
      const piek = Math.max(0, Math.min(jaren, piek_idx));
      const afloop = Math.max(0, Math.min(jaren, afloop_idx));
      const curve = it.curve_type || 'rise_plateau';
      for (let j = 0; j <= jaren; j++) {
        doel[j] += delta * curveWaarde(j, piek, afloop, curve);
      }
    }
  }

  verwerk(orde1, drift_orde1);
  verwerk(orde2, drift_orde2);
  verwerk(orde3, drift_orde3);

  for (let j = 0; j <= jaren; j++) {
    const cum = drift_orde1[j] + drift_orde2[j] + drift_orde3[j];
    drift_index[j] = 100 * Math.exp(cum / 100);
  }

  // v3.20.15 — Regel 144: cubic-fit door ankers j=0,3,7,15 zodat de
  // nullijn (drift_index) geen knik meer heeft bij orde-overgangen.
  cubicFitDoorAnkers(drift_index);
  cubicFitDoorAnkers(drift_orde1);
  cubicFitDoorAnkers(drift_orde2);

  return {
    drift_index,
    drift_orde1, drift_orde2, drift_orde3,
    som_orde1_pct: drift_orde1[jaren],
    som_orde2_pct: drift_orde2[jaren],
    som_orde3_pct: drift_orde3[jaren],
    aantal_items: { orde1: orde1.length, orde2: orde2.length, orde3: orde3.length },
    peildatum: bg.metadata?.peildatum || 'onbekend',
  };
}

// Regel 116-122 v3.12 — Vier-factor NEPK-formule + drie-orde-modulatie
// NEPK = E_tv × α × (1−τ) × φ  (canonieke formule, bron: nepk-indicator-methodologie.pdf)
// NTPK = E_tv × α × (1−τ)      (NEPK zonder eigendom-filter, regel 117)
// Startwaarden 2026 (eigen berekening, regel 117): E_tv=31%, α=0,40, τ=0,43, φ=0,53
//   → NTPK=7,07%, NEPK=3,75%
// Drie-orde-modulatie (regel 118): 1e orde jaar 1-3, 2e orde jaar 4-8, 3e orde jaar 9-15
// Historische baseline (regel 121): trend 2000-2026 zonder ombuiging
export interface NEPKResultaat {
  jaren: number[];
  kalender_jaren: number[];

  // Regel 116 v3.12 — vier factoren als aparte tijdreeksen
  E_tv_pct: number[];      // export-toegevoegde waarde % BBP
  alpha_index: number[];   // productieve kern-index 0-1
  tau_index: number[];     // collectieve lastendruk-index 0-1
  phi_index: number[];     // aandeel nationaal eigendom-index 0-1

  // Regel 117 v3.12 — afgeleide grootheden
  ntpk_pct_bbp: number[];  // NTPK = E_tv × α × (1−τ)
  nepk_pct_bbp: number[];  // NEPK = NTPK × φ
  npk_pct_bbp: number[];   // v3.20.6: NPK = NTPK × (1 + ψ), Nationaal Productief Kapitaal incl. buitenland
  ntpk_startwaarde_pct: number;
  npk_startwaarde_pct: number;  // v3.20.6
  startwaarde_pct: number; // NEPK startwaarde 3,75%
  kritische_grens: number; // 3,0% BBP
  point_of_no_return: number; // 2,0% BBP
  jaar_onder_grens: number | null;
  jaar_point_of_no_return: number | null;

  // Regel 121 v3.12 — historische baseline (grijze lijn)
  baseline_ntpk_pct: number[];
  baseline_nepk_pct: number[];

  // Regel 115 v3.11 — schuld-service (rente + aflossing, % BBP/jaar)
  schuld_service_pct_bbp: number[];
  schuld_service_startwaarde: number;
  schuld_service_uitmergel_drempel: number;
  jaar_uitmergel_intreedt: number | null;

  // Regel 115 v3.11 — netto-gezondheid = NEPK − schuld-service − uitmergel-drift
  netto_gezondheid_pct_bbp: number[];
  netto_gezondheid_jaar_onder_grens: number | null;

  // Regel 122 v3.12 — BBP-index (referentie 2026 = 100)
  bbp_index: number[];

  // Regel 118 v3.12 — drie-orde-modulatie diagnostiek per factor
  drie_orde_scoring: {
    E_tv:   { orde1: number; orde2: number; orde3: number; cumulatief_15j: number };
    alpha:  { orde1: number; orde2: number; orde3: number; cumulatief_15j: number };
    tau:    { orde1: number; orde2: number; orde3: number; cumulatief_15j: number };
    phi:    { orde1: number; orde2: number; orde3: number; cumulatief_15j: number };
  };

  // Legacy velden (v3.11) — behouden voor backwards compat
  fdi_afhankelijkheid_pct_bbp: number[];
  fdi_startwaarde_pct: number;
  daling_midden: number;
  partij_modulatie_nepk_pp: number;
  partij_modulatie_fdi_pp: number;
  partij_modulatie_schuld_pp: number;
  partij_naam: string;
}

// Regel 120 v3.12 — drie-orde-scoring per partij (top-6 + VMP + CARB)
// Elke waarde is pp/jaar; negatief = verlaging factor, positief = verhoging.
// Voor τ: negatief = lastenverlaging (gunstig voor NEPK).
interface OrdeScoring {
  E_tv: [number, number, number];   // [orde1, orde2, orde3]
  alpha: [number, number, number];
  tau: [number, number, number];
  phi: [number, number, number];
}
// Regel 120 v3.12c — alle 17 partijen gescoord volgens links-rechts-heuristiek
// Grondregel gebruiker: links = eerst uitgeven, dan verdienen (τ+, α/φ-)
//                        rechts = eerst verdienen, dan uitgeven (τ-, α/φ+)
// PRO: 1e orde klein, 2e/3e orde erg negatief (uitgesproken door gebruiker)
// PP/VOX: sterker positief
const DRIE_ORDE_TABEL: Record<string, OrdeScoring> = {
  // === Referentie-modellen (V4-standaard, ongewijzigd) ===
  VMP:        { E_tv: [0.06, 0.12, 0.2], alpha: [0.003, 0.006, 0.01],
               tau:  [-0.002, -0.003, -0.005], phi: [0.004, 0.009, 0.015] },
  CARB:       { E_tv: [0.01, 0.1, 0.34], alpha: [0.001, 0.01, 0.034],
               tau:  [0, -0.005, -0.017], phi: [0.001, 0.01, 0.034] },

  // === EP-fracties 2024-2029 — geordend op CHES-positie links → rechts ===
  // The Left: The Left (CHES 0.19, zelfs iets radicaler dan SUMAR's 0.23) krijgt de sterkste l
  'The Left':     { E_tv: [-0.02, -0.045, -0.08], alpha: [-0.003, -0.007, -0.013],
                    tau:  [0.003, 0.005, 0.008], phi: [-0.0015, -0.004, -0.009] },
  // Greens/EFA: Greens/EFA (CHES 0.28, vergelijkbaar met SUMAR 0.23) krijgt op basis van de kali
  'Greens/EFA':   { E_tv: [-0.015, -0.035, -0.055], alpha: [-0.002, -0.003, 0.0],
                    tau:  [0.0025, 0.0045, 0.007], phi: [-0.0015, -0.004, -0.008] },
  // S&D: S&D (CHES 0.38, vergelijkbaar met PSOE 0.39) volgt de linkse NEPK-regel 'eerst u
  'S&D':          { E_tv: [0.012, 0.022, 0.04], alpha: [0.0, -0.001, -0.002],
                    tau:  [0.0025, 0.0035, 0.005], phi: [0.001, 0.002, 0.003] },
  // NI: NI (CHES 0.55, mediaan van een zeer heterogene groep van BSW links-soevereinisti
  NI:             { E_tv: [0.001, 0.002, 0.003], alpha: [0.0001, 0.0002, 0.0003],
                    tau:  [-0.0001, -0.00015, -0.0002], phi: [0.0001, 0.0001, 0.0001] },
  // Renew Europe: Renew Europe (CHES 0.58) is een licht rechts-liberaal draaipunt: NEPK 'eerst ver
  'Renew Europe': { E_tv: [0.03, 0.055, 0.09], alpha: [0.0015, 0.003, 0.005],
                    tau:  [-0.0015, -0.0025, -0.0035], phi: [0.0, 0.0005, -0.001] },
  // EPP: EPP is een gematigd-rechtse (CHES 0.65) spilfractie met hoge leverbaarheid (0.85
  EPP:            { E_tv: [0.035, 0.06, 0.1], alpha: [0.002, 0.004, 0.007],
                    tau:  [-0.0025, -0.0035, -0.0045], phi: [0.001, 0.002, 0.004] },
  // ECR: ECR (CHES 0.82) valt onder de VOX-schaal-kalibratie voor CHES > 0.80: NEPK 'eers
  ECR:            { E_tv: [0.015, 0.025, 0.035], alpha: [0.0015, 0.0025, 0.003],
                    tau:  [-0.0035, -0.0045, -0.006], phi: [0.0015, 0.0005, -0.002] },
  // PfE: PfE (CHES 0.85) volgt de expliciete EU-context-regel voor anti-EU-fracties, die 
  PfE:            { E_tv: [-0.025, -0.06, -0.11], alpha: [-0.003, -0.007, -0.012],
                    tau:  [-0.002, -0.0025, -0.003], phi: [0.0005, -0.002, -0.006] },
  // ESN: ESN (CHES 0.91, hoogste in de tabel) heeft programmatisch het meest radicale ant
  ESN:            { E_tv: [-0.015, -0.035, -0.07], alpha: [-0.0015, -0.004, -0.007],
                    tau:  [-0.001, -0.0015, -0.002], phi: [0.0003, -0.001, -0.0035] },
};

function getPartijScoring(partij: string): OrdeScoring {
  // EU-varianten: partij-namen zoals 'S&D', 'Greens/EFA', 'The Left', 'Renew Europe' behouden hun exacte case+spaties
  if (DRIE_ORDE_TABEL[partij]) return DRIE_ORDE_TABEL[partij];
  const upper = partij.toUpperCase();
  if (DRIE_ORDE_TABEL[upper]) return DRIE_ORDE_TABEL[upper];
  // Fallback: nul-modulatie
  return {
    E_tv: [0, 0, 0], alpha: [0, 0, 0], tau: [0, 0, 0], phi: [0, 0, 0]
  };
}

// Regel 122 v3.12c — vergelijkingsbundel: 8 belangrijkste partijen voor bundel-grafiek
// EU-VARIANT: 8 grootste fracties + VMP+CARB als referentie voor vergelijkings-bundel
export const NEPK_BUNDEL_PARTIJEN = ['VMP', 'CARB', 'EPP', 'S&D', 'Renew Europe', 'Greens/EFA', 'ECR', 'PfE', 'The Left', 'ESN'];

// Bereken de NEPK-tijdreeks voor één partij zonder alle diagnostiek (voor bundel-lijnen)
// v3.20.6: retourneert nu ook NPK (Nationaal Productief Kapitaal) = NTPK + eigen productie in buitenland
// NPK = NTPK × (1 + ψ), waar ψ = ratio buitenlandse Spaanse productie / NTPK
// v3.20.14 — Regel 144: cubic-fit door 3 ankerpunten (j=3, 7, 15).
// Helper: fit een gladde derdegraadspolynoom door (0, A[0]), (3, A[3]),
// (7, A[7]), (15, A[15]) en overschrijf alle andere indices met de
// polynoom-waarde. Verwijdert de sprongen bij j=3→4 en j=8→9 die door
// ordeVoorJaar-stap-functie ontstaan zonder de ankerpunten (uit onderzoek)
// aan te raken.
function cubicFitDoorAnkers(A: number[]): void {
  if (!A || A.length < 16) return;
  const y0 = A[0], y3 = A[3], y7 = A[7], y15 = A[15];
  // Inverse van 4x4 Vandermonde-achtige matrix, hardcoded:
  const a = y0;
  const b = -y0 * 19/35 + y3 * 35/48 - y7 * 45/224 + y15 * 7/480;
  const c =  y0 * 5/63  - y3 * 11/72 + y7 * 9/112  - y15 / 144;
  const d = -y0 / 315   + y3 / 144   - y7 / 224    + y15 / 1440;
  for (let j = 1; j < 15; j++) {
    A[j] = a + b*j + c*j*j + d*j*j*j;
  }
}

export function bundelNEPKLijn(partij: string, jaren: number = 15): { nepk: number[]; ntpk: number[]; npk: number[] } {
  const nt: any = (personaData as any).nepk_tijdreeks || {};
  const E_tv_0 = nt.factoren?.E_tv_startwaarde_pct ?? 17.7;
  const alpha_0 = nt.factoren?.alpha_startwaarde ?? 0.47;
  const tau_0 = nt.factoren?.tau_startwaarde ?? 0.404;
  const phi_0 = nt.factoren?.phi_startwaarde ?? 0.904;
  const psi_0 = nt.factoren?.psi_startwaarde ?? 0.0;  // v3.20.6: buitenlandse-productie-ratio

  const partijenObj: any = (personaData as any).partijen || {};
  const lev = partijenObj[partij]?.leverbaarheid ?? 0.5;
  const scoring = getPartijScoring(partij);

  function ordeVoorJaar(j: number): 0 | 1 | 2 {
    if (j <= 3) return 0;
    if (j <= 8) return 1;
    return 2;
  }

  const nepk: number[] = [];
  const ntpk: number[] = [];
  const npk: number[] = [];  // v3.20.6: NPK = NTPK × (1 + ψ)
  let E = E_tv_0, a = alpha_0, t = tau_0, p = phi_0;

  // v3.20.3: baseline-drift + partij-ombuiging (zie berekenNEPK-motorfix)
  const BASELINE_dEtv = 0.27;    // EU-27 2000-2024: +0,27 pp/jaar (Eurostat FIGARO)
  const BASELINE_dalpha = -0.0009; // EU-27: industrie -0,09 pp/jaar (Eurostat nama_10)
  const BASELINE_dtau = 0.0003;    // EU-27: tax-to-GDP ~vlak, +0,03 pp/jaar
  const BASELINE_dphi = -0.0005;   // EU-27: FDI-inward stock proxy, milde stijging niet-EU-controle

  for (let j = 0; j <= jaren; j++) {
    const ntpk_j = E * a * (1 - t);
    const nepk_j = ntpk_j * p;
    const npk_j = ntpk_j * (1 + psi_0);  // v3.20.6: NPK = NTPK + buitenlandse Spaanse productie
    ntpk.push(Math.max(0, ntpk_j));
    nepk.push(Math.max(0, nepk_j));
    npk.push(Math.max(0, npk_j));
    if (j === jaren) break;
    const orde = ordeVoorJaar(j + 1);
    E += BASELINE_dEtv + scoring.E_tv[orde] * lev;
    a = Math.max(0.05, Math.min(0.95, a + BASELINE_dalpha + scoring.alpha[orde] * lev));
    t = Math.max(0.10, Math.min(0.90, t + BASELINE_dtau + scoring.tau[orde] * lev));
    p = Math.max(0.05, Math.min(0.95, p + BASELINE_dphi + scoring.phi[orde] * lev));
  }
  // v3.20.14 — Regel 144: cubic-fit door ankers j=0,3,7,15 om de knik-sprongen
  // uit de discrete orde-overgangen (j=3→4, j=8→9) weg te werken.
  cubicFitDoorAnkers(nepk);
  cubicFitDoorAnkers(ntpk);
  cubicFitDoorAnkers(npk);
  return { nepk, ntpk, npk };
}

export function berekenNEPK(
  antwoorden: Antwoorden,
  partij: string,
  jaren: number = 15,
): NEPKResultaat {
  const nt: any = (personaData as any).nepk_tijdreeks || {};
  const kritische_grens = nt.kritische_grens_pct_bbp || 3.0;
  const point_of_no_return = nt.point_of_no_return_pct_bbp || 2.0;
  const peildatum = new Date(nt.peildatum || '2026-07-04');
  const start_kalenderjaar = peildatum.getFullYear();

  // Regel 117 v3.12 — startwaarden vier factoren (2026)
  const E_tv_0 = nt.factoren?.E_tv_startwaarde_pct ?? 17.7;
  const alpha_0 = nt.factoren?.alpha_startwaarde ?? 0.47;
  const tau_0 = nt.factoren?.tau_startwaarde ?? 0.404;
  const phi_0 = nt.factoren?.phi_startwaarde ?? 0.904;
  const psi_0 = nt.factoren?.psi_startwaarde ?? 0.0;  // v3.20.6: buitenlandse-productie-ratio

  // Legacy compatibiliteit
  const fdi_startwaarde = nt.fdi_afhankelijkheid_pct_bbp?.startwaarde ?? 45.0;
  const schuld_startwaarde = nt.schuld_service_pct_bbp?.startwaarde ?? 2.4;
  const uitmergel_drempel = nt.schuld_service_pct_bbp?.kritische_drempel_uitmergel_pct ?? 5.0;

  // Regel 118 v3.12 — drie-orde-scoring ophalen voor deze partij
  const partijenObj: any = (personaData as any).partijen || {};
  const lev = partijenObj[partij]?.leverbaarheid ?? 0.5;
  const scoring = getPartijScoring(partij);

  // Legacy v1[F1..F5] blijven berekenen voor coalitie-vulling en legacy velden
  const alleKiesbaar = Object.keys((personaData as any).partij_posities).filter((pid: string) => {
    const m = partijenObj[pid];
    return m && m.referentie !== true;
  });
  const coalitieVullers = alleKiesbaar.filter(pid => pid !== partij);
  const coalitieProduct: Record<string, number> = {};
  for (const el of (personaData as any).elementen) {
    let som = 0; let gewicht = 0;
    for (const pid of coalitieVullers) {
      const pd = (personaData as any).partij_posities[pid]?.[el.id];
      if (!pd) continue;
      const p = (pd.positie == null) ? 0 : pd.positie;
      const i = (pd.intensiteit == null) ? 0 : pd.intensiteit;
      if (p === 0 || i === 0) continue;
      const iNorm = i > 1.0 ? i / 10.0 : i;
      const w = typeof partijenObj[pid]?.leverbaarheid === 'number' ? partijenObj[pid].leverbaarheid : 0.50;
      som += w * (p / 2.0) * iNorm;
      gewicht += w;
    }
    coalitieProduct[el.id] = gewicht > 0 ? som / gewicht : 0;
  }
  let v1_F1 = 0, v1_F3 = 0, v1_F5 = 0;
  for (const el of (personaData as any).elementen) {
    const pd = (personaData as any).partij_posities[partij]?.[el.id];
    if (!pd) continue;
    const positie = pd.positie || 0;
    const intens = pd.intensiteit || 0;
    let posIntProduct: number;
    if (positie === 0 || intens === 0) {
      posIntProduct = coalitieProduct[el.id];
      if (posIntProduct === 0) continue;
    } else {
      const iNorm = intens > 1.0 ? intens / 10.0 : intens;
      posIntProduct = (positie / 2.0) * iNorm;
    }
    v1_F5 += ((el.basis?.[4] ?? 5) - 5) * posIntProduct;
    v1_F1 += ((el.basis?.[0] ?? 5) - 5) * posIntProduct;
    v1_F3 += ((el.basis?.[2] ?? 5) - 5) * posIntProduct;
  }
  v1_F1 *= lev; v1_F3 *= lev; v1_F5 *= lev;

  // Legacy schuld-service modulatie (F5)
  const conv_schuld = 0.01;
  const mod_schuld_pp = -v1_F5 * conv_schuld;
  const eff_stijging_schuld = Math.max(-0.1, mod_schuld_pp);

  // Regel 118 — bepaal welke orde in welk jaar actief is
  function ordeVoorJaar(j: number): 0 | 1 | 2 {
    if (j <= 3) return 0;      // 1e orde
    if (j <= 8) return 1;      // 2e orde
    return 2;                  // 3e orde
  }

  // Tijdreeksen
  const E_tv_pct: number[] = [];
  const alpha_index: number[] = [];
  const tau_index: number[] = [];
  const phi_index: number[] = [];
  const ntpk_pct_bbp: number[] = [];
  const nepk_pct_bbp: number[] = [];
  const npk_pct_bbp: number[] = [];  // v3.20.6
  const baseline_ntpk_pct: number[] = [];
  const baseline_nepk_pct: number[] = [];
  const bbp_index: number[] = [];
  const schuld_pct_bbp: number[] = [];
  const netto_gezondheid: number[] = [];
  const kalender_jaren: number[] = [];
  const fdi_pct_bbp: number[] = [];
  let jaar_onder_grens: number | null = null;
  let jaar_point_of_no_return: number | null = null;
  let jaar_uitmergel_intreedt: number | null = null;
  let netto_jaar_onder_grens: number | null = null;

  // Historische baseline-drift (regel 121) — zonder ombuiging
  // Historisch tempo 2000-2026 (26 jaar):
  //   E_tv: +0,15 pp/j, α: -0,0077, τ: +0,0031, φ: -0,0104
  const BASELINE_dEtv = 0.27;    // EU-27 2000-2024: +0,27 pp/jaar (Eurostat FIGARO)
  const BASELINE_dalpha = -0.0009; // EU-27: industrie -0,09 pp/jaar (Eurostat nama_10)
  const BASELINE_dtau = 0.0003;    // EU-27: tax-to-GDP ~vlak, +0,03 pp/jaar
  const BASELINE_dphi = -0.0005;   // EU-27: FDI-inward stock proxy, milde stijging niet-EU-controle

  let E_tv = E_tv_0, alpha = alpha_0, tau = tau_0, phi = phi_0;
  let b_Etv = E_tv_0, b_alpha = alpha_0, b_tau = tau_0, b_phi = phi_0;
  let S = schuld_startwaarde;
  let cumulatieve_uitmergel_drift = 0;

  // BBP-index start op 100 in jaar 0; groeit langzaam met NEPK-versterking
  let bbp_idx = 100;

  const startNTPK = E_tv_0 * alpha_0 * (1 - tau_0);
  const startNEPK = startNTPK * phi_0;
  const startNPK = startNTPK * (1 + psi_0);  // v3.20.6

  for (let j = 0; j <= jaren; j++) {
    // Registreer huidige waarden
    const ntpk = E_tv * alpha * (1 - tau);
    const nepk = ntpk * phi;
    const npk = ntpk * (1 + psi_0);  // v3.20.6: NPK = NTPK × (1 + ψ)
    E_tv_pct.push(E_tv);
    alpha_index.push(alpha);
    tau_index.push(tau);
    phi_index.push(phi);
    ntpk_pct_bbp.push(Math.max(0, ntpk));
    nepk_pct_bbp.push(Math.max(0, nepk));
    npk_pct_bbp.push(Math.max(0, npk));

    // Baseline
    const b_ntpk = b_Etv * b_alpha * (1 - b_tau);
    const b_nepk = b_ntpk * b_phi;
    baseline_ntpk_pct.push(Math.max(0, b_ntpk));
    baseline_nepk_pct.push(Math.max(0, b_nepk));

    // BBP-index: partij-effect via NEPK-groei
    bbp_index.push(bbp_idx);

    // Schuld-service en netto-gezondheid (v3.11 mechaniek behouden)
    const overshoot = Math.max(0, S - uitmergel_drempel);
    cumulatieve_uitmergel_drift += 0.15 * overshoot;
    const netto = Math.max(0, nepk - S - cumulatieve_uitmergel_drift);
    schuld_pct_bbp.push(Math.max(0, S));
    netto_gezondheid.push(netto);
    kalender_jaren.push(start_kalenderjaar + j);
    fdi_pct_bbp.push(fdi_startwaarde);  // legacy, geen actieve modulatie meer

    if (jaar_onder_grens === null && nepk < kritische_grens) {
      jaar_onder_grens = start_kalenderjaar + j;
    }
    if (jaar_point_of_no_return === null && nepk < point_of_no_return) {
      jaar_point_of_no_return = start_kalenderjaar + j;
    }
    if (jaar_uitmergel_intreedt === null && S >= uitmergel_drempel) {
      jaar_uitmergel_intreedt = start_kalenderjaar + j;
    }
    if (netto_jaar_onder_grens === null && netto < kritische_grens) {
      netto_jaar_onder_grens = start_kalenderjaar + j;
    }

    if (j === jaren) break;

    // Regel 118 v3.20.3: pas orde-modulatie toe BOVENOP de baseline-drift.
    // v3.20.2-bug: partij-delta verving baseline i.p.v. bovenop, waardoor lichte
    // partij-modulatie (bv. PP) de historisch dalende trend (E_tv+, α-, τ+, φ-)
    // volledig weggooide en NEPK exponentieel liet stijgen tot 4.87% —
    // dit was econometrisch onmogelijk (±2 jaar historische reeks daalt −0,11 pp/j).
    const orde = ordeVoorJaar(j + 1);
    const dEtv = scoring.E_tv[orde] * lev;
    const dAlpha = scoring.alpha[orde] * lev;
    const dTau = scoring.tau[orde] * lev;
    const dPhi = scoring.phi[orde] * lev;

    // Baseline-drift + partij-ombuiging = werkelijke evolutie
    E_tv += BASELINE_dEtv + dEtv;
    alpha = Math.max(0.05, Math.min(0.95, alpha + BASELINE_dalpha + dAlpha));
    tau = Math.max(0.10, Math.min(0.90, tau + BASELINE_dtau + dTau));
    phi = Math.max(0.05, Math.min(0.95, phi + BASELINE_dphi + dPhi));

    // Baseline zonder ombuiging — puur historische drift voor grijze lijn
    b_Etv += BASELINE_dEtv;
    b_alpha = Math.max(0.05, b_alpha + BASELINE_dalpha);
    b_tau = Math.min(0.90, b_tau + BASELINE_dtau);
    b_phi = Math.max(0.05, b_phi + BASELINE_dphi);

    // BBP-index groeit proportioneel met NEPK-groei relatief tot start
    const nepk_next = E_tv * alpha * (1 - tau) * phi;
    const nepk_ratio = startNEPK > 0 ? nepk_next / startNEPK : 1;
    bbp_idx = 100 * Math.pow(nepk_ratio, 0.3);  // gedempte groei via NEPK

    S += eff_stijging_schuld;
  }

  // Cumulatieve 15j-verschuivingen voor diagnostiek
  function cumulatief(orde: [number, number, number]): number {
    return (orde[0]*3 + orde[1]*5 + orde[2]*7) * lev;
  }

  const drie_orde_scoring = {
    E_tv:  { orde1: scoring.E_tv[0] * lev, orde2: scoring.E_tv[1] * lev,
             orde3: scoring.E_tv[2] * lev, cumulatief_15j: cumulatief(scoring.E_tv) },
    alpha: { orde1: scoring.alpha[0] * lev, orde2: scoring.alpha[1] * lev,
             orde3: scoring.alpha[2] * lev, cumulatief_15j: cumulatief(scoring.alpha) },
    tau:   { orde1: scoring.tau[0] * lev, orde2: scoring.tau[1] * lev,
             orde3: scoring.tau[2] * lev, cumulatief_15j: cumulatief(scoring.tau) },
    phi:   { orde1: scoring.phi[0] * lev, orde2: scoring.phi[1] * lev,
             orde3: scoring.phi[2] * lev, cumulatief_15j: cumulatief(scoring.phi) },
  };

  return {
    jaren: Array.from({ length: jaren + 1 }, (_, j) => j),
    kalender_jaren,
    // v3.12 nieuwe velden
    E_tv_pct, alpha_index, tau_index, phi_index,
    ntpk_pct_bbp,
    nepk_pct_bbp,
    ntpk_startwaarde_pct: startNTPK,
    npk_startwaarde_pct: startNPK,  // v3.20.6
    npk_pct_bbp,                     // v3.20.6
    startwaarde_pct: startNEPK,
    kritische_grens,
    point_of_no_return,
    jaar_onder_grens,
    jaar_point_of_no_return,
    baseline_ntpk_pct,
    baseline_nepk_pct,
    bbp_index,
    drie_orde_scoring,
    // v3.11 behouden voor backwards compat
    fdi_afhankelijkheid_pct_bbp: fdi_pct_bbp,
    fdi_startwaarde_pct: fdi_startwaarde,
    schuld_service_pct_bbp: schuld_pct_bbp,
    schuld_service_startwaarde: schuld_startwaarde,
    schuld_service_uitmergel_drempel: uitmergel_drempel,
    jaar_uitmergel_intreedt,
    netto_gezondheid_pct_bbp: netto_gezondheid,
    netto_gezondheid_jaar_onder_grens: netto_jaar_onder_grens,
    daling_midden: 0,   // niet meer gebruikt in v3.12
    partij_modulatie_nepk_pp: drie_orde_scoring.E_tv.cumulatief_15j / 15,  // gemiddeld effect
    partij_modulatie_fdi_pp: 0,
    partij_modulatie_schuld_pp: mod_schuld_pp,
    partij_naam: partij,
  };
}

export interface LevensloopResultaat {
  jaren: number[];
  advies_index: number[];
  eigen_index: number[];
  herkeuze_index: number[];
  // Regel 105 v3.9: referentiemodellen als aparte lijnen op de grafiek
  vmp_index: number[];
  carb_index: number[];
  // NEPK-lijn (landsniveau): F1+F2+F3 gewogen cascade van de eigen-gekozen partij.
  // Interpretatie: 'als deze partij haar volledige programma uitvoert, hoe beweegt
  // dan de productieve kern van de nationale economie?'. Basis 100 = vandaag.
  nepk_eigen_index: number[];
  // v3.20.20 — NEPK-lijnen voor referentie-modellen VMP en CARB, zichtbaar
  // wanneer hun toggle aan staat.
  nepk_vmp_index: number[];
  nepk_carb_index: number[];
  band_pct: number[];
  band_advies_onder: number[];
  band_advies_boven: number[];
  band_herkeuze_onder: number[];
  band_herkeuze_boven: number[];
  pad: State[];
  herkeuzes: Array<{ jaar: number; van_partij: string; naar_partij: string; nieuwe_fase: Leeftijdsfase; nieuwe_status: EconomischeStatus }>;
  start_partij_advies: string;
  start_partij_eigen: string;
  // Regel 103 v3.9: baseline-drift voor UI-weergave (nullijn)
  baseline_drift?: BaselineDriftResultaat;
}

export function berekenLevensloop(
  antwoorden: Antwoorden,
  advies_partij: string,
  eigen_partij: string,
  sector: string,
  jaren: number = 15,
): LevensloopResultaat {
  const start = startStateUitAntwoorden(antwoorden);
  const pad = modaalPad(start, jaren);
  const startNiv = nivVoor(start);

  // Regel 103 v3.9: landsdrift wordt vooraf berekend zodat we hem
  // combineren met het persoonlijke levenspad. De nullijn van de
  // grafiek volgt daarmee de structurele beweging van NL-koopkracht
  // zonder partij-interventie — niet vlak 100.
  const _bd = berekenBaselineDrift(jaren);

  // Inkomenstraject baseline: persoonlijk pad × landsdrift (regel 103).
  // startNiv = 100 door normalisatie; de landsdrift zet de nullijn structureel dalend.
  const baseline = pad.map((s, j) => (nivVoor(s) / startNiv) * _bd.drift_index[j]);

  // Per partij: cumulatieve groei toepassen op baseline
  // v3.20.10: VMP en CARB zijn gewone partijen met eigen partij_posities
  // (bron: novademocratia.com VMP-programma + openvizier.org Carbon-Alert).
  // Ze lopen dus via dezelfde partijGroeiPerJaar-route als PP/PSOE/VOX etc.
  // De v3.20.9 bypass via bundelNEPKLijn is verwijderd — die routeerde op
  // NEPK % BBP, wat een dalende metric is en dus onjuist voor een
  // inkomens-index.
  function indexMet(partij: string): number[] {
    const groei = partijGroeiPerJaar(antwoorden, partij, jaren);
    const out = new Array(jaren+1).fill(0);
    let cum = 1.0;
    for (let j = 0; j <= jaren; j++) {
      cum *= (1 + groei[j]);
      out[j] = baseline[j] * cum;
    }

    // v3.20.20 — NTPK-koppeling: bestedingsruimte volgt de productieve
    // capaciteit van het regime (ongeacht eigendom). NTPK = E_tv × α × (1-τ).
    // Was v3.20.19 NEPK (= NTPK × φ), maar de eigendom-schil φ hoort niet in
    // bestedingsruimte per capita — alleen in soevereiniteitsvraag. NTPK is
    // de juiste metric: wat wordt er geproduceerd, wat er te besteden is.
    // 1:1 koppeling.
    try {
      const { ntpk } = bundelNEPKLijn(partij, jaren);
      const ntpk_start = ntpk[0] || 1;
      for (let j = 0; j <= jaren; j++) {
        const ntpk_factor = ntpk[j] / ntpk_start;
        out[j] = out[j] * ntpk_factor;
      }
    } catch (e) {
      // Als bundelNEPKLijn faalt, retourneer de ongekoppelde index.
    }

    return out;
  }

  const advies_index = indexMet(advies_partij);
  const eigen_index = indexMet(eigen_partij);

  // NEPK-lijn v3.20.5: gebruikt DEZELFDE motor als de onderste NEPK-grafiek
  // (bundelNEPKLijn = baseline-drift + partij-ombuiging) genormaliseerd naar
  // index=100 op jaar 0. Voorheen (≤ v3.20.4) rekende deze lijn via
  // partijGroeiPerJaar met filter-subset [0,1,2] cumulatief — die kende geen
  // historische baseline-drift en produceerde stijgende lijnen bij elke partij
  // met positieve F1+F2+F3 cascade. Dat was inconsistent met de onderste grafiek.
  function nepkIndexMet(partij: string): number[] {
    const { nepk } = bundelNEPKLijn(partij, jaren);
    const start = nepk[0] || 1;
    return nepk.map(v => (v / start) * 100);
  }
  const nepk_eigen_index = nepkIndexMet(eigen_partij);
  // v3.20.20 — aparte NEPK-lijnen voor VMP en CARB (voor toggle-weergave)
  const nepk_vmp_index = nepkIndexMet('VMP');
  const nepk_carb_index = nepkIndexMet('CARB');

  // Herkozen-traject: bij elke fase-overgang heroverwegen welke partij optimaal is
  const herkeuze_index = new Array(jaren+1).fill(100);
  const herkeuzes: LevensloopResultaat['herkeuzes'] = [];
  let huidige_partij = advies_partij;
  let huidige_groei = partijGroeiPerJaar(antwoorden, huidige_partij, jaren);
  let cum = 1.0;
  herkeuze_index[0] = baseline[0];
  let vorige_state = pad[0];
  for (let j = 1; j <= jaren; j++) {
    const nieuwe_state = pad[j];
    if (nieuwe_state.fase !== vorige_state.fase) {
      // Sprong: heroverweeg partij
      const nieuwe_partij = besteVoor(nieuwe_state, sector);
      if (nieuwe_partij !== huidige_partij) {
        herkeuzes.push({
          jaar: j, van_partij: huidige_partij, naar_partij: nieuwe_partij,
          nieuwe_fase: nieuwe_state.fase, nieuwe_status: nieuwe_state.status,
        });
        huidige_partij = nieuwe_partij;
        // Recompute groei vanaf hier voor nieuwe partij (vanaf jaar j)
        const nieuw_groei = partijGroeiPerJaar(antwoorden, huidige_partij, jaren);
        // Schuif huidige_groei: vóór j blijft het oude, na j komt het nieuwe
        for (let k = j; k <= jaren; k++) {
          huidige_groei[k] = nieuw_groei[k];
        }
      }
    }
    cum *= (1 + huidige_groei[j]);
    herkeuze_index[j] = baseline[j] * cum;
    vorige_state = nieuwe_state;
  }

  // Onzekerheidsband: lineair 0 → 25%
  const band_pct = Array.from({ length: jaren+1 }, (_, j) => (j / jaren) * 0.25);
  const band_advies_onder = advies_index.map((v, j) => v * (1 - band_pct[j]));
  const band_advies_boven = advies_index.map((v, j) => v * (1 + band_pct[j]));
  const band_herkeuze_onder = herkeuze_index.map((v, j) => v * (1 - band_pct[j]));
  const band_herkeuze_boven = herkeuze_index.map((v, j) => v * (1 + band_pct[j]));

  // Regel 103 v3.9: baseline-drift is al berekend voor de baseline hierboven; we hergebruiken die.
  const baseline_drift = _bd;

  // Regel 105 v3.9: bereken VMP- en CARB-lijnen zodat ze via toggle zichtbaar kunnen zijn.
  const vmp_index = indexMet('VMP');
  const carb_index = indexMet('CARB');

  return {
    jaren: Array.from({ length: jaren+1 }, (_, j) => j),
    advies_index, eigen_index, herkeuze_index,
    vmp_index, carb_index,
    nepk_eigen_index,
    nepk_vmp_index,
    nepk_carb_index,
    band_pct,
    band_advies_onder, band_advies_boven,
    band_herkeuze_onder, band_herkeuze_boven,
    pad, herkeuzes,
    start_partij_advies: advies_partij,
    start_partij_eigen: eigen_partij,
    baseline_drift,
  };
}
