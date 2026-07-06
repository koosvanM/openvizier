import { useState, useMemo } from 'react';
import {
  berekenRanglijst,
  getVragen,
  getPartijMeta,
  getFilterNaam,
  getFilterKort,
  getFilterInteractieReden,
  maakDuidingNarratief,
  type Antwoorden,
  type PartijResultaat,
  type Bijdrage,
  type DuidingItem,
} from '../lib/personaEngine';
import { SECTOR_ICONS, getClusterStyle, CLUSTER_STYLES } from '../components/SectorIcons';
import { MiniHero, accentVoorVraag, iconVoorAntwoord, iconVoorVraag } from '../components/MiniHero';
import { LevensloopGrafiek } from '../components/LevensloopGrafiek';
import { GezondheidsgrafiekNL } from '../components/GezondheidsgrafiekNL';
import { HistorischeTrend } from '../components/HistorischeTrend';
import { berekenLevensloop, berekenNEPK } from '../lib/levensloopEngine';
// v3.20.15 — VMP en CARB zijn normale partijen (bron: novademocratia.com
// en openvizier.org/carbon-alert.earth). Geen speciale referentie-check meer.
const isReferentie = (_partijId: string): boolean => false;

// ============================================================================
// KLEUR-HULPMIDDELEN
// ============================================================================
const KLEUR_NAAM_HEX: Record<string, string> = {
  rood: '#ef4444', donkerrood: '#b91c1c',
  groen: '#22c55e', smaragd: '#10b981', donkergroen: '#16a34a',
  blauw: '#3b82f6', donkerblauw: '#1d4ed8', turkoois: '#14b8a6',
  oranje: '#f97316', geel: '#eab308', goud: '#d97706',
  paars: '#a855f7', kastanje: '#c2410c',
  zwart: '#171717', grijs: '#525252',
};
function naarHex(kleur: string): string {
  if (!kleur) return '#a78bfa';
  if (kleur.startsWith('#')) return kleur;
  return KLEUR_NAAM_HEX[kleur.toLowerCase()] || '#a78bfa';
}
function tintKleur(kleur: string, pct: number): string {
  const hex = naarHex(kleur);
  const h = hex.replace('#', '');
  if (h.length !== 6) return hex;
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  const mix = (c: number) => Math.round(c + (255 - c) * pct);
  const toHex = (n: number) => Math.max(0, Math.min(255, n)).toString(16).padStart(2, '0');
  return `#${toHex(mix(r))}${toHex(mix(g))}${toHex(mix(b))}`;
}

// ============================================================================
// TYPES + CONSTANTS
// ============================================================================
interface VraagOptie { label: string; }
interface VraagData {
  vraag: string; trap: number; verplicht: boolean; multi_select?: boolean;
  conditioneel_op_Q1?: string[]; antwoorden: Record<string, VraagOptie>;
}

const VRAGEN_VOLGORDE = ['Q1_sector', 'Q2_wonen', 'Q3_gezin', 'Q4_leeftijd', 'Q5_regio'] as const;
type VraagId = typeof VRAGEN_VOLGORDE[number] | 'Q6_bedrijfslaag' | 'Q7_netwerk';

const VRAAG_LABELS: Record<string, string> = {
  Q1_sector: 'Sector', Q2_wonen: 'Wonen', Q3_gezin: 'Gezin',
  Q4_leeftijd: 'Leeftijd', Q5_regio: 'Regio',
  Q6_bedrijfslaag: 'Bedrijfslaag', Q7_netwerk: 'Netwerk',
};

// Accent-kleuren per vraag (pill-kleur in profielbalk)
const VRAAG_ACCENT: Record<string, { bg: string; tekst: string; rand: string; icon: string }> = {
  Q1_sector: { bg: 'bg-sky-500/10', tekst: 'text-sky-700', rand: 'border-sky-400/40', icon: '🎯' },
  Q2_wonen: { bg: 'bg-amber-500/10', tekst: 'text-amber-700', rand: 'border-amber-400/40', icon: '🏠' },
  Q3_gezin: { bg: 'bg-emerald-500/10', tekst: 'text-emerald-700', rand: 'border-emerald-400/40', icon: '👥' },
  Q4_leeftijd: { bg: 'bg-violet-500/10', tekst: 'text-violet-700', rand: 'border-violet-400/40', icon: '⏳' },
  Q5_regio: { bg: 'bg-rose-500/10', tekst: 'text-rose-700', rand: 'border-rose-400/40', icon: '📍' },
  Q6_bedrijfslaag: { bg: 'bg-cyan-500/10', tekst: 'text-cyan-700', rand: 'border-cyan-400/40', icon: '🏢' },
  Q7_netwerk: { bg: 'bg-fuchsia-500/10', tekst: 'text-fuchsia-700', rand: 'border-fuchsia-400/40', icon: '🌐' },
};

// ============================================================================
// HOOFDCOMPONENT
// ============================================================================
export default function PersonaFlow() {
  const [antwoorden, setAntwoorden] = useState<Antwoorden>({});
  const [orde, setOrde] = useState<'1e' | '2e' | '3e' | 'totaal'>('totaal');
  const [uitlegPartij, setUitlegPartij] = useState<string | null>(null);
  const [eigenKeuze, setEigenKeuze] = useState<string | null>(null);
  // Regel 105 v3.9: referentiemodellen VMP en CARB — aparte toggles per model
  // v3.20.15 — VMP en CARB zijn normale partijen, geen aparte toggles meer.
  // De props toonVMP/toonCARB blijven bestaan in LevensloopGrafiek voor
  // backward-compat maar worden altijd op false gezet.

  const vragen = getVragen() as Record<string, VraagData>;
  const partijMeta = getPartijMeta();

  const huidigeVraag = useMemo<VraagId | null>(() => {
    for (const q of VRAGEN_VOLGORDE) if (!antwoorden[q]) return q;
    const q1 = antwoorden['Q1_sector'];
    if (typeof q1 === 'string') {
      if (vragen.Q6_bedrijfslaag?.conditioneel_op_Q1?.includes(q1) && !antwoorden['Q6_bedrijfslaag']) return 'Q6_bedrijfslaag';
      if (vragen.Q7_netwerk?.conditioneel_op_Q1?.includes(q1) && !antwoorden['Q7_netwerk']) return 'Q7_netwerk';
    }
    return null;
  }, [antwoorden, vragen]);

  const gegevenAntwoorden = useMemo(() => {
    const lijst: Array<{ vraag_id: string; label: string; antwoord_label: string; sleutel: string }> = [];
    for (const qid of [...VRAGEN_VOLGORDE, 'Q6_bedrijfslaag', 'Q7_netwerk'] as const) {
      const ant = antwoorden[qid];
      if (!ant || ant === '__skip__') continue;
      const key = typeof ant === 'string' ? ant : ant[0];
      const opties = vragen[qid]?.antwoorden as Record<string, VraagOptie> | undefined;
      const antLabel = opties?.[key]?.label || key;
      lijst.push({ vraag_id: qid, label: VRAAG_LABELS[qid] || qid, antwoord_label: antLabel, sleutel: key });
    }
    return lijst;
  }, [antwoorden, vragen]);

  const ranglijst = useMemo<PartijResultaat[]>(() => berekenRanglijst(antwoorden, orde), [antwoorden, orde]);

  const resetAlles = () => { setAntwoorden({}); setUitlegPartij(null); setEigenKeuze(null); setOrde('totaal'); window.scrollTo({ top: 0, behavior: 'smooth' }); };
  const setAntwoord = (vraagId: string, value: string) => { setAntwoorden((prev) => ({ ...prev, [vraagId]: value })); setUitlegPartij(null); };
  const verwijderAntwoord = (vraagId: string) => {
    setAntwoorden((prev) => {
      const n = { ...prev };
      delete n[vraagId];
      const idx = VRAGEN_VOLGORDE.indexOf(vraagId as any);
      if (idx >= 0) { for (let i = idx + 1; i < VRAGEN_VOLGORDE.length; i++) delete n[VRAGEN_VOLGORDE[i]]; delete n['Q6_bedrijfslaag']; delete n['Q7_netwerk']; }
      return n;
    });
    setUitlegPartij(null);
  };

  const filterAntwoorden = (vraagId: string): Record<string, VraagOptie> => {
    const vraag = vragen[vraagId];
    if (!vraag) return {};
    if (vraagId === 'Q6_bedrijfslaag') {
      const q1 = antwoorden['Q1_sector'];
      if (typeof q1 !== 'string') return vraag.antwoorden;
      const filtered: Record<string, VraagOptie> = {};
      for (const [k, v] of Object.entries(vraag.antwoorden)) {
        const av = v as any;
        if (!av.alleen_voor || av.alleen_voor.includes(q1)) filtered[k] = v;
      }
      return filtered;
    }
    return vraag.antwoorden;
  };

  const maxAbs = Math.max(...ranglijst.map((r) => Math.abs(r.eerste_orde) + Math.abs(r.tweede_orde) + Math.abs(r.derde_orde)), 1);
  const gekozenPartij = uitlegPartij ? ranglijst.find((r) => r.partij_id === uitlegPartij) : null;
  const heeftAntwoorden = gegevenAntwoorden.length > 0;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 relative overflow-x-hidden">
      {/* Aurora background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-sky-300/30 rounded-full blur-[120px]" />
        <div className="absolute top-40 -right-40 w-[500px] h-[500px] bg-emerald-300/25 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 left-1/3 w-[700px] h-[400px] bg-violet-300/20 rounded-full blur-[120px]" />
      </div>

      {/* Header */}
      <header className="relative border-b border-slate-200 backdrop-blur-sm bg-white/70 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <button onClick={resetAlles} className="flex items-center gap-2.5 group" data-testid="button-home">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-400 to-violet-500 flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-sky-500/30">
              GK
            </div>
            <span className="font-bold tracking-tight text-slate-900">Gevolgenkaart</span>
            <span className="text-[10px] uppercase tracking-widest text-slate-400 hidden sm:inline">v3 · cascade-model</span>
          </button>
          {heeftAntwoorden && (
            <button onClick={resetAlles} className="text-xs text-slate-500 hover:text-slate-900 transition" data-testid="button-reset">
              ↺ Begin opnieuw
            </button>
          )}
        </div>
      </header>

      {/* CENTRAAL PANEL */}
      <main className="relative max-w-4xl mx-auto px-4 sm:px-6 py-8 z-10">
        <article className="bg-white/95 backdrop-blur-xl border border-slate-200 rounded-2xl shadow-xl shadow-slate-300/40 overflow-hidden">

          {/* INTRO */}
          {!heeftAntwoorden && (
            <section className="px-8 py-10 border-b border-slate-200 relative">
              <div className="absolute top-6 right-6 text-[10px] uppercase tracking-widest font-semibold text-sky-700 bg-sky-100 px-2.5 py-1 rounded-full border border-sky-300">
                live ranking
              </div>
              <h1 className="text-3xl sm:text-4xl font-bold tracking-tight mb-3 leading-tight bg-gradient-to-r from-slate-900 via-sky-700 to-violet-700 bg-clip-text text-transparent">
                Wat doen politieke keuzes<br/>écht voor jou?
              </h1>
              <p className="text-sm text-slate-600 leading-relaxed max-w-xl">
                Beantwoord een paar korte vragen. Het systeem berekent live welke partij in 1e, 2e en 3e orde voor jouw situatie uitpakt — niet alleen vandaag, maar ook over 2 en 5 jaar.
              </p>
              <div className="flex items-center gap-3 mt-5 text-[11px] text-slate-500">
                <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-emerald-400/50 shadow-[0_0_8px]" /> 17 partijen</span>
                <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-sky-500 shadow-sky-400/50 shadow-[0_0_8px]" /> ~180 elementen</span>
                <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-violet-500 shadow-violet-400/50 shadow-[0_0_8px]" /> 9 cascade-filters</span>
              </div>
            </section>
          )}

          {/* HUIDIGE VRAAG — v3.12c altijd BOVEN eigen-keuze en grafieken
              tot alle vragen zijn beantwoord. Tegels blijven zo in beeld
              terwijl de gebruiker door de vragen loopt. */}
          {huidigeVraag && (
            <section className="px-6 sm:px-8 py-8 border-b border-slate-200 animate-[fadein_0.4s_ease-out]" data-testid="huidige-vraag">
              <div className="flex items-center gap-2 mb-1">
                <span className={`text-[10px] uppercase tracking-widest font-bold ${VRAAG_ACCENT[huidigeVraag]?.tekst || 'text-sky-700'}`}>
                  Vraag {gegevenAntwoorden.length + 1}
                </span>
                {!vragen[huidigeVraag]?.verplicht && (
                  <button onClick={() => setAntwoorden((prev) => ({ ...prev, [huidigeVraag]: '__skip__' }))}
                    className="ml-auto text-xs text-slate-400 hover:text-slate-700 transition" data-testid="button-overslaan">
                    overslaan →
                  </button>
                )}
              </div>
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-5 leading-tight">
                {vragen[huidigeVraag]?.vraag}
              </h2>
              {huidigeVraag === 'Q1_sector' ? (
                <SectorKeuze opties={filterAntwoorden('Q1_sector')} onKies={(k) => setAntwoord('Q1_sector', k)} />
              ) : (
                <KeuzeLijst vraagId={huidigeVraag} opties={filterAntwoorden(huidigeVraag)} onKies={(k) => setAntwoord(huidigeVraag, k)} />
              )}
            </section>
          )}

          {/* EIGEN KEUZE — pas na eerste antwoord, ONDER de huidige vraag,
              zodat de vraag-tegels boven in beeld blijven. */}
          {heeftAntwoorden && ranglijst.length > 0 && (() => {
            const REF_IDS = new Set<string>();  // v3.20.15 leeg — VMP/CARB zijn normale partijen
            const echtePartijen = ranglijst.filter((r) => !REF_IDS.has(r.partij_id) && !isReferentie(r.partij_id));
            const eigenResultaat = eigenKeuze ? ranglijst.find((r) => r.partij_id === eigenKeuze) : null;
            return (
              <EigenKeuzeBlok
                ranglijst={echtePartijen}
                gekozenResultaat={eigenResultaat}
                partijMeta={partijMeta}
                eigenKeuze={eigenKeuze}
                onEigenKeuze={setEigenKeuze}
                onBekijkUitleg={() => {
                  if (eigenResultaat) {
                    setUitlegPartij(eigenResultaat.partij_id);
                    setTimeout(() => {
                      document.querySelector('[data-testid="uitleg-paneel"]')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                  }
                }}
              />
            );
          })()}

          {/* LEVENSLOOP-PROJECTIE — 15 jaar vooruit met herkeuzemomenten */}
          {heeftAntwoorden && ranglijst.length > 0 && (() => {
            const REF_IDS = new Set<string>();  // v3.20.15 leeg — VMP/CARB zijn normale partijen
            const isRef = (id: string) => REF_IDS.has(id) || isReferentie(id);
            const echteTop = ranglijst.find((r) => !isRef(r.partij_id)) || ranglijst[0];
            const eigenPartij = eigenKeuze || echteTop.partij_id;
            const sector = antwoorden.Q1_sector || 'S9';
            let lev;
            try {
              lev = berekenLevensloop(antwoorden, echteTop.partij_id, eigenPartij, sector, 15);
            } catch (e) {
              return null;
            }
            return (
              <section className="px-6 sm:px-8 py-6 border-b border-slate-200 bg-white" data-testid="levensloop-sectie">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-[10px] uppercase tracking-widest font-bold text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded-full border border-emerald-300">
                    ⏱ 15-jaars levensloop
                  </span>
                  <div className="flex-1 h-px bg-gradient-to-r from-emerald-300 to-transparent" />
                </div>
                <h3 className="text-lg sm:text-xl font-bold text-slate-900 mb-1 leading-tight">
                  Hoe ontwikkelt jouw inkomen zich — met of zonder herkeuze op levenssprongen
                </h3>
                <p className="text-xs text-slate-500 mb-4 leading-relaxed">
                  Index <strong>100 = vandaag</strong>. De groene gestreepte lijn toont wat er gebeurt als je bij elke levensovergang (student→starter, werkend→pensioen) de partij heroverweegt. Onzekerheidsband groeit lineair tot ±25% in jaar 15. Leverbaarheid van een partij is meegenomen op de 1e-orde score.
                </p>
                {/* v3.20.15 — VMP en CARB zijn normale partijen: geen aparte toggles meer. */}
                <LevensloopGrafiek data={lev} partijMeta={partijMeta} toonVMP={false} toonCARB={false} />

                {/* Regel 113/114 v3.10: Gezondheidsgrafiek van Spanje (NEPK) */}
                {(() => {
                  const nepkPartij = eigenPartij || echteTop.partij_id;
                  const nepkData = berekenNEPK(antwoorden, nepkPartij, 15);
                  const partijInfo = (partijMeta as any)[nepkPartij] || {};
                  return (
                    <section className="mt-8 pt-6 border-t border-slate-200">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-[10px] uppercase tracking-widest font-bold text-red-700 bg-red-100 px-2.5 py-1 rounded-full border border-red-300">
                          🏥 Gezondheidsgrafiek van Spanje (NTPK / NEPK)
                        </span>
                        <div className="flex-1 h-px bg-gradient-to-r from-red-300 to-transparent" />
                      </div>
                      <h3 className="text-lg sm:text-xl font-bold text-slate-900 mb-1 leading-tight">
                        Gezondheidsverloop van de Spaanse economie bij uw keuze
                      </h3>
                      <p className="text-xs text-slate-500 mb-4 leading-relaxed">
                        <strong>NEPK = E<sub>tv</sub> × α × (1−τ) × φ</strong> — canonieke formule uit <a href="https://novademocratia.com/assets/docs/nepk-indicator-methodologie.pdf" target="_blank" rel="noopener" className="underline">nepk-indicator-methodologie.pdf</a>. Drie grootheden: <strong>NTPK</strong> = totale productie binnen Spanje (ongeacht eigenaar). <strong>NEPK</strong> = NTPK × φ (deel in Spaanse handen). <strong>NPK</strong> = NTPK × (1+ψ) = productie in Spaanse handen wereldwijd, inclusief buitenlandse dochters (Santander LatAm, Iberdrola VS, Inditex, Telefónica). Startwaarden 2026: E<sub>tv</sub>=27,9%, α=0,321, τ=0,397, φ=0,76, ψ=0,31 (BdE Balance of Payments 2024) → <strong>NTPK = 5,40%</strong>, <strong>NEPK = 4,10%</strong>, <strong>NPK = 7,08% BBP</strong>. Historische aanloop (Eurostat + EC Spring 2026): 4,32% (2024) → 4,18% (2025) → 4,10% (2026). Kritiek: <strong>2,5%</strong> = sociaal kantelpunt, <strong>2,0%</strong> = point-of-no-return. Grijze baseline toont trend zonder ombuiging; partij-lijn toont drie-orde-modulatie (jaar 1-3 / 4-8 / 9-15).
                      </p>
                      <div className="mb-4">
                        <HistorischeTrend landLabel="Spanje" taal="nl" />
                      </div>
                      <GezondheidsgrafiekNL
                        data={nepkData}
                        partijNaam={partijInfo.naam || nepkPartij}
                        partijKleur={partijInfo.kleur}
                      />
                    </section>
                  );
                })()}
                {lev.herkeuzes.length > 0 && (
                  <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50/60 p-3 text-xs text-slate-700">
                    <strong className="text-emerald-700">Aanbeveling op levenssprong:</strong>{' '}
                    {lev.herkeuzes.map((h, i) => (
                      <span key={i}>
                        {i > 0 ? '; ' : ''}
                        op jaar {h.jaar} ({h.nieuwe_fase === 'pensioen' ? 'pensioen' : h.nieuwe_fase}) — herkies <strong>{h.naar_partij}</strong> ipv {h.van_partij}
                      </span>
                    ))}.
                  </div>
                )}
              </section>
            );
          })()}

          {/* RANGLIJST */}
          <section className="px-6 sm:px-8 py-8" data-testid="ranglijst-sectie">
            <div className="flex items-baseline justify-between mb-2">
              <div>
                <div className="text-[10px] uppercase tracking-widest font-bold text-emerald-700 mb-0.5">Live uitkomst</div>
                <h3 className="text-xl font-bold text-slate-900">
                  {heeftAntwoorden ? 'Jouw ranglijst' : 'Gemiddelde Spanjaard'}
                </h3>
              </div>
              <div className="flex items-center gap-1.5 bg-slate-100 rounded-lg p-1 border border-slate-200">
                {(['1e', '2e', '3e', 'totaal'] as const).map((o) => (
                  <button
                    key={o}
                    onClick={() => setOrde(o)}
                    className={`px-2.5 py-1 text-xs font-medium rounded transition ${
                      orde === o
                        ? 'bg-gradient-to-br from-sky-400 to-violet-500 text-white shadow-lg shadow-sky-500/30'
                        : 'text-slate-500 hover:text-slate-900'
                    }`}
                    data-testid={`button-orde-${o}`}
                  >
                    {o === 'totaal' ? 'Σ' : o}
                  </button>
                ))}
              </div>
            </div>
            <p className="text-xs text-slate-500 mb-5">
              {heeftAntwoorden
                ? 'Live bijgewerkt op basis van je profiel. Klik op een partij voor uitleg.'
                : 'Doorsnee-Spanjaard zonder verdere context. Beantwoord vragen om het scherper te maken.'}
            </p>

            <div className="space-y-1">
              {ranglijst.map((r, i) => {
                const meta = partijMeta[r.partij_id];
                const kleur = naarHex(meta?.kleur || '');
                const isGekozen = uitlegPartij === r.partij_id;
                return (
                  <CascadeBalk
                    key={r.partij_id}
                    rang={i + 1}
                    partijId={r.partij_id}
                    partijNaam={meta?.naam || r.partij_id}
                    partijKleur={kleur}
                    v1={r.eerste_orde}
                    v2={r.tweede_orde}
                    v3={r.derde_orde}
                    maxAbs={maxAbs}
                    orde={orde}
                    isGekozen={isGekozen}
                    onClick={() => setUitlegPartij(isGekozen ? null : r.partij_id)}
                  />
                );
              })}
            </div>

            <div className="flex items-center gap-4 mt-4 pt-3 border-t border-slate-200 text-[10px] text-slate-500">
              <span className="flex items-center gap-1.5"><span className="inline-block w-2.5 h-2.5 rounded-sm bg-slate-800" />1e direct</span>
              <span className="flex items-center gap-1.5"><span className="inline-block w-2.5 h-2.5 rounded-sm bg-slate-500" />2e gevolg</span>
              <span className="flex items-center gap-1.5"><span className="inline-block w-2.5 h-2.5 rounded-sm bg-slate-300" />3e gevolg-van-gevolg</span>
            </div>

            {/* UITLEG-TOGGLE — wat betekenen de 1e/2e/3e orde + bronnen */}
            <UitlegOrdesEnBronnen />
          </section>

          {/* PROFIEL-TROFEEEN — mini-hero's van gemaakte keuzes */}
          {heeftAntwoorden && (
            <section className="px-6 sm:px-8 pt-6 pb-5 border-b border-slate-200">
              <div className="flex items-center gap-2 mb-3">
                <div className="text-[10px] uppercase tracking-widest font-semibold text-slate-500">Jouw profiel</div>
                <div className="flex-1 h-px bg-gradient-to-r from-slate-300 to-transparent" />
              </div>
              <div className="flex flex-wrap gap-3">
                {gegevenAntwoorden.map((a) => (
                  <MiniHero
                    key={a.vraag_id}
                    icon={a.vraag_id === 'Q1_sector' && SECTOR_ICONS[a.sleutel]
                      ? <SectorIconWrap iconKey={a.sleutel} />
                      : iconVoorAntwoord(a.vraag_id, a.sleutel)}
                    label={a.antwoord_label}
                    sublabel={a.label}
                    accent={accentVoorVraag(a.vraag_id)}
                    size="sm"
                    variant="trofee"
                    onWissen={() => verwijderAntwoord(a.vraag_id)}
                    testId={`trofee-${a.vraag_id}`}
                  />
                ))}
              </div>
            </section>
          )}

          {/* TOPUITKOMST — computer-advies, pas na eerste antwoord */}
          {heeftAntwoorden && ranglijst.length > 0 && (() => {
            const REF_IDS = new Set<string>();  // v3.20.15 leeg — VMP/CARB zijn normale partijen
            const isRef = (id: string) => REF_IDS.has(id) || isReferentie(id);
            const refTop = ranglijst.find((r) => isRef(r.partij_id)) || null;
            const echteTop = ranglijst.find((r) => !isRef(r.partij_id)) || ranglijst[0];
            return (
              <TopUitkomstKaart
                top={echteTop}
                refModel={refTop && refTop.partij_id !== echteTop.partij_id ? refTop : null}
                partijMeta={partijMeta}
                isPersoonlijk={heeftAntwoorden}
                onKlik={() => {
                  setUitlegPartij(echteTop.partij_id);
                  setTimeout(() => {
                    document.querySelector('[data-testid="uitleg-paneel"]')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }, 100);
                }}
              />
            );
          })()}

          {/* UITLEG-PANEEL */}
          {gekozenPartij && (
            <section className="px-6 sm:px-8 py-8 border-t border-slate-200 bg-slate-50 animate-[fadein_0.4s_ease-out]" data-testid="uitleg-paneel">
              <UitlegPaneel
                resultaat={gekozenPartij}
                orde={orde}
                partijMeta={partijMeta}
                antwoorden={antwoorden}
                onSluit={() => setUitlegPartij(null)}
              />
            </section>
          )}

          {/* FOOTER */}
          <footer className="px-6 sm:px-8 py-4 border-t border-slate-200 text-[11px] text-slate-500 leading-relaxed bg-slate-50/80">
            De Gevolgenkaart geeft geen stemadvies. Persoonlijke schatting via basis 9 × overlays met cascade naar 2e en 3e orde via 9×9 filter-interactiematrix met asymmetrische overshoot-correctie.
          </footer>
        </article>
      </main>

      <style>{`
        @keyframes fadein {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}

// ============================================================================
// TOP-UITKOMSTKAART — doorschakel-blok naar de winnaar + top 3 ± gevolgen
// ============================================================================
interface TopUitkomstProps {
  top: PartijResultaat;
  refModel: PartijResultaat | null;
  partijMeta: Record<string, { naam?: string; kleur?: string; cluster?: string }>;
  isPersoonlijk: boolean;
  onKlik: () => void;
}
function TopUitkomstKaart({ top, refModel, partijMeta, isPersoonlijk, onKlik }: TopUitkomstProps) {
  const meta = partijMeta[top.partij_id];
  const kleur = naarHex(meta?.kleur || '#0ea5e9');
  const totaal = top.eerste_orde + top.tweede_orde + top.derde_orde;
  const topPos = top.top_positief.filter((b) => b.bijdrage > 0.5).slice(0, 3);
  const topNeg = top.top_negatief.filter((b) => b.bijdrage < -0.5).slice(0, 3);

  const koplabel = isPersoonlijk
    ? 'Computer-advies: beste partij op het stembiljet voor jou'
    : 'Computer-advies: beste partij — gemiddelde Spanjaard';

  return (
    <section className="px-6 sm:px-8 py-6 border-b border-slate-200 bg-gradient-to-br from-white to-slate-50" data-testid="top-uitkomst">
      {/* Referentiemodel-banner (CARB/VMP): toont als had-de-beste-geweest */}
      {refModel && (() => {
        const rMeta = partijMeta[refModel.partij_id];
        const rKleur = naarHex(rMeta?.kleur || '#10b981');
        const rTot = refModel.eerste_orde + refModel.tweede_orde + refModel.derde_orde;
        return (
          <div className="mb-3 rounded-lg border border-dashed p-2.5 flex items-baseline gap-2 text-[12px]" style={{ borderColor: `${rKleur}66`, backgroundColor: `${rKleur}0c` }}>
            <span className="text-[9px] uppercase tracking-widest font-bold" style={{ color: rKleur }}>referentie-model</span>
            <span className="font-bold tabular-nums" style={{ color: rKleur }}>{refModel.partij_id}</span>
            <span className="text-slate-600">({rMeta?.naam})</span>
            <span className="text-slate-500">zou structureel beter scoren —</span>
            <span className={`tabular-nums font-bold ${rTot >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>{rTot > 0 ? '+' : ''}{rTot.toFixed(0)}</span>
            <span className="text-slate-500">— maar staat niet op het stembiljet.</span>
          </div>
        );
      })()}

      <div className="flex items-center gap-2 mb-3">
        <div className="text-[10px] uppercase tracking-widest font-bold text-emerald-700">{koplabel}</div>
        <div className="flex-1 h-px bg-gradient-to-r from-emerald-300 to-transparent" />
      </div>

      <button
        onClick={onKlik}
        className="w-full text-left rounded-xl border-2 p-4 sm:p-5 transition hover:shadow-lg group"
        style={{ borderColor: `${kleur}55`, backgroundColor: `${kleur}08` }}
        data-testid="top-uitkomst-knop"
      >
        <div className="flex items-center justify-between gap-4 mb-3">
          <div className="flex items-baseline gap-3">
            <span
              className="text-3xl sm:text-4xl font-bold tracking-tight"
              style={{ color: kleur, textShadow: `0 0 18px ${kleur}33` }}
            >
              {top.partij_id}
            </span>
            <span className="text-sm text-slate-600">{meta?.naam}</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">totaal</span>
            <span className={`text-2xl font-bold tabular-nums ${totaal >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
              {totaal > 0 ? '+' : ''}{totaal.toFixed(0)}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-5">
          <div className="rounded-lg border border-emerald-200 bg-emerald-50/60 p-3">
            <div className="text-[10px] uppercase tracking-widest font-bold text-emerald-700 mb-1.5 flex items-center gap-1.5">
              <span>↑</span> Wat dit voor jou oplevert
            </div>
            {topPos.length === 0 ? (
              <p className="text-xs text-slate-500 italic">Geen sterk positieve gevolgen.</p>
            ) : (
              <ul className="space-y-1">
                {topPos.map((b) => (
                  <li key={b.element_id} className="flex items-baseline gap-2 text-[13px]">
                    <span className="font-mono text-emerald-700 font-bold tabular-nums w-10 shrink-0">+{b.bijdrage.toFixed(0)}</span>
                    <span className="text-slate-700 leading-snug">{b.naam}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="rounded-lg border border-rose-200 bg-rose-50/60 p-3">
            <div className="text-[10px] uppercase tracking-widest font-bold text-rose-700 mb-1.5 flex items-center gap-1.5">
              <span>↓</span> Wat dit voor jou kost
            </div>
            {topNeg.length === 0 ? (
              <p className="text-xs text-slate-500 italic">Geen sterk negatieve gevolgen.</p>
            ) : (
              <ul className="space-y-1">
                {topNeg.map((b) => (
                  <li key={b.element_id} className="flex items-baseline gap-2 text-[13px]">
                    <span className="font-mono text-rose-700 font-bold tabular-nums w-10 shrink-0">{b.bijdrage.toFixed(0)}</span>
                    <span className="text-slate-700 leading-snug">{b.naam}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="mt-3 flex items-center justify-end gap-1 text-xs text-sky-700 font-semibold group-hover:gap-2 transition-all">
          <span>Bekijk volledige ranglijst en uitleg</span>
          <span>→</span>
        </div>
      </button>
    </section>
  );
}

// ============================================================================
// EIGEN KEUZE-BLOK — prominent: gebruiker kiest partij, ziet eigen impact
// ============================================================================
interface EigenKeuzeProps {
  ranglijst: PartijResultaat[];
  gekozenResultaat: PartijResultaat | null | undefined;
  partijMeta: Record<string, { naam?: string; kleur?: string; cluster?: string }>;
  eigenKeuze: string | null;
  onEigenKeuze: (id: string | null) => void;
  onBekijkUitleg: () => void;
}
function EigenKeuzeBlok({ ranglijst, gekozenResultaat, partijMeta, eigenKeuze, onEigenKeuze, onBekijkUitleg }: EigenKeuzeProps) {
  return (
    <section className="px-6 sm:px-8 py-6 border-b border-slate-200 bg-gradient-to-br from-sky-50/70 via-white to-violet-50/40" data-testid="eigen-keuze-blok">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-[10px] uppercase tracking-widest font-bold text-sky-700 bg-sky-100 px-2.5 py-1 rounded-full border border-sky-300">
          ★ Mijn eigen keuze
        </span>
        <div className="flex-1 h-px bg-gradient-to-r from-sky-300 to-transparent" />
      </div>
      <h3 className="text-lg sm:text-xl font-bold text-slate-900 mb-3 leading-tight">
        Welke partij wil <span className="text-sky-700">jij</span> stemmen?
      </h3>

      {/* Partij-pills — alle echte partijen op rij */}
      <div className="flex flex-wrap gap-2 mb-4">
        {ranglijst.map((r) => {
          const m = partijMeta[r.partij_id];
          const k = naarHex(m?.kleur || '#64748b');
          const isActief = eigenKeuze === r.partij_id;
          return (
            <button
              key={r.partij_id}
              onClick={() => onEigenKeuze(isActief ? null : r.partij_id)}
              className={`px-3 py-1.5 rounded-full text-sm font-bold tabular-nums border-2 transition ${
                isActief ? 'shadow-lg scale-105' : 'hover:scale-105 hover:shadow-md'
              }`}
              style={{
                borderColor: isActief ? k : `${k}55`,
                backgroundColor: isActief ? `${k}1f` : '#ffffff',
                color: k,
                textShadow: isActief ? `0 0 10px ${k}55` : 'none',
              }}
              data-testid={`eigen-pill-${r.partij_id}`}
              title={m?.naam}
            >
              {r.partij_id}
            </button>
          );
        })}
        {eigenKeuze && (
          <button
            onClick={() => onEigenKeuze(null)}
            className="px-3 py-1.5 rounded-full text-xs text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition"
            data-testid="eigen-keuze-wissen"
          >
            wissen ×
          </button>
        )}
      </div>

      {/* Preview als er een eigen keuze is */}
      {gekozenResultaat ? (() => {
        const m = partijMeta[gekozenResultaat.partij_id];
        const k = naarHex(m?.kleur || '#64748b');
        const tot = gekozenResultaat.eerste_orde + gekozenResultaat.tweede_orde + gekozenResultaat.derde_orde;
        const pos = gekozenResultaat.top_positief.filter((b) => b.bijdrage > 0.5).slice(0, 3);
        const neg = gekozenResultaat.top_negatief.filter((b) => b.bijdrage < -0.5).slice(0, 3);
        return (
          <button
            onClick={onBekijkUitleg}
            className="w-full text-left rounded-xl border-2 p-4 sm:p-5 transition hover:shadow-lg group"
            style={{ borderColor: k, backgroundColor: `${k}10` }}
            data-testid="eigen-keuze-preview"
          >
            <div className="flex items-center justify-between gap-4 mb-3">
              <div className="flex items-baseline gap-3">
                <span
                  className="text-3xl sm:text-4xl font-bold tracking-tight"
                  style={{ color: k, textShadow: `0 0 18px ${k}55` }}
                >
                  {gekozenResultaat.partij_id}
                </span>
                <span className="text-sm text-slate-700 font-medium">{m?.naam}</span>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">totaal voor jou</span>
                <span className={`text-2xl sm:text-3xl font-bold tabular-nums ${tot >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {tot > 0 ? '+' : ''}{tot.toFixed(0)}
                </span>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-5">
              <div className="rounded-lg border border-emerald-200 bg-emerald-50/70 p-3">
                <div className="text-[10px] uppercase tracking-widest font-bold text-emerald-700 mb-1.5">↑ Wat dit jou oplevert</div>
                {pos.length === 0 ? (
                  <p className="text-xs text-slate-500 italic">Geen sterk positieve gevolgen.</p>
                ) : (
                  <ul className="space-y-1">
                    {pos.map((b) => (
                      <li key={b.element_id} className="flex items-baseline gap-2 text-[13px]">
                        <span className="font-mono text-emerald-700 font-bold tabular-nums w-10 shrink-0">+{b.bijdrage.toFixed(0)}</span>
                        <span className="text-slate-700 leading-snug">{b.naam}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <div className="rounded-lg border border-rose-200 bg-rose-50/70 p-3">
                <div className="text-[10px] uppercase tracking-widest font-bold text-rose-700 mb-1.5">↓ Wat dit jou kost</div>
                {neg.length === 0 ? (
                  <p className="text-xs text-slate-500 italic">Geen sterk negatieve gevolgen.</p>
                ) : (
                  <ul className="space-y-1">
                    {neg.map((b) => (
                      <li key={b.element_id} className="flex items-baseline gap-2 text-[13px]">
                        <span className="font-mono text-rose-700 font-bold tabular-nums w-10 shrink-0">{b.bijdrage.toFixed(0)}</span>
                        <span className="text-slate-700 leading-snug">{b.naam}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
            <div className="mt-3 flex items-center justify-end gap-1 text-xs font-semibold group-hover:gap-2 transition-all" style={{ color: k }}>
              <span>Bekijk volledige analyse van {gekozenResultaat.partij_id}</span>
              <span>→</span>
            </div>
          </button>
        );
      })() : (
        <p className="text-sm text-slate-500 italic">
          Klik hierboven op jouw partij om te zien wat échte gevolgen voor jóu zijn — los van wat de computer adviseert.
        </p>
      )}
    </section>
  );
}

// ============================================================================
// UITLEG ORDES + BRONNEN — uitklapbaar onder de ranglijst
// ============================================================================
function UitlegOrdesEnBronnen() {
  const [tab, setTab] = useState<'ordes' | 'bronnen' | 'methode' | null>(null);

  const TabKnop = ({ id, label, icon }: { id: 'ordes' | 'bronnen' | 'methode'; label: string; icon: string }) => (
    <button
      onClick={() => setTab(tab === id ? null : id)}
      className={`px-3 py-1.5 text-xs font-semibold rounded-lg border transition ${
        tab === id
          ? 'bg-sky-100 border-sky-400 text-sky-800'
          : 'bg-white border-slate-200 text-slate-600 hover:border-sky-300 hover:bg-sky-50'
      }`}
      data-testid={`uitleg-tab-${id}`}
    >
      <span className="mr-1.5">{icon}</span>{label}
    </button>
  );

  return (
    <div className="mt-5 pt-4 border-t border-slate-200">
      <div className="flex flex-wrap items-center gap-2 mb-3">
        <span className="text-[10px] uppercase tracking-widest font-bold text-slate-500 mr-1">Wat zie ik hier?</span>
        <TabKnop id="ordes" label="1e · 2e · 3e orde" icon="⏱" />
        <TabKnop id="bronnen" label="Bronnen & historische data" icon="📚" />
        <TabKnop id="methode" label="Hoe de score tot stand komt" icon="🔬" />
      </div>

      {tab === 'ordes' && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700 leading-relaxed space-y-3 animate-[fadein_0.3s_ease-out]" data-testid="uitleg-content-ordes">
          <div>
            <span className="inline-block w-2.5 h-2.5 rounded-sm bg-slate-800 mr-2 align-middle" />
            <strong className="text-slate-900">1e orde — directe gevolgen (0-12 maanden).</strong>{' '}
            Wat je binnen een jaar in jouw portemonnee, baan of dagelijks leven merkt: koopkracht, belastingen, premies, eigen risico, regeldruk.
          </div>
          <div>
            <span className="inline-block w-2.5 h-2.5 rounded-sm bg-slate-500 mr-2 align-middle" />
            <strong className="text-slate-900">2e orde — doorwerking (2-5 jaar).</strong>{' '}
            Hoe de markt en de samenleving reageren: bedrijven verschuiven hun investeringen, mensen veranderen van baan, woningen worden wel of niet gebouwd, kapitaal vlucht of komt terug. Beleid van vandaag bepaalt de keuzes van bedrijven en burgers van morgen.
          </div>
          <div>
            <span className="inline-block w-2.5 h-2.5 rounded-sm bg-slate-300 mr-2 align-middle" />
            <strong className="text-slate-900">3e orde — structurele doorwerking (5-15 jaar).</strong>{' '}
            De productieve basis zelf verschuift: instituties verzwakken of versterken, talent vertrekt of komt terug, infrastructuur veroudert of vernieuwt, vertrouwen brokkelt af of groeit. Hier wordt zichtbaar of beleid eet van de toekomst of die toekomst opbouwt.
          </div>
          <div className="mt-3 pt-3 border-t border-slate-200 text-xs text-slate-600 italic">
            De getrapte balkjes laten zien hoe een eerste positief signaal in latere ordes kan kantelen (of juist versterken). Sparen-eerst beleid scoort vaak laag in 1e orde maar bouwt in 3e orde de basis op; uitgeven-eerst beleid pieket in 1e orde en daalt scherp in 3e.
          </div>
        </div>
      )}

      {tab === 'bronnen' && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700 leading-relaxed space-y-3 animate-[fadein_0.3s_ease-out]" data-testid="uitleg-content-bronnen">
          <p>
            De cascade-coëfficiënten zijn gekalibreerd aan <strong className="text-slate-900">historische natuurlijke experimenten</strong>{' '}
            waarin beleid de productieve basis van een land daadwerkelijk raakte. Geen modelmatige voorspellingen, maar gemeten relatieve verschuivingen.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
            <div className="rounded-md border border-rose-200 bg-rose-50/60 p-3">
              <div className="text-[11px] uppercase tracking-widest font-bold text-rose-700 mb-1">🇦🇷 Argentinië (2003–2019)</div>
              <p className="text-xs leading-relaxed">
                Herhaalde vermogensheffingen, prijscontroles en kapitaalrestricties. <strong>Resultaat:</strong> meetbare krimp productieve basis, hoge inflatie, kapitaalvlucht naar Uruguay/USA, herhaalde valutaschokken. Levert kalibratie voor sparen-versus-uitgeven asymmetrie.
              </p>
            </div>
            <div className="rounded-md border border-amber-200 bg-amber-50/60 p-3">
              <div className="text-[11px] uppercase tracking-widest font-bold text-amber-700 mb-1">🇿🇦 Zuid-Afrika (1994–2024)</div>
              <p className="text-xs leading-relaxed">
                Institutionele erosie, brain drain van hooggeschoolden (≈ 1 mln vertrokken), desinvestering in netinfrastructuur (load shedding). <strong>Resultaat:</strong> 1e-orde herverdelingswinst werd 3e-orde structurele verarming. Levert de overshoot-factor voor institutionele schade.
              </p>
            </div>
            <div className="rounded-md border border-sky-200 bg-sky-50/60 p-3">
              <div className="text-[11px] uppercase tracking-widest font-bold text-sky-700 mb-1">🌎 Latijns-Amerika breder</div>
              <p className="text-xs leading-relaxed">
                Venezuela (olie-staat in verval), Chili (hervormingen jaren 80-90), Brazilië (commodity-cycles). <strong>Resultaat:</strong> levert cross-checks op de cascade-effecten van populistisch herverdelingsbeleid versus institutionele hervorming.
              </p>
            </div>
            <div className="rounded-md border border-emerald-200 bg-emerald-50/60 p-3">
              <div className="text-[11px] uppercase tracking-widest font-bold text-emerald-700 mb-1">🇨🇭 Zwitserland / 🇸🇬 Singapore</div>
              <p className="text-xs leading-relaxed">
                Sparen-eerst regimes met sterke instituties. <strong>Resultaat:</strong> stabiele 3e-orde productiviteitsgroei na 1e-orde terughoudendheid. Levert de positieve overshoot voor sparen.
              </p>
            </div>
            <div className="rounded-md border border-violet-200 bg-violet-50/60 p-3">
              <div className="text-[11px] uppercase tracking-widest font-bold text-violet-700 mb-1">🇩🇪 Duitsland (Energiewende)</div>
              <p className="text-xs leading-relaxed">
                Vroege subsidies hernieuwbaar versus latere energieprijscrisis 2022. <strong>Resultaat:</strong> 2e/3e orde aandeel van industriële keuzes in netbalans. Levert cascade-coëfficiënten voor energie & industrie.
              </p>
            </div>
            <div className="rounded-md border border-slate-200 bg-white p-3">
              <div className="text-[11px] uppercase tracking-widest font-bold text-slate-700 mb-1">🇪🇸 Spanje zelf</div>
              <p className="text-xs leading-relaxed">
                CBS, DNB, CPB-ramingen, sectortabellen werknemersverzekeringen, pensioenfondsen (ABP/PFZW), Nibud-koopkrachtcijfers. Levert de huidige sectorgewichten en absoluut prijsniveau van de elementen.
              </p>
            </div>
          </div>
          <p className="text-xs text-slate-600 italic mt-3">
            <strong>CARB</strong> en <strong>VMP</strong> zijn kleine partijen die volledig doorwerken op systeem-hervorming. VMP-scoring komt volledig uit novademocratia.com; CARB-scoring komt uit openvizier.org en carbon-alert.earth, aangevuld met VMP-waarden waar CARB geen eigen positie heeft. Ze worden verder als normale partijen behandeld.
          </p>
        </div>
      )}

      {tab === 'methode' && (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700 leading-relaxed space-y-3 animate-[fadein_0.3s_ease-out]" data-testid="uitleg-content-methode">
          <p>
            <strong className="text-slate-900">1.</strong> Elke partij heeft een positiematrix over <strong>~180 beleidselementen</strong> (±2 = sterk voor/tegen, ±1 = matig, 0 = neutraal).
          </p>
          <p>
            <strong className="text-slate-900">2.</strong> Elk element heeft een impact-vector over <strong>9 filters</strong>: koopkracht, bedrijvigheid, investeringsklimaat, sociaal vangnet, kwetsbaren, energie, productieve basis, instituties, internationale positie.
          </p>
          <p>
            <strong className="text-slate-900">3.</strong> Jouw profielantwoorden (sector, woning, gezin, leeftijd, regio, enz.) passen <strong>overlays</strong> toe op die filterscores — zodat een huurder andere koopkrachtschade ervaart dan een vermogend gepensioneerde.
          </p>
          <p>
            <strong className="text-slate-900">4.</strong> De 1e-orde score is de directe som over alle filters. De 2e en 3e orde komen via een <strong>9×9 cascade-interactiematrix</strong>: koopkracht-schade zakt door naar bedrijvigheid (consumptie), bedrijvigheid naar investeringsklimaat, instituties naar internationale positie.
          </p>
          <p>
            <strong className="text-slate-900">5.</strong> Een <strong>asymmetrische overshoot-correctie</strong> zorgt dat schade aan instituties (Z-Afrika) en aan productieve basis (Argentinië) zwaarder doorwerkt in 3e orde dan een puur lineair model zou geven. Sparen-eerst beleid wordt mild bestraft in 1e orde maar krijgt 3e-orde herstel; uitgeven-eerst beleid wordt zwaar bestraft in latere ordes.
          </p>
          <p className="text-xs text-slate-600 italic mt-2">
            De Gevolgenkaart geeft <strong>geen stemadvies</strong>. Het is een persoonlijke bijsluiter — onzekerheid neemt toe naar de 3e orde.
          </p>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// SECTOR-KEUZE — kleurig per cluster
// ============================================================================
const CLUSTER_GLOW: Record<string, { ring: string; bg: string; tekst: string; label: string }> = {
  publiek: { ring: 'hover:border-sky-500 hover:bg-sky-100', bg: 'border-sky-300 bg-sky-50', tekst: 'text-sky-700', label: 'Publieke sector' },
  industrie: { ring: 'hover:border-amber-500 hover:bg-amber-100', bg: 'border-amber-300 bg-amber-50', tekst: 'text-amber-700', label: 'Industrie & primair' },
  diensten: { ring: 'hover:border-emerald-500 hover:bg-emerald-100', bg: 'border-emerald-300 bg-emerald-50', tekst: 'text-emerald-700', label: 'Diensten & handel' },
  overig: { ring: 'hover:border-violet-500 hover:bg-violet-100', bg: 'border-violet-300 bg-violet-50', tekst: 'text-violet-700', label: 'Overig' },
};

// Helper: SVG sector-icoon binnen MiniHero
function SectorIconWrap({ iconKey }: { iconKey: string }) {
  const Icon = SECTOR_ICONS[iconKey];
  if (!Icon) return <>•</>;
  return <Icon className="w-8 h-8" />;
}

// Map cluster → hero-accent
const CLUSTER_ACCENT = { publiek: 'sky', industrie: 'amber', diensten: 'emerald', overig: 'violet' } as const;
const CLUSTER_LABEL = { publiek: 'Publieke sector', industrie: 'Industrie & primair', diensten: 'Diensten & handel', overig: 'Overig' };
const CLUSTER_TEKST = { publiek: 'text-sky-700', industrie: 'text-amber-700', diensten: 'text-emerald-700', overig: 'text-violet-700' };

function SectorKeuze({ opties, onKies }: { opties: Record<string, VraagOptie>; onKies: (k: string) => void }) {
  const clusterOrder: Array<'publiek' | 'industrie' | 'diensten' | 'overig'> = ['publiek', 'industrie', 'diensten', 'overig'];
  const perCluster: Record<string, string[]> = {};
  for (const k of Object.keys(opties)) {
    const c = getClusterStyle(k);
    const label = Object.entries(CLUSTER_STYLES).find(([_, v]) => v === c)?.[0] || 'overig';
    if (!perCluster[label]) perCluster[label] = [];
    perCluster[label].push(k);
  }

  return (
    <div className="space-y-5">
      {clusterOrder.map((cluster) => {
        const keys = perCluster[cluster] || [];
        if (keys.length === 0) return null;
        return (
          <div key={cluster}>
            <div className={`text-[10px] uppercase tracking-widest font-bold mb-2 ${CLUSTER_TEKST[cluster]}`}>{CLUSTER_LABEL[cluster]}</div>
            <div className="flex flex-wrap gap-3">
              {keys.map((k) => (
                <MiniHero
                  key={k}
                  icon={<SectorIconWrap iconKey={k} />}
                  label={opties[k].label}
                  accent={CLUSTER_ACCENT[cluster]}
                  size="md"
                  variant="keuze"
                  onClick={() => onKies(k)}
                  testId={`button-Q1_sector-${k}`}
                />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ============================================================================
// KEUZE-LIJST
// ============================================================================
function KeuzeLijst({ vraagId, opties, onKies }: { vraagId: string; opties: Record<string, VraagOptie>; onKies: (k: string) => void }) {
  const accent = accentVoorVraag(vraagId);
  return (
    <div className="flex flex-wrap gap-3">
      {Object.entries(opties).map(([k, v]) => (
        <MiniHero
          key={k}
          icon={iconVoorAntwoord(vraagId, k)}
          label={(v as VraagOptie).label}
          accent={accent}
          size="md"
          variant="keuze"
          onClick={() => onKies(k)}
          testId={`button-${vraagId}-${k}`}
        />
      ))}
    </div>
  );
}

// ============================================================================
// CASCADEBALK — volle kleuren met glow
// ============================================================================
interface CascadeBalkProps {
  rang: number; partijId: string; partijNaam: string; partijKleur: string;
  v1: number; v2: number; v3: number; maxAbs: number;
  orde: '1e' | '2e' | '3e' | 'totaal'; isGekozen: boolean; onClick: () => void;
}
function CascadeBalk({ rang, partijId, partijNaam, partijKleur, v1, v2, v3, maxAbs, orde, isGekozen, onClick }: CascadeBalkProps) {
  const k1 = naarHex(partijKleur);
  const k2 = tintKleur(partijKleur, 0.35);
  const k3 = tintKleur(partijKleur, 0.65);

  const totalNum = orde === '1e' ? v1 : orde === '2e' ? v2 : orde === '3e' ? v3 : v1 + v2 + v3;

  // Schaal: waarde in pct van maxAbs (-100..+100), met factor zodat 50% van maxAbs ~= halve helft van de balk.
  const schaal = (val: number) => Math.max(-100, Math.min(100, (val / maxAbs) * 100));

  // Cumulatieve eindpunten van 1e, 2e, 3e orde (alleen voor 'totaal').
  // De 2e begint waar de 1e eindigt, de 3e waar de 2e eindigt.
  const e1Tot = schaal(v1);
  const e2Tot = schaal(v1 + v2);
  const e3Tot = schaal(v1 + v2 + v3);

  type Seg = { start: number; eind: number; kleur: string; rij: 0 | 1 | 2 };
  const segments: Seg[] = [];
  if (orde === 'totaal') {
    segments.push({ start: 0, eind: e1Tot, kleur: k1, rij: 0 });
    segments.push({ start: e1Tot, eind: e2Tot, kleur: k2, rij: 1 });
    segments.push({ start: e2Tot, eind: e3Tot, kleur: k3, rij: 2 });
  } else if (orde === '1e') {
    segments.push({ start: 0, eind: schaal(v1), kleur: k1, rij: 0 });
  } else if (orde === '2e') {
    segments.push({ start: 0, eind: schaal(v2), kleur: k2, rij: 1 });
  } else {
    segments.push({ start: 0, eind: schaal(v3), kleur: k3, rij: 2 });
  }

  const toCss = (start: number, eind: number) => {
    const a = start / 2;
    const b = eind / 2;
    const left = 50 + Math.min(a, b);
    const width = Math.max(0.6, Math.abs(b - a));
    return { left: `${left}%`, width: `${width}%` };
  };

  const rijTop: Record<0 | 1 | 2, string> = { 0: '4px', 1: '12px', 2: '20px' };

  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 py-1.5 px-2 rounded-lg transition text-left ${
        isGekozen ? 'bg-sky-50 ring-1 ring-sky-200' : 'hover:bg-slate-50'
      }`}
      data-testid={`rank-row-${partijId}`}
      title={`${partijNaam} · 1e ${v1.toFixed(0)} · 2e ${v2.toFixed(0)} · 3e ${v3.toFixed(0)} · ∑ ${(v1+v2+v3).toFixed(0)}`}
    >
      <span className="w-5 text-[11px] text-slate-400 tabular-nums">{rang}</span>
      <span className="w-14 text-sm font-bold tabular-nums" style={{ color: k1, textShadow: `0 0 12px ${k1}55` }}>{partijId}</span>
      <div className="flex-1 relative" style={{ height: '26px' }}>
        {/* Midden-as */}
        <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-300" />
        {/* Drie getrapte rijen */}
        {segments.map((s, i) => {
          const css = toCss(s.start, s.eind);
          return (
            <div
              key={i}
              className="absolute rounded-full transition-all duration-500"
              style={{
                ...css,
                top: rijTop[s.rij],
                height: '3px',
                backgroundColor: s.kleur,
                boxShadow: `0 0 8px ${s.kleur}cc`,
              }}
            />
          );
        })}
      </div>
      <span className={`w-12 text-right text-xs tabular-nums font-bold ${totalNum >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
        {totalNum > 0 ? '+' : ''}{totalNum.toFixed(0)}
      </span>
    </button>
  );
}

// ============================================================================
// UITLEG-PANEEL
// ============================================================================
interface UitlegPaneelProps {
  resultaat: PartijResultaat;
  orde: '1e' | '2e' | '3e' | 'totaal';
  partijMeta: Record<string, { naam?: string; kleur?: string; cluster?: string }>;
  antwoorden: Antwoorden;
  onSluit: () => void;
}
function UitlegPaneel({ resultaat, orde, partijMeta, antwoorden, onSluit }: UitlegPaneelProps) {
  const meta = partijMeta[resultaat.partij_id];
  const kleur = naarHex(meta?.kleur || '');
  const narratief = useMemo(() => maakDuidingNarratief(resultaat, antwoorden, meta?.naam || resultaat.partij_id), [resultaat, antwoorden, meta]);
  const [openElement, setOpenElement] = useState<string | null>(null);
  // Detail-secties op aanvraag tonen
  const [toonCascade, setToonCascade] = useState(false);
  const [toonElementen, setToonElementen] = useState(false);
  const topPos = resultaat.top_positief.filter((b) => b.bijdrage > 0.5).slice(0, 5);
  const topNeg = resultaat.top_negatief.filter((b) => b.bijdrage < -0.5).slice(0, 5);
  const totaal = resultaat.eerste_orde + resultaat.tweede_orde + resultaat.derde_orde;
  const scoreLabel = orde === '1e' ? resultaat.eerste_orde.toFixed(0)
    : orde === '2e' ? resultaat.tweede_orde.toFixed(0)
    : orde === '3e' ? resultaat.derde_orde.toFixed(0)
    : totaal.toFixed(0);

  return (
    <div data-testid={`uitleg-${resultaat.partij_id}`}>
      <div className="flex items-baseline justify-between mb-4 pb-3 border-b border-slate-200">
        <div className="flex items-baseline gap-3">
          <h4 className="text-2xl font-bold" style={{ color: kleur, textShadow: `0 0 20px ${kleur}66` }}>{resultaat.partij_id}</h4>
          <span className="text-sm text-slate-500">{meta?.naam}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm tabular-nums">
            <span className="text-slate-500">{orde === 'totaal' ? '∑' : orde}:</span>{' '}
            <span className={`font-bold ${totaal >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>{scoreLabel}</span>
          </span>
          <button onClick={onSluit} className="text-xs text-slate-500 hover:text-slate-900 transition" data-testid="uitleg-sluit">sluiten ×</button>
        </div>
      </div>

      <p className="text-sm text-slate-700 leading-relaxed mb-5">{narratief.samenvatting}</p>

      {/* Cascade per filter — op aanvraag */}
      <button
        onClick={() => setToonCascade(!toonCascade)}
        className="w-full flex items-center justify-between px-3 py-2 mb-5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 transition"
        data-testid="toggle-cascade"
      >
        <span className="text-xs font-semibold text-slate-200">
          🔍 Gevolg per filter — wat dit veroorzaakt in de 9 dimensies
        </span>
        <span className="text-xs text-slate-400">{toonCascade ? 'verbergen ▴' : 'tonen ▾'}</span>
      </button>
      {toonCascade && <FilterCascade resultaat={resultaat} partijKleur={kleur} />}

      {narratief.beloften.length > 0 && (
        <div className="mb-5">
          <div className="text-[10px] uppercase tracking-widest font-bold text-emerald-700 mb-2">↑ Wat dit voor jou oplevert</div>
          <ul className="space-y-2">
            {narratief.beloften.map((it) => <DuidingRegel key={it.filter_index} item={it} variant="positief" />)}
          </ul>
        </div>
      )}
      {narratief.dreigingen.length > 0 && (
        <div className="mb-5">
          <div className="text-[10px] uppercase tracking-widest font-bold text-rose-700 mb-2">↓ Wat hierbij dreigt</div>
          <ul className="space-y-2">
            {narratief.dreigingen.map((it) => <DuidingRegel key={it.filter_index} item={it} variant="negatief" />)}
          </ul>
        </div>
      )}

      {/* Belangrijkste elementen — op aanvraag */}
      <button
        onClick={() => setToonElementen(!toonElementen)}
        className="w-full flex items-center justify-between px-3 py-2 mt-3 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 transition"
        data-testid="toggle-elementen"
      >
        <span className="text-xs font-semibold text-slate-200">
          📊 Belangrijkste verkiezingsbeloften ({resultaat.aantal_actieve_elementen} actief)
        </span>
        <span className="text-xs text-slate-400">{toonElementen ? 'verbergen ▴' : 'tonen ▾'}</span>
      </button>

      {toonElementen && (
        <div className="mt-3 space-y-3">
          {topPos.length > 0 && (
            <div>
              <div className="text-xs text-emerald-700 font-semibold mb-1.5">Positief voor jou — klik voor details</div>
              <ul className="space-y-1">
                {topPos.map((b) => <ElementRegel key={b.element_id} bijdrage={b} open={openElement === b.element_id} onToggle={() => setOpenElement(openElement === b.element_id ? null : b.element_id)} variant="positief" />)}
              </ul>
            </div>
          )}
          {topNeg.length > 0 && (
            <div>
              <div className="text-xs text-rose-700 font-semibold mb-1.5">Negatief voor jou — klik voor details</div>
              <ul className="space-y-1">
                {topNeg.map((b) => <ElementRegel key={b.element_id} bijdrage={b} open={openElement === b.element_id} onToggle={() => setOpenElement(openElement === b.element_id ? null : b.element_id)} variant="negatief" />)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function DuidingRegel({ item, variant }: { item: DuidingItem; variant: 'positief' | 'negatief' }) {
  const symbol = item.trend === 'kantelt_negatief' ? '⚠' : (item.trend.startsWith('versterkt') || item.trend.startsWith('verbetert') || item.trend.startsWith('stabiel_pos') ? '↑' : '↓');
  const trendKleur = variant === 'positief' ? 'text-emerald-600' : 'text-rose-600';
  const bgKleur = variant === 'positief' ? 'bg-emerald-50 border-emerald-200' : 'bg-rose-50 border-rose-200';
  return (
    <li className={`rounded-lg border px-3 py-2 ${bgKleur}`}>
      <div className="flex gap-3 text-sm">
        <span className={`${trendKleur} font-bold w-4 flex-shrink-0`}>{symbol}</span>
        <div className="flex-1">
          <span className="font-semibold text-slate-900">{item.filter_naam}</span>
          <span className="text-slate-700"> — {item.zin}</span>
          <div className="text-[10px] text-slate-500 tabular-nums mt-1">
            1e {item.v1 > 0 ? '+' : ''}{item.v1} · 2e {item.v2 > 0 ? '+' : ''}{item.v2} · 3e {item.v3 > 0 ? '+' : ''}{item.v3}
          </div>
        </div>
      </div>
    </li>
  );
}

function ElementRegel({ bijdrage, open, onToggle, variant }: { bijdrage: Bijdrage; open: boolean; onToggle: () => void; variant: 'positief' | 'negatief' }) {
  const grouped: Record<string, { vraagLabel: string; antwoordLabel: string; filters: { idx: number; delta: number; reden: string }[] }> = {};
  for (const ob of bijdrage.overlay_bijdragen) {
    if (Math.abs(ob.delta) < 0.1) continue;
    const key = `${ob.vraag_id}::${ob.antwoord_label}`;
    if (!grouped[key]) grouped[key] = { vraagLabel: ob.vraag_label, antwoordLabel: ob.antwoord_label, filters: [] };
    grouped[key].filters.push({ idx: ob.filter_index, delta: ob.delta, reden: ob.reden });
  }
  const positieLabel = bijdrage.positie === 2 ? 'sterk voor' : bijdrage.positie === 1 ? 'voor' : bijdrage.positie === -1 ? 'tegen' : bijdrage.positie === -2 ? 'sterk tegen' : 'neutraal';
  const scoreKleur = variant === 'positief' ? 'text-emerald-600' : 'text-rose-600';

  return (
    <li>
      <button onClick={onToggle} className="w-full flex items-baseline justify-between gap-3 py-1.5 px-2 rounded hover:bg-slate-50 text-left transition" data-testid={`element-toggle-${bijdrage.element_id}`}>
        <span className="text-sm text-slate-700 flex-1">
          {bijdrage.naam}
          <span className="text-[10px] text-slate-500 ml-2">({positieLabel})</span>
        </span>
        <span className={`text-xs tabular-nums font-bold flex-shrink-0 ${scoreKleur}`}>{bijdrage.bijdrage > 0 ? '+' : ''}{bijdrage.bijdrage.toFixed(1)}</span>
      </button>
      {open && (
        <div className="px-3 py-3 bg-slate-50 rounded-lg mt-1 space-y-3 border border-slate-200" data-testid={`element-detail-${bijdrage.element_id}`}>
          <div>
            <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1.5">Filterscores (basis → persoonlijk)</div>
            <div className="grid grid-cols-9 gap-1">
              {bijdrage.basis_scores.map((b, i) => {
                const p = bijdrage.persoonlijk_scores[i];
                const verschil = p - b;
                return (
                  <div key={i} className="text-center bg-white border border-slate-200 rounded py-1" title={getFilterNaam(i)}>
                    <div className="text-[9px] text-slate-500">F{i + 1}</div>
                    <div className="font-mono text-[10px]">
                      <span className="text-slate-500">{b}</span>
                      <span className="text-slate-400">→</span>
                      <span className={verschil === 0 ? 'text-slate-700 font-bold' : verschil > 0 ? 'text-emerald-600 font-bold' : 'text-rose-600 font-bold'}>{p}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {Object.keys(grouped).length > 0 && (
            <div>
              <div className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1.5">Door jouw antwoorden verschoven</div>
              <ul className="space-y-1.5">
                {Object.entries(grouped).map(([key, g]) => (
                  <li key={key} className="bg-white border border-slate-200 rounded px-2 py-1.5">
                    <div className="text-[10px] text-slate-500">{g.vraagLabel}</div>
                    <div className="text-xs font-semibold text-slate-900">{g.antwoordLabel}</div>
                    <div className="text-[10px] mt-1">
                      {g.filters.map((f, i) => (
                        <span key={i} className="mr-2">
                          <span className="text-slate-500">F{f.idx + 1}:</span>{' '}
                          <span className={f.delta > 0 ? 'text-emerald-600 font-bold' : 'text-rose-600 font-bold'}>
                            {f.delta > 0 ? '+' : ''}{f.delta.toFixed(1)}
                          </span>
                        </span>
                      ))}
                    </div>
                    {g.filters[0]?.reden && (
                      <div className="text-[10px] italic text-slate-500 mt-1 leading-snug">{g.filters[0].reden}</div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </li>
  );
}

// ============================================================================
// FILTERCASCADE — per filter de 1e/2e/3e gestapeld in partijkleur
// ============================================================================
function FilterCascade({ resultaat, partijKleur }: { resultaat: PartijResultaat; partijKleur: string }) {
  const [open, setOpen] = useState(false);
  const k1 = naarHex(partijKleur);
  const k2 = tintKleur(partijKleur, 0.35);
  const k3 = tintKleur(partijKleur, 0.65);
  const filterMax = Math.max(1, ...Array.from({ length: 9 }, (_, i) =>
    Math.abs(resultaat.v1[i]) + Math.abs(resultaat.v2[i]) + Math.abs(resultaat.v3[i])
  ));
  const redenen = getFilterInteractieReden();

  return (
    <div className="mb-5 rounded-lg border border-slate-200 bg-slate-50">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-slate-100 transition rounded-t-lg" data-testid="filter-cascade-toggle">
        <span className="text-[10px] uppercase tracking-widest font-bold text-slate-600">Gevolg per filter — wat dit veroorzaakt in de 9 dimensies</span>
        <span className="text-slate-500 text-xs">{open ? '▾' : '▸'}</span>
      </button>
      <div className="px-3 pb-3 space-y-1">
        {Array.from({ length: 9 }, (_, i) => i).map((i) => {
          const v1 = resultaat.v1[i];
          const v2 = resultaat.v2[i];
          const v3 = resultaat.v3[i];
          const fullPct = (val: number) => Math.min(100, (Math.abs(val) / filterMax) * 100 * 2);
          const tot = v1 + v2 + v3;
          const reden = redenen[`F${i + 1}`];
          return (
            <div key={i}>
              <div className="flex items-center gap-2 py-0.5">
                <span className="w-24 text-[10px] text-slate-500 truncate" title={getFilterNaam(i)}>F{i + 1} {getFilterKort(i)}</span>
                <div className="flex-1 relative h-3 bg-slate-200 rounded overflow-hidden">
                  <div className="absolute top-0 bottom-0 left-0 right-1/2 flex flex-row-reverse">
                    {v1 < 0 && <div style={{ width: `${fullPct(v1)}%`, backgroundColor: k1, boxShadow: `0 0 8px ${k1}80` }} className="h-full" />}
                    {v2 < 0 && <div style={{ width: `${fullPct(v2)}%`, backgroundColor: k2 }} className="h-full" />}
                    {v3 < 0 && <div style={{ width: `${fullPct(v3)}%`, backgroundColor: k3 }} className="h-full" />}
                  </div>
                  <div className="absolute top-0 bottom-0 left-1/2 right-0 flex flex-row">
                    {v1 > 0 && <div style={{ width: `${fullPct(v1)}%`, backgroundColor: k1, boxShadow: `0 0 8px ${k1}80` }} className="h-full" />}
                    {v2 > 0 && <div style={{ width: `${fullPct(v2)}%`, backgroundColor: k2 }} className="h-full" />}
                    {v3 > 0 && <div style={{ width: `${fullPct(v3)}%`, backgroundColor: k3 }} className="h-full" />}
                  </div>
                  <div className="absolute left-1/2 top-0 bottom-0 w-px bg-slate-400" />
                </div>
                <span className={`w-10 text-right text-[10px] tabular-nums font-bold ${tot >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {tot > 0 ? '+' : ''}{tot.toFixed(0)}
                </span>
              </div>
              {open && (
                <div className="ml-24 pl-2 py-1 text-[10px] text-slate-500 border-l border-slate-300 leading-snug">
                  <span className="text-slate-500">1e:</span> {v1.toFixed(1)} ·{' '}
                  <span className="text-slate-500">2e:</span> {v2.toFixed(1)} ·{' '}
                  <span className="text-slate-500">3e:</span> {v3.toFixed(1)}
                  {reden && <div className="italic text-slate-500 mt-0.5">{reden}</div>}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
