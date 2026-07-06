import raw from "@/data/gevolgenkaart.json";

export interface Bijdrage {
  element_id: string;
  naam: string;
  positie: number;
  intensiteit: number;
  cascade: number;
  bijdrage: number;
}

export interface Uitkomst {
  sector_naam: string;
  "1e_orde": number;
  "2e_orde": number;
  "3e_orde": number;
  aantal_actieve_elementen: number;
  top_positief: Bijdrage[];
  top_negatief: Bijdrage[];
}

export interface Sector {
  naam: string;
  kenmerken: Record<string, string>;
  primaire_gevoeligheden: string[];
}

export interface Partij {
  naam: string;
  kleur: string;
  type: string;
  referentie?: boolean;
  opmerking?: string;
}

export interface Filter {
  naam: string;
  volledig: string;
  uitleg: string;
  indicatoren: string[];
}

interface DataShape {
  filters: Record<string, Filter>;
  filters_meta: Record<string, string>;
  sectoren: Record<string, Sector>;
  sector_groepen: Record<string, string[]>;
  partijen: Record<string, Partij>;
  partij_meta: any;
  uitkomst: Record<string, Record<string, Uitkomst>>;
}

const data = raw as unknown as DataShape;

export const filters = data.filters;
export const filtersMeta = data.filters_meta;
export const sectoren = data.sectoren;
export const sectorGroepen = data.sector_groepen;
export const partijen = data.partijen;
export const uitkomst = data.uitkomst;

export function getUitkomst(partijId: string, sectorId: string): Uitkomst | undefined {
  return data.uitkomst[partijId]?.[sectorId];
}

export const sectorIds = Object.keys(sectoren);
export const partijIds = Object.keys(partijen);

// Een ingetogen, krant-achtige kleur per partij (geen felle campagnekleuren).
// Gebruikt enkel als klein accent-stipje, niet als vlak.
export const partijAccent: Record<string, string> = {
  PRO: "#b23b2e",
  D66: "#4a7c4e",
  VVD: "#2f4b6e",
  CDA: "#3f6b4a",
  NSC: "#b0682a",
  BBB: "#9a8420",
  JA21: "#27395a",
  CU: "#3a6088",
  Volt: "#6b4a86",
  SGP: "#a85f28",
  PVV: "#3a6088",
  SP: "#a83128",
  FvD: "#7a3b32",
  PvdD: "#3f7350",
  DENK: "#2f7d78",
  // Referentiemodellen \u2014 ingetogen goud/smaragd accent
  VMP: "#9a7b1f",
  CARB: "#1f6b4e",
};

export const referentieIds = partijIds.filter((id) => partijen[id]?.referentie);
export const echteIds = partijIds.filter((id) => !partijen[id]?.referentie);

export function isReferentie(partijId: string): boolean {
  return Boolean(partijen[partijId]?.referentie);
}

export function partijKorteLabel(p: Partij): string {
  // "type" is bv. "links-progressief" -> "Links\u2011progressief"
  const t = p.type.replace(/-/g, "\u2011");
  return t.charAt(0).toUpperCase() + t.slice(1);
}

export const ordeLabels = {
  "1e_orde": { titel: "1e orde", periode: "Jaar 1\u20112", omschrijving: "Direct effect" },
  "2e_orde": { titel: "2e orde", periode: "Jaar 3", omschrijving: "Gedragsreactie" },
  "3e_orde": { titel: "3e orde", periode: "Jaar 5\u201110", omschrijving: "Cascade" },
} as const;

export type OrdeKey = "1e_orde" | "2e_orde" | "3e_orde";

// ----- Afgeleide bereiken voor heatmap-kleurintensiteit -----

function berekenBereik(): Record<OrdeKey, number> {
  const max: Record<OrdeKey, number> = { "1e_orde": 1, "2e_orde": 1, "3e_orde": 1 };
  const ordes: OrdeKey[] = ["1e_orde", "2e_orde", "3e_orde"];
  for (const pid of partijIds) {
    for (const sid of sectorIds) {
      const u = getUitkomst(pid, sid);
      if (!u) continue;
      for (const o of ordes) {
        const v = Math.abs(u[o]);
        if (v > max[o]) max[o] = v;
      }
    }
  }
  return max;
}

/** Maximale absolute waarde per orde, gebruikt om kleurintensiteit te normaliseren. */
export const ordeMaxAbs = berekenBereik();

/**
 * Geeft een achtergrondkleur (rgba) voor een heatmap-cel: groen voor positief,
 * rood voor negatief, met intensiteit evenredig aan de relatieve grootte.
 */
export function heatmapKleur(waarde: number, orde: OrdeKey): string {
  const max = ordeMaxAbs[orde];
  const ratio = Math.min(1, Math.abs(waarde) / max);
  // Een zachte, niet-lineaire curve zodat kleine waarden toch zichtbaar zijn.
  const a = 0.08 + Math.pow(ratio, 0.7) * 0.62;
  if (waarde >= 0) {
    // smaragdgroen 152 42% 28% -> rgb(41 102 71)
    return `rgba(41, 102, 71, ${a.toFixed(3)})`;
  }
  // baksteenrood 4 62% 44% -> rgb(182 55 44)
  return `rgba(182, 55, 44, ${a.toFixed(3)})`;
}

/** Geeft een tekstkleur (donker of licht) afhankelijk van de celintensiteit. */
export function heatmapTekstKleur(waarde: number, orde: OrdeKey): string {
  const max = ordeMaxAbs[orde];
  const ratio = Math.min(1, Math.abs(waarde) / max);
  const a = 0.08 + Math.pow(ratio, 0.7) * 0.62;
  return a > 0.42 ? "#ffffff" : "#2b2723";
}

export function fmtGetal(n: number): string {
  const r = Math.round(n);
  return (r > 0 ? "+" : "") + r.toLocaleString("nl-NL");
}

export interface RangRegel {
  partijId: string;
  partij: Partij;
  een: number;
  twee: number;
  drie: number;
}

/** Ranglijst van alle partijen voor één sector, oplopend gesorteerd op de gekozen orde (hoog->laag). */
export function ranglijstVoorSector(sectorId: string, sorteerOp: OrdeKey): RangRegel[] {
  const regels: RangRegel[] = partijIds
    .map((pid) => {
      const u = getUitkomst(pid, sectorId);
      if (!u) return null;
      return {
        partijId: pid,
        partij: partijen[pid],
        een: u["1e_orde"],
        twee: u["2e_orde"],
        drie: u["3e_orde"],
      } as RangRegel;
    })
    .filter((r): r is RangRegel => r !== null);

  const sleutel = sorteerOp === "1e_orde" ? "een" : sorteerOp === "2e_orde" ? "twee" : "drie";
  regels.sort((a, b) => b[sleutel] - a[sleutel]);
  return regels;
}

export interface GewogenRegel {
  partijId: string;
  partij: Partij;
  gewogen: number;
}

/**
 * Persoonlijke gewogen ranglijst: voor elke partij het gewogen gemiddelde van de
 * 3e orde over de geselecteerde sectoren. Gewichten worden genormaliseerd naar som 1.
 *   weighted_3e[partij] = sum(weight[s] * uitkomst[partij][s].3e_orde)
 */
export function gewogenRanglijst(weights: Record<string, number>): GewogenRegel[] {
  const sectorenSel = Object.keys(weights).filter((s) => weights[s] > 0);
  const totaal = sectorenSel.reduce((acc, s) => acc + weights[s], 0);
  if (totaal <= 0 || sectorenSel.length === 0) return [];

  const genormaliseerd: Record<string, number> = {};
  for (const s of sectorenSel) genormaliseerd[s] = weights[s] / totaal;

  const regels: GewogenRegel[] = partijIds
    .map((pid) => {
      let som = 0;
      let geldig = false;
      for (const s of sectorenSel) {
        const u = getUitkomst(pid, s);
        if (!u) continue;
        geldig = true;
        som += genormaliseerd[s] * u["3e_orde"];
      }
      if (!geldig) return null;
      return { partijId: pid, partij: partijen[pid], gewogen: som } as GewogenRegel;
    })
    .filter((r): r is GewogenRegel => r !== null);

  regels.sort((a, b) => b.gewogen - a.gewogen);
  return regels;
}

/** Plat lijstje van sectoren met groep-label, in volgorde S1..S22. */
export interface SectorOptie {
  id: string;
  naam: string;
  groep: string;
}

export function sectorOpties(): SectorOptie[] {
  const groepVan: Record<string, string> = {};
  for (const [groep, ids] of Object.entries(sectorGroepen)) {
    for (const id of ids) groepVan[id] = groep;
  }
  return sectorIds.map((id) => ({ id, naam: sectoren[id].naam, groep: groepVan[id] ?? "" }));
}
