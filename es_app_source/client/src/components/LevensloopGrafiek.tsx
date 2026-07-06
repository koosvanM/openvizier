import { useMemo, useState } from 'react';
import type { LevensloopResultaat } from '../lib/levensloopEngine';

interface Props {
  data: LevensloopResultaat;
  partijMeta: Record<string, { naam?: string; kleur?: string; leverbaarheid?: number; leverbaarheid_label?: string }>;
  // Regel 105 v3.9: aparte toggles voor VMP en CARB, standaard uit
  toonVMP?: boolean;
  toonCARB?: boolean;
}

const KLEUR_ADVIES   = '#0ea5e9'; // lichtblauw
const KLEUR_EIGEN    = '#a855f7'; // paars
const KLEUR_HERKEUZE = '#16a34a'; // groen
const KLEUR_NEPK     = '#c2410c'; // roodbruin/terra — landsniveau: productieve kern (F1+F2+F3)
const KLEUR_VMP      = '#0891b2'; // donkercyaan
const KLEUR_CARB     = '#ea580c'; // oranje
const KLEUR_DRIFT    = '#94a3b8'; // slate — nullijn/baseline-drift

const FASE_LABEL: Record<string, string> = {
  student: 'student',
  starter: 'starter',
  midcarriere: 'midcarrière',
  senior: 'senior',
  preret: 'pre-pensioen',
  pensioen: 'pensioen',
};

export function LevensloopGrafiek({ data, partijMeta, toonVMP = false, toonCARB = false }: Props) {
  const [tooltip, setTooltip] = useState<{ x: number; y: number; jaar: number } | null>(null);

  // SVG-coordinaten + schaal
  const breedte = 820;
  const hoogte = 380;
  const marge = { top: 28, right: 80, bottom: 40, left: 56 };
  const plotB = breedte - marge.left - marge.right;
  const plotH = hoogte - marge.top - marge.bottom;

  // Schaal krapper trekken: kleinere padding rond de werkelijke data,
  // stap-grootte 10 i.p.v. 50, en bodem/plafond dichter bij de echte extremen.
  // Regel 105 v3.9 — vaste Y-as 80–120.
  // Buiten dit venster is het beleidsinhoudelijk niet meer interessant:
  // ±20% t.o.v. huidige koopkracht dekt alle realiëele 15-jaars-effecten van
  // Nederlandse politieke keuzes plus de structurele drift. VMP/CARB en
  // eventuele extreme partijcurves worden bij de plotrand geclipt met een
  // caret-indicator, zodat de vergelijking tussen partijen niet verstoord
  // wordt door theoretische ijkpunten.
  // Regel v3.20.24 — Y-as uitgebreid naar 300 voor CARB kwadratisch profiel
  // BiCRS-narratief geeft NTPK j15 +141% → inkomensindex ~280
  // Advies/eigen/herkeuze bewegen historisch 85-115; VMP-referentie ~125; CARB nu tot ~280
  // Bij buiten-bereik-waarden worden lijnen geclamped en gemarkeerd met driehoek/pijl
  const maxY = 300;
  const minY = 80;

  const maxJaar = data.jaren[data.jaren.length - 1];

  function xPx(jaar: number) { return marge.left + (jaar / maxJaar) * plotB; }
  function yPx(idx: number) { return marge.top + plotH - ((idx - minY) / (maxY - minY)) * plotH; }
  // Regel 105 v3.9: clamp-versie voor VMP/CARB — klemt bij plotrand met caret-indicator.
  function yPxClamp(idx: number): { y: number; buiten: 'boven' | 'onder' | null } {
    if (idx > maxY) return { y: marge.top + 2, buiten: 'boven' };
    if (idx < minY) return { y: marge.top + plotH - 2, buiten: 'onder' };
    return { y: yPx(idx), buiten: null };
  }

  function pad(xs: number[], ys: number[]) {
    return xs.map((x, i) => `${i === 0 ? 'M' : 'L'}${xPx(x)},${yPx(ys[i])}`).join(' ');
  }
  function bandPad(xs: number[], onder: number[], boven: number[]) {
    const top = xs.map((x, i) => `${i === 0 ? 'M' : 'L'}${xPx(x)},${yPx(boven[i])}`).join(' ');
    const bot = xs.slice().reverse().map(x => {
      const idx = xs.indexOf(x);
      return `L${xPx(x)},${yPx(onder[idx])}`;
    }).join(' ');
    return `${top} ${bot} Z`;
  }

  const baselineY = yPx(100);
  const adviesNaam = data.start_partij_advies;
  const eigenNaam = data.start_partij_eigen;
  const heeftHerkeuze = data.herkeuzes.length > 0;
  const lev_advies = partijMeta[adviesNaam];
  const lev_eigen = partijMeta[eigenNaam];

  return (
    <div className="w-full" data-testid="levensloop-grafiek">
      <svg viewBox={`0 0 ${breedte} ${hoogte}`} className="w-full h-auto" style={{ maxHeight: 460 }}>
        {/* Y-as ticks */}
        {[minY, 100, maxY, Math.round((minY+maxY)/2)].filter((v, i, a) => a.indexOf(v) === i).map(v => (
          <g key={v}>
            <line x1={marge.left} y1={yPx(v)} x2={breedte - marge.right} y2={yPx(v)} stroke="#e2e8f0" strokeWidth={0.5} />
            <text x={marge.left - 8} y={yPx(v)} fontSize={11} fill="#64748b" textAnchor="end" dy=".3em">{v}</text>
          </g>
        ))}
        {/* X-as ticks */}
        {data.jaren.filter(j => j % Math.max(1, Math.floor(maxJaar/12)) === 0).map(j => (
          <g key={j}>
            <line x1={xPx(j)} y1={marge.top + plotH} x2={xPx(j)} y2={marge.top + plotH + 4} stroke="#94a3b8" strokeWidth={0.8} />
            <text x={xPx(j)} y={marge.top + plotH + 18} fontSize={10} fill="#64748b" textAnchor="middle">{j}</text>
          </g>
        ))}
        <text x={marge.left + plotB / 2} y={hoogte - 6} fontSize={11} fill="#475569" textAnchor="middle">Jaar</text>
        <text x={12} y={marge.top + plotH / 2} fontSize={11} fill="#475569" textAnchor="middle" transform={`rotate(-90 12 ${marge.top + plotH / 2})`}>Inkomensindex (jaar 0 = 100)</text>

        {/* Vlakke 100-referentielijn ("vandaag") */}
        <line x1={marge.left} y1={baselineY} x2={breedte - marge.right} y2={baselineY}
              stroke="#475569" strokeWidth={1} strokeDasharray="3 4" opacity={0.4} />
        <text x={marge.left + 4} y={baselineY - 4} fontSize={9} fill="#475569" textAnchor="start" fontStyle="italic">100 = vandaag</text>

        {/* Regel 103 v3.9: dalende Nullijn / baseline-drift van NL */}
        {(data as any).baseline_drift?.drift_index && (
          <>
            <path d={pad(data.jaren, (data as any).baseline_drift.drift_index)} fill="none" stroke={KLEUR_DRIFT}
                  strokeWidth={1.8} strokeLinecap="round" strokeDasharray="6 4" opacity={0.85} />
            <text x={breedte - marge.right + 4}
                  y={yPx((data as any).baseline_drift.drift_index[(data as any).baseline_drift.drift_index.length - 1])}
                  fontSize={10} fill={KLEUR_DRIFT} dy=".3em" fontWeight={600}>
              Nullijn
            </text>
          </>
        )}

        {/* Onzekerheidsbanden */}
        <path d={bandPad(data.jaren, data.band_advies_onder, data.band_advies_boven)}
              fill={KLEUR_ADVIES} opacity={0.10} />
        {heeftHerkeuze && (
          <path d={bandPad(data.jaren, data.band_herkeuze_onder, data.band_herkeuze_boven)}
                fill={KLEUR_HERKEUZE} opacity={0.10} />
        )}

        {/* Verticale stippels op herkeuzemomenten */}
        {data.herkeuzes.map((h, i) => (
          <line key={i} x1={xPx(h.jaar)} y1={marge.top} x2={xPx(h.jaar)} y2={marge.top + plotH}
                stroke="#cbd5e1" strokeWidth={1} strokeDasharray="2 3" />
        ))}

        {/* Lijnen */}
        <path d={pad(data.jaren, data.advies_index)} fill="none" stroke={KLEUR_ADVIES}
              strokeWidth={2.4} strokeLinecap="round" />
        <path d={pad(data.jaren, data.eigen_index)} fill="none" stroke={KLEUR_EIGEN}
              strokeWidth={2.4} strokeLinecap="round" />
        {heeftHerkeuze && (
          <path d={pad(data.jaren, data.herkeuze_index)} fill="none" stroke={KLEUR_HERKEUZE}
                strokeWidth={2.4} strokeLinecap="round" strokeDasharray="6 4" />
        )}
        {/* NEPK-lijn: landsniveau, F1+F2+F3 gewogen cascade van eigen partij */}
        {data.nepk_eigen_index && (
          <path d={pad(data.jaren, data.nepk_eigen_index)} fill="none" stroke={KLEUR_NEPK}
                strokeWidth={2} strokeLinecap="round" strokeDasharray="2 3" opacity={0.85} />
        )}

        {/* Regel 105 v3.9: VMP-referentielijn — alleen bij toggle, geclampt bij plotrand */}
        {toonVMP && data.vmp_index && (() => {
          const clamped = data.jaren.map(j => yPxClamp(data.vmp_index[j]));
          const dpath = data.jaren.map((j, i) => `${i === 0 ? 'M' : 'L'}${xPx(j)},${clamped[i].y}`).join(' ');
          const laatste = clamped[clamped.length - 1];
          return (
            <>
              <path d={dpath} fill="none" stroke={KLEUR_VMP}
                    strokeWidth={2} strokeLinecap="round" strokeDasharray="4 2" opacity={0.9} />
              {data.jaren.filter(j => j % 3 === 0).map(j => (
                <circle key={`vmp-${j}`} cx={xPx(j)} cy={yPxClamp(data.vmp_index[j]).y} r={3} fill={KLEUR_VMP} stroke="white" strokeWidth={1.2} />
              ))}
              <text x={breedte - marge.right + 4} y={laatste.y}
                    fontSize={10} fill={KLEUR_VMP} dy=".3em" fontWeight={600}>
                VMP {laatste.buiten === 'boven' ? '▲' : laatste.buiten === 'onder' ? '▼' : ''}
              </text>
            </>
          );
        })()}

        {/* Regel 105 v3.9: CARB-referentielijn — alleen bij toggle, geclampt bij plotrand */}
        {toonCARB && data.carb_index && (() => {
          const clamped = data.jaren.map(j => yPxClamp(data.carb_index[j]));
          const dpath = data.jaren.map((j, i) => `${i === 0 ? 'M' : 'L'}${xPx(j)},${clamped[i].y}`).join(' ');
          const laatste = clamped[clamped.length - 1];
          return (
            <>
              <path d={dpath} fill="none" stroke={KLEUR_CARB}
                    strokeWidth={2} strokeLinecap="round" strokeDasharray="6 2" opacity={0.9} />
              {data.jaren.filter(j => j % 3 === 0).map(j => (
                <circle key={`carb-${j}`} cx={xPx(j)} cy={yPxClamp(data.carb_index[j]).y} r={3} fill={KLEUR_CARB} stroke="white" strokeWidth={1.2} />
              ))}
              <text x={breedte - marge.right + 4} y={laatste.y}
                    fontSize={10} fill={KLEUR_CARB} dy=".3em" fontWeight={600}>
                CARB {laatste.buiten === 'boven' ? '▲' : laatste.buiten === 'onder' ? '▼' : ''}
              </text>
            </>
          );
        })()}

        {/* Markers per jaar */}
        {data.jaren.map(j => (
          <g key={`m-${j}`}>
            {/* Advies: cirkel */}
            <circle cx={xPx(j)} cy={yPx(data.advies_index[j])} r={3.5} fill="white" stroke={KLEUR_ADVIES} strokeWidth={1.6} />
            {/* Eigen: vierkant */}
            <rect x={xPx(j) - 3} y={yPx(data.eigen_index[j]) - 3} width={6} height={6} fill="white" stroke={KLEUR_EIGEN} strokeWidth={1.6} />
            {/* Herkeuze: driehoek */}
            {heeftHerkeuze && (
              <polygon points={`${xPx(j)},${yPx(data.herkeuze_index[j])-4} ${xPx(j)-3.5},${yPx(data.herkeuze_index[j])+3} ${xPx(j)+3.5},${yPx(data.herkeuze_index[j])+3}`}
                       fill="white" stroke={KLEUR_HERKEUZE} strokeWidth={1.6} />
            )}
          </g>
        ))}

        {/* Start-pins: advies en eigen */}
        <circle cx={xPx(0) + 4} cy={baselineY} r={8} fill={KLEUR_ADVIES} stroke="white" strokeWidth={2.5} />
        <text x={xPx(0) + 4} y={baselineY - 14} fontSize={11} fontWeight={700} fill={KLEUR_ADVIES} textAnchor="middle">{adviesNaam}</text>
        {eigenNaam !== adviesNaam && (
          <>
            <circle cx={xPx(0) + 28} cy={baselineY} r={8} fill={KLEUR_EIGEN} stroke="white" strokeWidth={2.5} />
            <text x={xPx(0) + 28} y={baselineY - 14} fontSize={11} fontWeight={700} fill={KLEUR_EIGEN} textAnchor="middle">{eigenNaam}</text>
          </>
        )}

        {/* Herkeuze-pins */}
        {data.herkeuzes.map((h, i) => (
          <g key={`h-${i}`}>
            <circle cx={xPx(h.jaar)} cy={yPx(data.herkeuze_index[h.jaar])} r={9} fill={KLEUR_HERKEUZE} stroke="white" strokeWidth={2.5} />
            <text x={xPx(h.jaar)} y={yPx(data.herkeuze_index[h.jaar]) - 14} fontSize={11} fontWeight={700} fill={KLEUR_HERKEUZE} textAnchor="middle">{h.naar_partij}</text>
            <text x={xPx(h.jaar)} y={yPx(data.herkeuze_index[h.jaar]) + 22} fontSize={9} fill="#64748b" textAnchor="middle" fontStyle="italic">jaar {h.jaar} · {FASE_LABEL[h.nieuwe_fase] || h.nieuwe_fase}</text>
          </g>
        ))}
      </svg>

      {/* Legenda + leverbaarheid */}
      <div className="mt-3 flex flex-wrap items-start justify-between gap-3 text-xs">
        <div className="flex flex-wrap gap-4 items-center">
          <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: KLEUR_ADVIES }} /> Computer-advies: <strong>{adviesNaam}</strong></span>
          <span className="flex items-center gap-1.5"><span className="inline-block w-3 h-3 rounded-sm" style={{ backgroundColor: KLEUR_EIGEN }} /> Eigen keuze: <strong>{eigenNaam}</strong></span>
          {heeftHerkeuze && (
            <span className="flex items-center gap-1.5"><span className="inline-block w-0 h-0" style={{ borderLeft: '5px solid transparent', borderRight: '5px solid transparent', borderBottom: `7px solid ${KLEUR_HERKEUZE}` }} /> Herkozen bij elke sprong</span>
          )}
          {data.nepk_eigen_index && (
            <span className="flex items-center gap-1.5" title="Productieve kern van de nationale economie: F1 NEPK + F2 Bedrijvigheid + F3 Investeringsklimaat, gewogen cascade van de eigen partij.">
              <span className="inline-block h-[2px] w-4" style={{ backgroundImage: `repeating-linear-gradient(to right, ${KLEUR_NEPK} 0 3px, transparent 3px 6px)` }} />
              NEPK Spanje: <strong>{eigenNaam}</strong>
            </span>
          )}
        </div>
        <div className="flex flex-col items-end gap-0.5 text-[10px] text-slate-500">
          {lev_advies?.leverbaarheid !== undefined && (
            <span>uitvoeringskracht <strong style={{ color: KLEUR_ADVIES }}>{adviesNaam}</strong>: {Math.round(lev_advies.leverbaarheid * 100)}% — {lev_advies.leverbaarheid_label}</span>
          )}
          {eigenNaam !== adviesNaam && lev_eigen?.leverbaarheid !== undefined && (
            <span>uitvoeringskracht <strong style={{ color: KLEUR_EIGEN }}>{eigenNaam}</strong>: {Math.round(lev_eigen.leverbaarheid * 100)}% — {lev_eigen.leverbaarheid_label}</span>
          )}
        </div>
      </div>
    </div>
  );
}
