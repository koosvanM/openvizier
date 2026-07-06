import { useMemo } from 'react';
import type { NEPKResultaat } from '../lib/levensloopEngine';
import { bundelNEPKLijn, NEPK_BUNDEL_PARTIJEN } from '../lib/levensloopEngine';
import personaData from '../data/gevolgenkaart-persona.json';

/**
 * Regel 116-122 v3.12 — Gezondheidsgrafiek van Spanje
 *
 * ONTWERP-WIJZIGING v3.12b: enkele Y-as in absolute % BBP (0-11%)
 *  — geen dubbele-as-verwarring meer
 *  — alle vier NEPK-varianten (partij, baseline, drempels) op één schaal
 *  — NTPK op zelfde as, boven NEPK
 *  — netto-gezondheid weggelaten als aparte lijn (info in banner onder)
 *  — BBP-index weggelaten uit grafiek (staat als getal in banner)
 *
 * Toont vier lijnen op één Y-as (% BBP):
 *  1. NEPK-partij (partijkleur, dikst)
 *  2. NTPK-partij (groen)
 *  3. Historische baseline NEPK (grijs dashed)
 *  4. Historische baseline NTPK (grijs, lichter dashed)
 * Plus twee horizontale drempellijnen: 3,0% (rood) en 2,0% (donkerrood).
 */

interface Props {
  data: NEPKResultaat;
  partijNaam?: string;
  partijKleur?: string;
}

// Kleuren voor bundel-partijen (mag afwijken van hun matrix-kleur voor duidelijkheid)
const BUNDEL_KLEUREN: Record<string, string> = {
  VMP:       '#eab308',   // goud
  CARB:      '#0891b2',   // cyaan
  VVD:       '#1e40af',   // blauw
  JA21:      '#14b8a6',   // turkoois
  BBB:       '#84cc16',   // groen-geel
  D66:       '#84cc16',   // groen (D66-groen)
  'GL-PvdA': '#dc2626',   // rood
  PVV:       '#facc15',   // geel
  PRO:       '#ec4899',   // magenta
};

// v3.12c — vertaal kleurnamen (uit persona.json) naar hex
// zodat SVG stroke correct rendert.
const NL_KLEUR_HEX: Record<string, string> = {
  'rood':        '#dc2626',
  'blauw':       '#2563eb',
  'donkerblauw': '#1e3a8a',
  'groen':       '#16a34a',
  'oranje':      '#ea580c',
  'geel':        '#facc15',
  'goud':        '#ca8a04',
  'paars':       '#7c3aed',
  'kastanje':    '#7f1d1d',
  'turkoois':    '#0891b2',
  'smaragd':     '#059669',
  'cyaan':       '#06b6d4',
  'roze':        '#ec4899',
  'magenta':     '#d946ef',
  'grijs':       '#64748b',
  'zwart':       '#0f172a',
};

function resolveKleur(input?: string): string {
  if (!input) return '#7c3aed';
  const trimmed = input.trim().toLowerCase();
  if (NL_KLEUR_HEX[trimmed]) return NL_KLEUR_HEX[trimmed];
  // Als het al een hex-code is (#rrggbb of rgb()), retourneer direct
  if (input.startsWith('#') || input.startsWith('rgb')) return input;
  return '#7c3aed';
}

export function GezondheidsgrafiekNL({ data, partijNaam, partijKleur }: Props) {
  const breedte = 900;
  const hoogte = 400;
  const marge = { top: 32, right: 130, bottom: 60, left: 68 };
  const plotB = breedte - marge.left - marge.right;
  const plotH = hoogte - marge.top - marge.bottom;

  // Y-as: absolute % BBP, 0-11
  const yMin = 0;
  const yMax = 11;
  const maxJaar = data.jaren[data.jaren.length - 1];

  function xPx(j: number) { return marge.left + (j / maxJaar) * plotB; }
  function yPx(v: number) {
    const clamped = Math.max(yMin, Math.min(yMax, v));
    return marge.top + plotH - ((clamped - yMin) / (yMax - yMin)) * plotH;
  }

  function padPunten(reeks: number[]): string {
    return data.jaren.map((j, i) => `${i === 0 ? 'M' : 'L'}${xPx(j)},${yPx(reeks[i])}`).join(' ');
  }

  const padNepk = padPunten(data.nepk_pct_bbp);
  const padNtpk = padPunten(data.ntpk_pct_bbp);
  const padNpk = data.npk_pct_bbp ? padPunten(data.npk_pct_bbp) : '';  // v3.20.6
  const padBaseNepk = padPunten(data.baseline_nepk_pct);
  const padBaseNtpk = padPunten(data.baseline_ntpk_pct);

  // Bundel-lijnen berekenen — alle relevante partijen behalve de geselecteerde
  const partijenObj: any = (personaData as any).partijen || {};
  const bundelLijnen = useMemo(() => {
    return NEPK_BUNDEL_PARTIJEN
      .filter(p => p.toUpperCase() !== (data.partij_naam || '').toUpperCase())
      .map(pid => {
        const meta = partijenObj[pid] || {};
        const naam = meta.naam || pid;
        const kleur = BUNDEL_KLEUREN[pid] || '#94a3b8';
        const { nepk } = bundelNEPKLijn(pid, data.jaren.length - 1);
        return { pid, naam, kleur, nepk };
      });
  }, [data.partij_naam, data.jaren.length]);

  // v3.12c: los NL-kleurnamen op naar hex zodat SVG stroke werkt
  const kleur = resolveKleur(partijKleur);
  const KLEUR_NTPK = '#059669';         // groen
  const KLEUR_NPK = '#0891b2';          // v3.20.6: cyan-blauw voor NPK (breder dan NTPK)
  const KLEUR_BASELINE = '#94a3b8';     // grijs
  const KLEUR_GRENS = '#dc2626';        // rood
  const KLEUR_PONR = '#7f1d1d';         // donkerrood
  const KLEUR_START = '#475569';

  const startN = data.startwaarde_pct;
  const startNTPK = data.ntpk_startwaarde_pct;
  const eindNEPK = data.nepk_pct_bbp[data.nepk_pct_bbp.length - 1];
  const eindNTPK = data.ntpk_pct_bbp[data.ntpk_pct_bbp.length - 1];
  const eindBaseNepk = data.baseline_nepk_pct[data.baseline_nepk_pct.length - 1];
  const eindNetto = data.netto_gezondheid_pct_bbp[data.netto_gezondheid_pct_bbp.length - 1];
  const eindjaar = data.kalender_jaren[data.kalender_jaren.length - 1];

  // Y-as ticks: 0, 2 (PONR), 3 (grens), 4, 6, 8, 10
  const yTicks = [0, 2, 3, 4, 6, 8, 10];

  // Drie-orde-samenvatting
  const s = data.drie_orde_scoring;

  const netEffectTekst = useMemo(() => {
    const dNepk = eindNEPK - startN;
    if (Math.abs(dNepk) < 0.15) return 'NEPK blijft vrijwel stabiel (nauwelijks partij-effect)';
    if (dNepk > 0) return `NEPK stijgt met ${dNepk.toFixed(2)} pp BBP (van ${startN.toFixed(2)}% naar ${eindNEPK.toFixed(2)}%)`;
    return `NEPK daalt met ${Math.abs(dNepk).toFixed(2)} pp BBP (van ${startN.toFixed(2)}% naar ${eindNEPK.toFixed(2)}%)`;
  }, [eindNEPK, startN]);

  return (
    <div className="w-full">
      <svg viewBox={`0 0 ${breedte} ${hoogte}`} className="w-full h-auto">
        {/* Kritische zones — donkerrode band 0-2, licht-rode band 2-3 */}
        <rect x={marge.left} y={yPx(2)} width={plotB} height={yPx(0) - yPx(2)}
              fill={KLEUR_PONR} opacity={0.08} />
        <rect x={marge.left} y={yPx(3)} width={plotB} height={yPx(2) - yPx(3)}
              fill={KLEUR_GRENS} opacity={0.06} />

        {/* Horizontale gridlijnen + Y-labels */}
        {yTicks.map(v => (
          <g key={`gy-${v}`}>
            <line x1={marge.left} y1={yPx(v)} x2={breedte - marge.right} y2={yPx(v)}
                  stroke={v === 3 ? KLEUR_GRENS : v === 2 ? KLEUR_PONR : '#e2e8f0'}
                  strokeWidth={v === 2 || v === 3 ? 1.6 : 0.6}
                  strokeDasharray={v === 2 || v === 3 ? '6 4' : undefined}
                  opacity={v === 2 || v === 3 ? 0.85 : 1} />
            <text x={marge.left - 8} y={yPx(v)} fontSize={11}
                  fill={v === 3 ? KLEUR_GRENS : v === 2 ? KLEUR_PONR : '#64748b'}
                  textAnchor="end" dy=".33em"
                  fontWeight={v === 2 || v === 3 ? 700 : 400}>
              {v}%
            </text>
          </g>
        ))}

        {/* Drempel-annotaties — rechts van de plot in de marge */}
        <text x={breedte - marge.right - 6} y={yPx(3) - 4} fontSize={10} fill={KLEUR_GRENS} fontWeight={700} textAnchor="end">
          sociaal kantelpunt — 3,0%
        </text>
        <text x={breedte - marge.right - 6} y={yPx(2) - 4} fontSize={10} fill={KLEUR_PONR} fontWeight={700} textAnchor="end">
          point-of-no-return — 2,0%
        </text>

        {/* X-as jaar-labels */}
        {data.jaren.filter(j => j % 3 === 0).map(j => (
          <g key={`gx-${j}`}>
            <line x1={xPx(j)} y1={marge.top} x2={xPx(j)} y2={marge.top + plotH}
                  stroke="#e2e8f0" strokeWidth={0.5} />
            <text x={xPx(j)} y={marge.top + plotH + 18} fontSize={11} fill="#64748b" textAnchor="middle">
              {data.kalender_jaren[j]}
            </text>
          </g>
        ))}

        {/* Astitels */}
        <text x={20} y={marge.top + plotH / 2} fontSize={12} fill="#334155" textAnchor="middle"
              transform={`rotate(-90 20 ${marge.top + plotH / 2})`} fontWeight={600}>
          Waarde als % van BBP
        </text>
        <text x={marge.left + plotB / 2} y={hoogte - 22} fontSize={11} fill="#334155" textAnchor="middle" fontWeight={600}>
          Kalenderjaar
        </text>

        {/* Startpunt-marker (verticale lijn op 2026) */}
        <line x1={xPx(0)} y1={marge.top} x2={xPx(0)} y2={marge.top + plotH}
              stroke={KLEUR_START} strokeWidth={1} strokeDasharray="2 3" opacity={0.4} />

        {/* Historische baselines — grijs op de achterkant */}
        <path d={padBaseNtpk} fill="none" stroke={KLEUR_BASELINE} strokeWidth={1.5}
              strokeDasharray="2 4" opacity={0.55} />
        <path d={padBaseNepk} fill="none" stroke={KLEUR_BASELINE} strokeWidth={2.0}
              strokeDasharray="4 5" opacity={0.75} />

        {/* Bundel: 8 andere partij-NEPK-lijnen als achtergrond-context.
            Labels rechts worden 'stacked' om overlap te voorkomen: elke label
            krijgt minstens 12px verticale ruimte t.o.v. de vorige. */}
        {(() => {
          // Sorteer op eind-waarde, hoogste eerst
          const gesorteerd = [...bundelLijnen]
            .map(b => ({ ...b, eind: b.nepk[b.nepk.length - 1] }))
            .sort((a, b) => b.eind - a.eind);
          const MIN_SPACING = 11;
          // Bereken y-posities van labels met vertical stacking
          const labelPositions: number[] = [];
          gesorteerd.forEach((b, i) => {
            let y = yPx(b.eind) + 3;
            if (i > 0) {
              const prev = labelPositions[i - 1];
              if (y - prev < MIN_SPACING) y = prev + MIN_SPACING;
            }
            labelPositions.push(y);
          });
          return gesorteerd.map((b, i) => {
            const pad = data.jaren.map((j, k) =>
              `${k === 0 ? 'M' : 'L'}${xPx(j)},${yPx(b.nepk[k])}`).join(' ');
            const labelY = labelPositions[i];
            const trueY = yPx(b.eind);
            return (
              <g key={`bundel-${b.pid}`}>
                <path d={pad} fill="none" stroke={b.kleur} strokeWidth={1.5}
                      strokeLinecap="round" opacity={0.45} />
                {/* Verbinder van eind-punt naar label als ze niet op elkaar liggen */}
                {Math.abs(labelY - trueY) > 2 && (
                  <line x1={xPx(maxJaar)} y1={trueY}
                        x2={xPx(maxJaar) + 3} y2={labelY}
                        stroke={b.kleur} strokeWidth={0.6} opacity={0.4} />
                )}
                <text x={xPx(maxJaar) + 5} y={labelY}
                      fontSize={9} fill={b.kleur} opacity={0.85} fontWeight={600}>
                  {b.pid} {b.eind.toFixed(1)}%
                </text>
              </g>
            );
          });
        })()}

        {/* v3.20.6: NPK-lijn (Nationaal Productief Kapitaal incl. buitenland) — cyan-blauw, dun */}
        {padNpk && (
          <>
            <path d={padNpk} fill="none" stroke={KLEUR_NPK} strokeWidth={2.2}
                  strokeLinecap="round" strokeDasharray="5 3" opacity={0.85} />
            {data.jaren.filter(j => j % 3 === 0).map(j => (
              <circle key={`npk-${j}`} cx={xPx(j)} cy={yPx(data.npk_pct_bbp![j])} r={3.2}
                      fill="white" stroke={KLEUR_NPK} strokeWidth={1.6} />
            ))}
          </>
        )}

        {/* NTPK-partijlijn — groen doorlopend */}
        <path d={padNtpk} fill="none" stroke={KLEUR_NTPK} strokeWidth={2.5}
              strokeLinecap="round" opacity={0.9} />
        {data.jaren.filter(j => j % 3 === 0).map(j => (
          <circle key={`ntpk-${j}`} cx={xPx(j)} cy={yPx(data.ntpk_pct_bbp[j])} r={3.5}
                  fill="white" stroke={KLEUR_NTPK} strokeWidth={1.8} />
        ))}

        {/* NEPK-partijlijn — partijkleur, dikst en vetst, met witte halo eromheen
            zodat de lijn duidelijk boven de bundel uitkomt. */}
        <path d={padNepk} fill="none" stroke="white" strokeWidth={6.5} strokeLinecap="round" opacity={0.9} />
        <path d={padNepk} fill="none" stroke={kleur} strokeWidth={3.6} strokeLinecap="round" />
        {data.jaren.filter(j => j % 3 === 0).map(j => (
          <circle key={`nepk-${j}`} cx={xPx(j)} cy={yPx(data.nepk_pct_bbp[j])} r={5}
                  fill="white" stroke={kleur} strokeWidth={2.6} />
        ))}

        {/* Kantelpunt-marker */}
        {data.jaar_onder_grens && (() => {
          const j = data.jaar_onder_grens - data.kalender_jaren[0];
          if (j < 0 || j > maxJaar) return null;
          return (
            <g>
              <line x1={xPx(j)} y1={marge.top} x2={xPx(j)} y2={marge.top + plotH}
                    stroke={KLEUR_GRENS} strokeWidth={1.5} strokeDasharray="2 3" opacity={0.7} />
              <circle cx={xPx(j)} cy={yPx(3)} r={7} fill={KLEUR_GRENS} stroke="white" strokeWidth={2.5} />
              <text x={xPx(j)} y={marge.top + plotH + 36} fontSize={10} fill={KLEUR_GRENS}
                    textAnchor="middle" fontWeight={700}>
                kantelpunt {data.jaar_onder_grens}
              </text>
            </g>
          );
        })()}

        {/* Point-of-no-return marker */}
        {data.jaar_point_of_no_return && (() => {
          const j = data.jaar_point_of_no_return - data.kalender_jaren[0];
          if (j < 0 || j > maxJaar) return null;
          return (
            <g>
              <circle cx={xPx(j)} cy={yPx(2)} r={6} fill={KLEUR_PONR} stroke="white" strokeWidth={2} />
              <text x={xPx(j)} y={marge.top + plotH + 48} fontSize={9} fill={KLEUR_PONR}
                    textAnchor="middle" fontWeight={700}>
                point-of-no-return {data.jaar_point_of_no_return}
              </text>
            </g>
          );
        })()}

        {/* Eindlabels — rechts naast de lijnen */}
        {data.npk_pct_bbp && (() => {
          const eindNpk = data.npk_pct_bbp[data.npk_pct_bbp.length - 1];
          return (
            <text x={xPx(maxJaar) + 4} y={yPx(eindNpk) + 4}
                  fontSize={11} fill={KLEUR_NPK} fontWeight={700}>
              NPK {eindNpk.toFixed(2)}%
            </text>
          );
        })()}
        <text x={xPx(maxJaar) + 4} y={yPx(eindNTPK) + 4}
              fontSize={11} fill={KLEUR_NTPK} fontWeight={700}>
          NTPK {eindNTPK.toFixed(2)}%
        </text>
        <text x={xPx(maxJaar) + 4} y={yPx(eindNEPK) + 4}
              fontSize={11} fill={kleur} fontWeight={700}>
          NEPK {eindNEPK.toFixed(2)}%
        </text>
        <text x={xPx(maxJaar) + 4} y={yPx(eindBaseNepk) + 4}
              fontSize={9} fill={KLEUR_BASELINE} fontStyle="italic">
          baseline {eindBaseNepk.toFixed(2)}%
        </text>

        {/* Startpunt-label */}
        <text x={marge.left + 6} y={yPx(startN) - 4} fontSize={10} fill={KLEUR_START} fontStyle="italic" fontWeight={600}>
          start 2026: NEPK {startN.toFixed(2)}% · NTPK {startNTPK.toFixed(2)}%
        </text>
        <text x={xPx(maxJaar) - 60} y={marge.top + plotH + 40} fontSize={9} fill="#64748b" textAnchor="end">
          eindjaar {eindjaar}
        </text>
      </svg>

      {/* Legenda */}
      <div className="mt-3 space-y-2 text-xs">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <div className="flex flex-col gap-1.5">
            <span className="flex items-center gap-2">
              <span className="inline-block h-[4px] w-8 rounded-full" style={{ backgroundColor: kleur }} />
              <strong>NEPK</strong> ({partijNaam || data.partij_naam}) — productie binnen Spanje in Spaanse handen (NTPK×φ)
            </span>
            <span className="flex items-center gap-2">
              <span className="inline-block h-[3px] w-8 rounded-full" style={{ backgroundColor: KLEUR_NTPK }} />
              <strong>NTPK</strong> — totale productie binnen Spanje (ongeacht eigenaar)
            </span>
            {data.npk_pct_bbp && (
              <span className="flex items-center gap-2">
                <span className="inline-block h-[2.5px] w-8" style={{ backgroundImage: `repeating-linear-gradient(to right, ${KLEUR_NPK} 0 5px, transparent 5px 8px)` }} />
                <strong>NPK</strong> — alle Spaanse productie wereldwijd, incl. buitenlandse dochters (NTPK×(1+ψ))
              </span>
            )}
          </div>
          <div className="flex flex-col gap-1.5 text-slate-600">
            <span className="flex items-center gap-2">
              <span className="inline-block h-[2px] w-8" style={{ backgroundImage: `repeating-linear-gradient(to right, ${KLEUR_BASELINE} 0 4px, transparent 4px 9px)` }} />
              Historische baseline (zonder ombuiging)
            </span>
            <span>Y-as: % BBP · Formule: NEPK = E<sub>tv</sub> × α × (1−τ) × φ</span>
          </div>
        </div>
        {/* Bundel-legenda */}
        <div className="pt-2 border-t border-slate-100">
          <div className="text-[11px] text-slate-500 mb-1.5">Vergelijkingsbundel (dunne lijnen, alle op zelfde as — rechts eind-label):</div>
          <div className="flex flex-wrap gap-x-3 gap-y-1">
            {bundelLijnen.map(({ pid, kleur: bKleur }) => (
              <span key={pid} className="flex items-center gap-1 text-[11px]">
                <span className="inline-block h-[2px] w-4" style={{ backgroundColor: bKleur, opacity: 0.75 }} />
                <span style={{ color: bKleur }}>{pid}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Netto-gezondheid als banner (i.p.v. lijn) */}
      <div className="mt-3 rounded-lg border border-slate-200 bg-white p-3 text-xs">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div>
            <strong className="text-slate-800">Netto-gezondheid eindjaar {eindjaar}:</strong>{' '}
            <span className={eindNetto < 3 ? 'text-red-700 font-bold' : eindNetto < 4 ? 'text-amber-700 font-bold' : 'text-emerald-700 font-bold'}>
              {eindNetto.toFixed(2)}% BBP
            </span>
            <span className="text-slate-500 ml-2">(= NEPK − schuld-service − uitmergel-drift)</span>
          </div>
          <div className="text-slate-500 text-[11px]">
            {netEffectTekst}
          </div>
        </div>
      </div>

      {/* Drie-orde-tabel */}
      <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50/60 p-3">
        <div className="text-xs font-bold text-slate-800 mb-2">
          Drie-orde-modulatie ({partijNaam || data.partij_naam}) — pp per jaar per factor
        </div>
        <table className="w-full text-[11px]">
          <thead>
            <tr className="border-b border-slate-300">
              <th className="text-left py-1 font-semibold">Factor</th>
              <th className="text-right px-2 py-1 font-semibold text-slate-600">1e orde<br/>(j 1-3)</th>
              <th className="text-right px-2 py-1 font-semibold text-slate-600">2e orde<br/>(j 4-8)</th>
              <th className="text-right px-2 py-1 font-semibold text-slate-600">3e orde<br/>(j 9-15)</th>
              <th className="text-right px-2 py-1 font-semibold text-slate-800">Cum. 15j</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-slate-200">
              <td className="py-1"><strong>E<sub>tv</sub></strong> (export-VA % BBP)</td>
              <td className="text-right px-2 tabular-nums">{s.E_tv.orde1 >= 0 ? '+' : ''}{s.E_tv.orde1.toFixed(3)}</td>
              <td className="text-right px-2 tabular-nums">{s.E_tv.orde2 >= 0 ? '+' : ''}{s.E_tv.orde2.toFixed(3)}</td>
              <td className="text-right px-2 tabular-nums">{s.E_tv.orde3 >= 0 ? '+' : ''}{s.E_tv.orde3.toFixed(3)}</td>
              <td className="text-right px-2 tabular-nums font-bold" style={{ color: s.E_tv.cumulatief_15j >= 0 ? '#059669' : '#dc2626' }}>
                {s.E_tv.cumulatief_15j >= 0 ? '+' : ''}{s.E_tv.cumulatief_15j.toFixed(2)} pp
              </td>
            </tr>
            <tr className="border-b border-slate-200">
              <td className="py-1"><strong>α</strong> (productieve kern)</td>
              <td className="text-right px-2 tabular-nums">{s.alpha.orde1 >= 0 ? '+' : ''}{s.alpha.orde1.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums">{s.alpha.orde2 >= 0 ? '+' : ''}{s.alpha.orde2.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums">{s.alpha.orde3 >= 0 ? '+' : ''}{s.alpha.orde3.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums font-bold" style={{ color: s.alpha.cumulatief_15j >= 0 ? '#059669' : '#dc2626' }}>
                {s.alpha.cumulatief_15j >= 0 ? '+' : ''}{s.alpha.cumulatief_15j.toFixed(3)}
              </td>
            </tr>
            <tr className="border-b border-slate-200">
              <td className="py-1"><strong>τ</strong> (collectieve lasten)</td>
              <td className="text-right px-2 tabular-nums">{s.tau.orde1 >= 0 ? '+' : ''}{s.tau.orde1.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums">{s.tau.orde2 >= 0 ? '+' : ''}{s.tau.orde2.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums">{s.tau.orde3 >= 0 ? '+' : ''}{s.tau.orde3.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums font-bold" style={{ color: s.tau.cumulatief_15j <= 0 ? '#059669' : '#dc2626' }}>
                {s.tau.cumulatief_15j >= 0 ? '+' : ''}{s.tau.cumulatief_15j.toFixed(3)}
              </td>
            </tr>
            <tr>
              <td className="py-1"><strong>φ</strong> (nationaal eigendom)</td>
              <td className="text-right px-2 tabular-nums">{s.phi.orde1 >= 0 ? '+' : ''}{s.phi.orde1.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums">{s.phi.orde2 >= 0 ? '+' : ''}{s.phi.orde2.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums">{s.phi.orde3 >= 0 ? '+' : ''}{s.phi.orde3.toFixed(4)}</td>
              <td className="text-right px-2 tabular-nums font-bold" style={{ color: s.phi.cumulatief_15j >= 0 ? '#059669' : '#dc2626' }}>
                {s.phi.cumulatief_15j >= 0 ? '+' : ''}{s.phi.cumulatief_15j.toFixed(3)}
              </td>
            </tr>
          </tbody>
        </table>
        <div className="mt-2 text-[10px] text-slate-600 leading-tight">
          Voor <strong>τ</strong> geldt: negatief = lastenverlaging (gunstig voor NEPK). Groen = NEPK-versterkend, rood = NEPK-verzwakkend.
        </div>
      </div>

      {/* Waarschuwingsbanners */}
      {data.jaar_onder_grens && (
        <div className="mt-3 rounded-lg border border-red-200 bg-red-50/60 p-3 text-xs text-slate-700">
          <strong className="text-red-700">Sociaal kantelpunt bereikt in {data.jaar_onder_grens}:</strong>{' '}
          NEPK zakt onder 3,0% BBP. Historisch valt zo'n daling samen met
          groeiende sociale spanning tussen bezittenden en niet-bezittenden — zoals in Frankrijk 2023-2026.
        </div>
      )}
      {data.jaar_point_of_no_return && (
        <div className="mt-3 rounded-lg border border-red-300 bg-red-100/60 p-3 text-xs text-slate-800">
          <strong className="text-red-800">Point-of-no-return in {data.jaar_point_of_no_return}:</strong>{' '}
          NEPK zakt onder 2,0% BBP. Onder dit niveau is herstel binnen een menselijke tijdshorizon onwaarschijnlijk.
        </div>
      )}
      {data.jaar_uitmergel_intreedt && (
        <div className="mt-3 rounded-lg border border-amber-300 bg-amber-50/60 p-3 text-xs text-slate-700">
          <strong className="text-amber-800">Uitmergel-fase in {data.jaar_uitmergel_intreedt}:</strong>{' '}
          Schuld-service kruist de 5%-BBP-drempel — rente en aflossing krijgen voorrang op lokale prioriteiten.
        </div>
      )}
    </div>
  );
}
