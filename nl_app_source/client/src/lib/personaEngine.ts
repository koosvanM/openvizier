// Persona-rekenmotor in TypeScript
// Basis 9 + overlays (sector + persona) binnen relatieve-fout-marge
// CASCADE PER FILTER (echte 2e/3e orde):
//   1e orde = vector v1[9]: per filter de gewogen som van element-bijdragen op die filter
//   2e orde = vector v2[9] = M · v1 (×demping_2e)  -- per filter: gevolgen op dezelfde 9 filters
//   3e orde = vector v3[9] = M · v2 (×demping_3e)  -- per filter: gevolgen van gevolgen
// Eindscore per orde = som van de vector, met teken van de polarisatie

import personaData from '../data/gevolgenkaart-persona.json';

export type Antwoorden = Record<string, string | string[]>;

const FILTER_NAMEN = ['F1 NEPK', 'F2 Bedrijvigheid', 'F3 Investeringsklimaat', 'F4 Talentmobiliteit', 'F5 Begroting', 'F6 Energie', 'F7 Demografie', 'F8 Institutie', 'F9 Wereldhandel'];

export function getFilterNaam(idx: number): string {
  return FILTER_NAMEN[idx] || `F${idx + 1}`;
}

export function getFilterKort(idx: number): string {
  const k = ['NEPK', 'Bedrijvigheid', 'Investering', 'Talent', 'Begroting', 'Energie', 'Demografie', 'Institutie', 'Wereldhandel'];
  return k[idx] || `F${idx + 1}`;
}

export interface OverlayBijdrage {
  laag: string;
  waarde: string;
  filter_index: number;
  delta: number;
  reden: string;
  vraag_id: string;
  vraag_label: string;
  antwoord_label: string;
}

export interface Bijdrage {
  element_id: string;
  naam: string;
  domein: string;
  positie: number;
  intensiteit_norm: number;
  basis_scores: number[];
  persoonlijk_scores: number[];
  filter_bijdragen: number[];  // bijdrage van dit element per filter (1e orde)
  bijdrage: number;             // som van filter_bijdragen
  overlay_bijdragen: OverlayBijdrage[];
}

export interface PartijResultaat {
  partij_id: string;
  // Vectoren per filter
  v1: number[];  // 1e orde per filter
  v2: number[];  // 2e orde per filter
  v3: number[];  // 3e orde per filter
  // Geaggregeerd
  eerste_orde: number;
  tweede_orde: number;
  derde_orde: number;
  aantal_actieve_elementen: number;
  top_positief: Bijdrage[];
  top_negatief: Bijdrage[];
  leverbaarheid?: number;
  leverbaarheid_label?: string;
  alle_bijdragen: Bijdrage[];
}

const clamp = (x: number, lo = 0, hi = 10) => Math.max(lo, Math.min(hi, x));

const data = personaData as any;

const M: number[][] = data.filter_interactie?.matrix || Array.from({length:9}, () => Array(9).fill(0));
const DEMPING_2E: number = data.filter_interactie?.demping_2e ?? 0.60;
const DEMPING_3E: number = data.filter_interactie?.demping_3e ?? 0.30;
// Overshoot-drempel
const OVERSHOOT_DREMPEL: number = data.filter_interactie?.overshoot_drempel ?? 25;
// ASYMMETRISCHE OVERSHOOT-FACTOREN per filter
// Sparen-eerst wint: uitgeven (positieve F5 overschrijding) krijgt zwaardere terugkoppeling dan bezuinigen.
// Geforceerde talentmobiliteit (positieve F4) is destructiever dan restrictief talentbeleid.
const OF_POS: number[] = [-0.35, -0.30, -0.25, -0.85, -0.95, -0.30, -0.35, -0.25, -0.30];
const OF_NEG: number[] = [-0.75, -0.75, -0.85, -0.20, -0.45, -0.80, -0.80, -0.85, -0.75];

function matvec(M: number[][], v: number[]): number[] {
  const out = new Array(9).fill(0);
  for (let i = 0; i < 9; i++) {
    let s = 0;
    for (let j = 0; j < 9; j++) {
      s += M[j][i] * v[j];  // M[j][i] = invloed van filter j op filter i
    }
    out[i] = s;
  }
  return out;
}

// Overshoot-correctie — ASYMMETRISCH: sparen-eerst is gezond, uitgeven-eerst kantelt sterker.
// Per filter een eigen factor voor positieve vs negatieve overshoot:
//   F5 sterk omhoog (uitgeven/herverdelen, +) → kapitaalvlucht, brain drain. ZEER NEGATIEF.
//   F5 sterk omlaag (bezuinigen, −) → sociale onrust, maar economisch milder dan kapitaalvlucht.
//   F4 sterk omhoog (geforceerde mobiliteit zoals BEE) → brain drain. ZEER NEGATIEF.
//   F4 sterk omlaag (restrictief talentbeleid) → milde stagnatie.
//   F3 sterk omlaag (investeringsklimaat verzwakt) → zware schade. F3 omhoog = beloning.
function overshootCorrectie(v: number[]): number[] {
  const schade = v.map((x, i) => {
    const ex = Math.abs(x) - OVERSHOOT_DREMPEL;
    if (ex <= 0) return 0;
    const factor = x > 0 ? OF_POS[i] : OF_NEG[i];
    // Schade is ALTIJD negatief, gegroepeerd in dezelfde richting als origineel teken
    return Math.sign(x) * ex * Math.abs(factor) * (1 + ex / 100) * -1;
  });
  // 55% lokaal, 45% verspreidt via |M|
  const direct = schade.map((x) => x * 0.55);
  const absM = M.map((row) => row.map((c) => Math.abs(c)));
  const verspreid = matvec(absM, schade).map((x) => x * 0.45);
  return direct.map((d, i) => d + verspreid[i]);
}

const vraagNaarOverlay: Record<string, (v: string) => [string, string]> = {
  Q1_sector: (v) => ['sector', v.split('_')[0]],
  Q2_wonen: (v) => ['vermogen_huis', v],
  Q3_gezin: (v) => ['gezin', v],
  Q4_leeftijd: (v) => ['leeftijd', v],
  Q5_regio: (v) => ['regio', v],
  Q6_bedrijfslaag: (v) => ['bedrijfslaag', v],
  Q7_netwerk: (v) => ['netwerk_infrastructuur', v],
};

export function getVraagLabel(vraagId: string): string {
  return data.vragen[vraagId]?.vraag || vraagId;
}

export function getAntwoordLabel(vraagId: string, antwoordKey: string): string {
  return data.vragen[vraagId]?.antwoorden?.[antwoordKey]?.label || antwoordKey;
}

function getOverlay(kind: string, key: string): Record<string, Record<string, any>> {
  if (kind === 'sector') {
    if (data.sector_overlays[key]) return data.sector_overlays[key];
    const base = key.split('_')[0];
    return data.sector_overlays[base] || {};
  }
  return data.persona_overlays[kind]?.[key] || {};
}

type OverlayAanwijzing = [string, string, number, string, string];

function antwoordenNaarOverlays(antwoorden: Antwoorden): OverlayAanwijzing[] {
  const overlays: OverlayAanwijzing[] = [];
  for (const [vraagId, antwoord] of Object.entries(antwoorden)) {
    const mapping = vraagNaarOverlay[vraagId];
    if (!mapping || !antwoord) continue;
    if (typeof antwoord === 'string') {
      const [kind, key] = mapping(antwoord);
      overlays.push([kind, key, 1.0, vraagId, antwoord]);
    } else if (Array.isArray(antwoord)) {
      for (const a of antwoord) {
        const [kind, key] = mapping(a);
        overlays.push([kind, key, 1.0, vraagId, a]);
      }
    }
  }
  return overlays;
}

interface PersoonlijkResult {
  scores: number[];
  overlay_bijdragen: OverlayBijdrage[];
}

function berekenPersoonlijkeBasis(antwoorden: Antwoorden): Record<string, PersoonlijkResult> {
  const overlays = antwoordenNaarOverlays(antwoorden);
  const persoonlijk: Record<string, PersoonlijkResult> = {};

  for (const el of data.elementen) {
    const elId = el.id;
    const basis = [...el.basis];
    const maxCorr = el.mc as number;

    const ruweDeltas = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    const overlayBijdragen: OverlayBijdrage[] = [];

    for (const [kind, key, gew, vraagId, antwKey] of overlays) {
      const overlay = getOverlay(kind, key);
      const elCorr = overlay[elId];
      if (!elCorr) continue;
      const reden = (elCorr as any).reden || '';
      for (const [fkey, delta] of Object.entries(elCorr)) {
        if (fkey === 'reden') continue;
        if (!fkey.startsWith('F')) continue;
        const fi = parseInt(fkey.slice(1)) - 1;
        if (fi >= 0 && fi < 9) {
          const d = (delta as number) * gew;
          ruweDeltas[fi] += d;
          overlayBijdragen.push({
            laag: kind,
            waarde: key,
            filter_index: fi,
            delta: d,
            reden,
            vraag_id: vraagId,
            vraag_label: getVraagLabel(vraagId),
            antwoord_label: getAntwoordLabel(vraagId, antwKey),
          });
        }
      }
    }

    const scores: number[] = [];
    for (let i = 0; i < 9; i++) {
      let delta = ruweDeltas[i];
      if (delta > maxCorr) delta = maxCorr;
      else if (delta < -maxCorr) delta = -maxCorr;
      scores.push(Math.round(clamp(basis[i] + delta)));
    }
    persoonlijk[elId] = { scores, overlay_bijdragen: overlayBijdragen };
  }
  return persoonlijk;
}

export function berekenPartij(partij: string, antwoorden: Antwoorden): PartijResultaat {
  const persoonlijkeBasis = berekenPersoonlijkeBasis(antwoorden);

  const bijdragen: Bijdrage[] = [];
  const v1 = new Array(9).fill(0);

  // Regel 108 v3.9 — COALITIE-VULLING
  // Een partij regeert nooit alleen. Voor elementen waarop partij P geen
  // actief standpunt heeft (positie=0 of intensiteit=0), gebruiken we het
  // leverbaarheid-gewogen gemiddelde van de andere kiesbare partijen op
  // datzelfde element. Referentiemodellen (VMP/CARB) worden uitgesloten.
  //
  // v3.20.10.2 — CARB-uitzondering: CARB is een smalle klimaat/energie-partij
  // die op economische/bestuurlijke elementen doorgaans de VMP-lijn volgt
  // (subsidie-afschaffing, kleine overheid, marktwerking). Voor CARB gebruiken
  // we daarom VMP's posities als vullers voor CARB's zwijg-elementen, ipv het
  // reguliere-partij-gemiddelde. Effect: CARB's eindindex komt dichter bij VMP.
  const partijenObj: any = (data.partijen as any) || {};
  const alleKiesbaar = Object.keys(data.partij_posities).filter((pid) => {
    const meta = partijenObj[pid];
    return meta && meta.referentie !== true;
  });
  // v3.20.15 — CARB behandeld als normale partij, geen speciale VMP-only
  // coalitie-route meer. Alle partijen (incl. VMP en CARB) gebruiken de
  // gewone coalitie-vulling: alle andere kiesbare partijen.
  const coalitieVullers = alleKiesbaar.filter((pid) => pid !== partij);
  const coalitieProduct: Record<string, number> = {};
  for (const el of data.elementen) {
    let som = 0;
    let gewicht = 0;
    for (const pid of coalitieVullers) {
      const pd2 = data.partij_posities[pid]?.[el.id];
      if (!pd2) continue;
      const p = (pd2.positie == null) ? 0 : pd2.positie;
      const i = (pd2.intensiteit == null) ? 0 : pd2.intensiteit;
      if (p === 0 || i === 0) continue;
      const iNorm = i > 1.0 ? i / 10.0 : i;
      const w = typeof partijenObj[pid]?.leverbaarheid === 'number'
        ? partijenObj[pid].leverbaarheid
        : 0.50;
      som += w * (p / 2.0) * iNorm;
      gewicht += w;
    }
    coalitieProduct[el.id] = gewicht > 0 ? (som / gewicht) : 0;
  }

  for (const el of data.elementen) {
    const elId = el.id;
    const pd = data.partij_posities[partij]?.[elId];
    if (!pd) continue;
    const positie = pd.positie || 0;
    const intens = pd.intensiteit || 0;

    let posIntProduct: number;
    let uitCoalitie = false;
    if (positie === 0 || intens === 0) {
      posIntProduct = coalitieProduct[elId];
      if (posIntProduct === 0) continue;
      uitCoalitie = true;
    } else {
      const intensNorm = intens > 1.0 ? intens / 10.0 : intens;
      posIntProduct = (positie / 2.0) * intensNorm;
    }

    const pres = persoonlijkeBasis[elId];
    const scores = pres.scores;
    const filterBijdragen = scores.map((s) => (s - 5) * posIntProduct);
    const totaal = filterBijdragen.reduce((a, b) => a + b, 0);

    // Akkumuleer per filter
    for (let i = 0; i < 9; i++) v1[i] += filterBijdragen[i];

    bijdragen.push({
      element_id: elId,
      naam: el.naam,
      domein: el.domein,
      positie: uitCoalitie ? 0 : positie,
      intensiteit_norm: uitCoalitie ? posIntProduct : ((intens > 1 ? intens / 10 : intens)),
      basis_scores: el.basis,
      persoonlijk_scores: scores,
      filter_bijdragen: filterBijdragen.map((x) => Math.round(x * 100) / 100),
      bijdrage: Math.round(totaal * 100) / 100,
      overlay_bijdragen: pres.overlay_bijdragen,
      uit_coalitie: uitCoalitie,
    } as any);
  }

  // Leverbaarheids-factor: hoeveel van het programma zet de partij echt om in beleid?
  // Wordt alleen op de 1e orde toegepast. De cascade naar 2e/3e orde werkt vervolgens
  // autonoom op de afgewaardeerde 1e orde — gevolgen volgen automatisch.
  const partijMeta = (data.partijen as any)[partij];
  const leverbaarheid = typeof partijMeta?.leverbaarheid === 'number' ? partijMeta.leverbaarheid : 0.50;
  for (let i = 0; i < 9; i++) v1[i] *= leverbaarheid;

  // 2e orde = matrix-cascade van v1 + overshoot van v1 (omkering al hier voelbaar)
  const v2_raw = matvec(M, v1);
  const v2_overshoot = overshootCorrectie(v1);
  const v2 = v2_raw.map((x, i) => x * DEMPING_2E + v2_overshoot[i]);

  // 3e orde = matrix-cascade van v2 + overshoot van v2 + EXTRA cumulatieve overshoot van v1
  // (effecten als kapitaalvlucht/brain drain bouwen op door de tijd — het wordt erger)
  const v3_raw = matvec(M, v2);
  const v3_overshoot = overshootCorrectie(v2);
  const v3_cumulatief = overshootCorrectie(v1).map((x) => x * 0.5);  // helft vóórt door
  const v3 = v3_raw.map((x, i) => x * DEMPING_3E + v3_overshoot[i] + v3_cumulatief[i]);

  const sum = (v: number[]) => v.reduce((a, b) => a + b, 0);

  return {
    partij_id: partij,
    v1: v1.map((x) => Math.round(x * 100) / 100),
    v2: v2.map((x) => Math.round(x * 100) / 100),
    v3: v3.map((x) => Math.round(x * 100) / 100),
    eerste_orde: Math.round(sum(v1) * 100) / 100,
    tweede_orde: Math.round(sum(v2) * 100) / 100,
    derde_orde: Math.round(sum(v3) * 100) / 100,
    aantal_actieve_elementen: bijdragen.length,
    top_positief: [...bijdragen].sort((a, b) => b.bijdrage - a.bijdrage).slice(0, 10),
    top_negatief: [...bijdragen].sort((a, b) => a.bijdrage - b.bijdrage).slice(0, 10),
    alle_bijdragen: bijdragen,
    leverbaarheid: leverbaarheid,
    leverbaarheid_label: partijMeta?.leverbaarheid_label || 'beperkt uitvoerend',
  };
}

export function berekenRanglijst(
  antwoorden: Antwoorden,
  orde: '1e' | '2e' | '3e' | 'totaal' = 'totaal'
): PartijResultaat[] {
  const partijen = Object.keys(data.partij_posities);
  const resultaten = partijen.map((p) => berekenPartij(p, antwoorden));
  const sleutel = (r: PartijResultaat) => {
    if (orde === '1e') return r.eerste_orde;
    if (orde === '2e') return r.tweede_orde;
    if (orde === '3e') return r.derde_orde;
    return r.eerste_orde + r.tweede_orde + r.derde_orde;
  };
  return resultaten.sort((a, b) => sleutel(b) - sleutel(a));
}

export function getVragen() {
  return data.vragen;
}

export function getPartijMeta() {
  return data.partijen;
}

export function getSectorMeta() {
  return data.sectoren;
}

export function getFilters() {
  return data.filters;
}

export function getElementen() {
  return data.elementen;
}

export function getFilterInteractieReden(): Record<string, string> {
  return data.filter_interactie?.reden || {};
}

// ============================================================================
// DUIDING-NARRATIEF — wat dreigt of belooft de 2e en 3e orde voor jou?
// ============================================================================

export interface DuidingItem {
  filter_index: number;
  filter_naam: string;
  v1: number;
  v2: number;
  v3: number;
  trend: 'kantelt_negatief' | 'verergert_negatief' | 'verbetert_op_termijn' | 'versterkt_positief' | 'stabiel_positief' | 'stabiel_negatief';
  zin: string;
}

export interface DuidingNarratief {
  samenvatting: string;
  oordeel: 'sterk_positief' | 'matig_positief' | 'gemengd' | 'matig_negatief' | 'sterk_negatief' | 'kantelt';
  beloften: DuidingItem[];
  dreigingen: DuidingItem[];
}

// Per filter de korte uitleg in mensentaal, met sector-context
function beschrijvingPerFilter(filterIdx: number, sectorBase: string): { veld: string; pos: string; neg: string; sectorPos?: string; sectorNeg?: string } {
  const f: Record<number, any> = {
    0: { veld: 'kapitaalbalans', pos: 'Spanje houdt netto kapitaal in eigen land — sterker pensioen, beter beschikbare hypotheek, koopkracht onder controle.', neg: 'Kapitaalvlucht: bedrijven en spaargeld verlaten Spanje — pensioenfondsen zwakken af, hypotheekrente loopt op, koopkracht onder druk.' },
    1: { veld: 'bedrijvigheid en banen', pos: 'De economie groeit, banen ontstaan, ondernemers durven te investeren.', neg: 'Banen verdwijnen of staan onder druk, lonen blijven achter, werkloosheid loert.',
         _S22_pos: 'Voor jou als student: je vindt straks gemakkelijker een (start-)baan.', _S22_neg: 'Voor jou als student: na je studie wordt het lastig een baan op niveau te vinden.',
         _S5_pos: 'Industrie groeit, meer werk in jouw sector.', _S5_neg: 'In de industrie kunnen bedrijven sluiten of verhuizen.',
         _S8_pos: 'Stevige binnenlandse vraag voor agrarische producten.', _S8_neg: 'Boerenbedrijven raken in de knel door wegvallende vraag.' },
    2: { veld: 'investeringsklimaat', pos: 'Bedrijven en mensen durven te investeren — nieuwe winkels, projecten, woningbouw, infrastructuur.', neg: 'Investeerders haken af, projecten worden afgeblazen, vernieuwing stokt.' },
    3: { veld: 'talentmobiliteit', pos: 'Talent komt en blijft — betere collega\'s, sterker onderwijs, levendige steden.', neg: 'Brain drain: opgeleide mensen vertrekken naar het buitenland, kennis verdwijnt.',
         _S22_pos: 'Je medestudenten blijven hier werken — breder netwerk, betere baankansen.', _S22_neg: 'Veel medestudenten vertrekken na hun diploma — minder kansen op het hoogwaardige werk waarvoor je studeert.',
         _S2_neg: 'Onderwijspersoneel vertrekt, klassen lopen vol, kwaliteit zakt.',
         _S11_neg: 'IT-talent vertrekt, projecten lopen vast, salarisinflatie door schaarste.' },
    4: { veld: 'overheidsbegroting', pos: 'De overheid houdt ruimte voor zorg, onderwijs en infrastructuur zonder schuld op te bouwen.', neg: 'Staatsschuld loopt op of voorzieningen worden uitgekleed — minder geld voor zorg, onderwijs, wegen.',
         _S22_neg: 'Studiefinanciering, OV-kaart en publiek onderwijs komen onder druk.', _S22_pos: 'Voorzieningen voor studenten blijven overeind of worden uitgebreid.',
         _S1_neg: 'In de zorg bezuinigingen: minder collega\'s, hogere werkdruk, minder middelen.', _S1_pos: 'Ruimte voor extra zorgcapaciteit en hogere salarissen.',
         _S20_neg: 'AOW en pensioenen onder druk, koopkracht voor gepensioneerden daalt.', _S20_pos: 'AOW en aanvullende voorzieningen blijven op niveau.' },
    5: { veld: 'energie-autonomie', pos: 'Energie wordt betrouwbaarder en betaalbaarder — minder afhankelijkheid van het buitenland.', neg: 'Energiekosten lopen op, leveringszekerheid verslechtert — industrie kan in problemen komen, gezinnen in koude huizen.',
         _S5_neg: 'Energie-intensieve industrie ontvlucht Spanje of staakt productie.', _S5_pos: 'Goedkopere en stabielere energie maakt jouw industrie concurrerend.' },
    6: { veld: 'demografie', pos: 'De demografische opbouw blijft houdbaar — voldoende werkenden om voorzieningen te dragen.', neg: 'Vergrijzing slaat door, te weinig werkenden dragen de last — pensioenleeftijd omhoog, premies omhoog.',
         _S22_neg: 'Jouw generatie betaalt straks zwaarder voor een vergrijsd land.', _S22_pos: 'Voor jouw generatie is er straks ruimte op de arbeidsmarkt.',
         _S20_neg: 'Pensioenfondsen krijgen het zwaar, indexering vervalt.', _S20_pos: 'Het stelsel blijft gepensioneerden ondersteunen.' },
    7: { veld: 'institutionele kwaliteit', pos: 'Vertrouwen in overheid, rechtspraak en bestuur blijft op peil — het cement van een welvarende samenleving.', neg: 'Instituties verzwakken: minder vertrouwen, meer corruptie, willekeur — ondernemers en burgers worden voorzichtiger.' },
    8: { veld: 'wereldhandel', pos: 'Spanje blijft een open handelsland — exportbedrijven groeien, prijzen blijven concurrerend.', neg: 'Internationaal isolement — export onder druk, importprijzen omhoog, supermarktprijzen duurder.',
         _S7_neg: 'Logistiek krimpt door minder handel via Rotterdam/Schiphol.', _S7_pos: 'Logistiek groeit door bloeiende handel.',
         _S5_neg: 'Exporterende industrie verliest markten.', _S5_pos: 'Exportkansen vermenigvuldigen.' },
  };
  const base = f[filterIdx] || { veld: '?', pos: '', neg: '' };
  return {
    veld: base.veld,
    pos: base.pos,
    neg: base.neg,
    sectorPos: base[`_${sectorBase}_pos`],
    sectorNeg: base[`_${sectorBase}_neg`],
  };
}

function bepaalTrendEnZin(filterIdx: number, v1: number, v2: number, v3: number, sectorBase: string): { trend: DuidingItem['trend']; zin: string } | null {
  const absTot = Math.abs(v1) + Math.abs(v2) + Math.abs(v3);
  if (absTot < 10) return null;

  const b = beschrijvingPerFilter(filterIdx, sectorBase);
  const som23 = v2 + v3;

  // Kantelt: v1 duidelijk positief maar v2+v3 sterk negatief
  if (v1 > 8 && som23 < -v1 * 0.4) {
    const sectorTekst = b.sectorNeg ? ` ${b.sectorNeg}` : '';
    return { trend: 'kantelt_negatief', zin: `Korte-termijnwinst op ${b.veld}, maar in 2e en 3e orde kantelt het: ${b.neg.toLowerCase()}${sectorTekst}` };
  }
  // Herstelt: v1 negatief maar v2+v3 positief
  if (v1 < -8 && som23 > Math.abs(v1) * 0.4) {
    const sectorTekst = b.sectorPos ? ` ${b.sectorPos}` : '';
    return { trend: 'verbetert_op_termijn', zin: `Eerst pijn op ${b.veld}, daarna herstel: ${b.pos.toLowerCase()}${sectorTekst}` };
  }
  // Verergert: alle drie negatief
  if (v1 < -3 && v2 < -3 && v3 < -3) {
    const sectorTekst = b.sectorNeg ? ` ${b.sectorNeg}` : '';
    return { trend: 'verergert_negatief', zin: `${b.neg} Het effect stapelt op door de jaren.${sectorTekst}` };
  }
  // Versterkt: alle drie positief
  if (v1 > 3 && v2 > 3 && v3 > 3) {
    const sectorTekst = b.sectorPos ? ` ${b.sectorPos}` : '';
    return { trend: 'versterkt_positief', zin: `${b.pos} En het effect houdt aan of versterkt door de jaren.${sectorTekst}` };
  }
  // Saldo bepaalt het label
  if (v1 + som23 < -10) {
    const sectorTekst = b.sectorNeg ? ` ${b.sectorNeg}` : '';
    return { trend: 'stabiel_negatief', zin: `${b.neg}${sectorTekst}` };
  }
  if (v1 + som23 > 10) {
    const sectorTekst = b.sectorPos ? ` ${b.sectorPos}` : '';
    return { trend: 'stabiel_positief', zin: `${b.pos}${sectorTekst}` };
  }
  return null;
}

export function maakDuidingNarratief(resultaat: PartijResultaat, antwoorden: Antwoorden, partijNaam: string): DuidingNarratief {
  const sectorKeuze = (antwoorden['Q1_sector'] as string) || '';
  const sectorBase = sectorKeuze.split('_')[0];
  const items: DuidingItem[] = [];

  for (let i = 0; i < 9; i++) {
    const v1 = resultaat.v1[i];
    const v2 = resultaat.v2[i];
    const v3 = resultaat.v3[i];
    const res = bepaalTrendEnZin(i, v1, v2, v3, sectorBase);
    if (!res) continue;
    items.push({
      filter_index: i,
      filter_naam: getFilterNaam(i),
      v1: Math.round(v1),
      v2: Math.round(v2),
      v3: Math.round(v3),
      trend: res.trend,
      zin: res.zin,
    });
  }

  const posTrends: DuidingItem['trend'][] = ['versterkt_positief', 'verbetert_op_termijn', 'stabiel_positief'];
  const negTrends: DuidingItem['trend'][] = ['verergert_negatief', 'kantelt_negatief', 'stabiel_negatief'];

  const beloften = items
    .filter((it) => posTrends.includes(it.trend))
    .sort((a, b) => (b.v1 + b.v2 + b.v3) - (a.v1 + a.v2 + a.v3))
    .slice(0, 4);
  const dreigingen = items
    .filter((it) => negTrends.includes(it.trend))
    .sort((a, b) => (a.v1 + a.v2 + a.v3) - (b.v1 + b.v2 + b.v3))
    .slice(0, 4);

  const totaal = resultaat.eerste_orde + resultaat.tweede_orde + resultaat.derde_orde;
  const kantelGevallen = items.filter((it) => it.trend === 'kantelt_negatief').length;

  let oordeel: DuidingNarratief['oordeel'];
  let samenvatting: string;

  if (kantelGevallen >= 2) {
    oordeel = 'kantelt';
    samenvatting = `${partijNaam} levert je op korte termijn iets op, maar via ${kantelGevallen} kanalen kantelt dat in 2e en 3e orde om in schade. Het lijkt aantrekkelijk — pas op.`;
  } else if (totaal > 150) {
    oordeel = 'sterk_positief';
    samenvatting = `${partijNaam} werkt voor jou positief uit op korte én langere termijn. Meerdere domeinen versterken elkaar.`;
  } else if (totaal > 50) {
    oordeel = 'matig_positief';
    samenvatting = `${partijNaam} levert je in totaal winst op. Niet overal even sterk, maar het saldo is gunstig.`;
  } else if (totaal < -150) {
    oordeel = 'sterk_negatief';
    samenvatting = `${partijNaam} werkt voor jou negatief uit. De korte-termijneffecten lijken hanteerbaar, maar in 2e en 3e orde stapelt de schade zich op.`;
  } else if (totaal < -50) {
    oordeel = 'matig_negatief';
    samenvatting = `${partijNaam} kost je per saldo. Geen ramp, maar meer minnen dan plussen.`;
  } else {
    oordeel = 'gemengd';
    samenvatting = `${partijNaam} heeft voor jou een gemengd effect: sommige domeinen winnen, andere verliezen, het saldo blijft beperkt.`;
  }

  return { samenvatting, oordeel, beloften, dreigingen };
}
