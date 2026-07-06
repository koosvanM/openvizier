import { useMemo } from 'react';
import personaData from '../data/gevolgenkaart-persona.json';

/**
 * Regel 141 v3.14 — Historische trend NEPK/NTPK (2024/2025/2026)
 *
 * Toont een 3-punts lijngrafiek met NEPK (donker) en NTPK (licht) voor
 * de drie peildata uit persona.json.nepk_tijdreeks.trend.
 *
 * Doel: visuele validatie van consistentie:
 *  - is de trend dalend/stabiel/stijgend zoals verwacht?
 *  - past de helling bij de fase-classificatie?
 *  - klopt de NTPK/NEPK-verhouding (1/φ constant)?
 */

interface TrendPunt {
  jaar: number;
  E_tv_pct: number;
  alpha: number;
  tau: number;
  phi: number;
  nepk_pct: number;
  ntpk_pct: number;
  bron: string;
  status: string;
}

interface Props {
  landLabel?: string;   // "Nederland" / "Deutschland" / "Malta" / "Schweiz"
  taal?: 'nl' | 'de' | 'en';
}

const LABELS = {
  nl: {
    titel: 'Historische aanloop NEPK & NTPK',
    subtitel: 'Drie peildata: 2024, 2025, 2026 — % BBP',
    nepk: 'NEPK (netto)',
    ntpk: 'NTPK (bruto)',
    voetnoot: 'Bron: Vizier-publicaties (klimaatlogica, methodologie-scoreboard, evaluatie-PDF). α en φ constant; E_tv en τ variëren jaar-op-jaar.',
    interpolatie: 'geïnterpoleerd',
  },
  de: {
    titel: 'Historischer Verlauf NEPK & NTPK',
    subtitel: 'Drei Stichtage: 2024, 2025, 2026 — % BIP',
    nepk: 'NEPK (netto)',
    ntpk: 'NTPK (brutto)',
    voetnoot: 'Quelle: Vizier-Publikationen (Klimalogik, Methodologie-Scoreboard, Evaluations-PDF). α und φ konstant; E_tv und τ variieren jährlich.',
    interpolatie: 'interpoliert',
  },
  en: {
    titel: 'Historical trend NEPK & NTPK',
    subtitel: 'Three reference dates: 2024, 2025, 2026 — % GDP',
    nepk: 'NEPK (net)',
    ntpk: 'NTPK (gross)',
    voetnoot: 'Source: Vizier publications (climate-logic, methodology-scoreboard, evaluation-PDF). α and φ constant; E_tv and τ vary year-on-year.',
    interpolatie: 'interpolated',
  },
};

export function HistorischeTrend({ landLabel, taal = 'nl' }: Props) {
  const trend: TrendPunt[] = useMemo(() => {
    const tr = (personaData as any).nepk_tijdreeks?.trend;
    return Array.isArray(tr) && tr.length === 3 ? tr : [];
  }, []);

  const L = LABELS[taal];

  if (trend.length !== 3) {
    return (
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
        {L.titel} — data niet beschikbaar (nepk_tijdreeks.trend ontbreekt of onvolledig).
      </div>
    );
  }

  // SVG layout
  const breedte = 640;
  const hoogte = 240;
  const marge = { top: 32, right: 100, bottom: 40, left: 56 };
  const plotB = breedte - marge.left - marge.right;
  const plotH = hoogte - marge.top - marge.bottom;

  // Y-as: 0 → max(NTPK) + 2, altijd startend op 0 (Regel 141.5)
  const maxNTPK = Math.max(...trend.map(t => t.ntpk_pct));
  const yMax = Math.ceil((maxNTPK + 2) / 2) * 2;
  const yMin = 0;

  // X-as: 3 posities gelijkmatig verdeeld
  function xPx(i: number) { return marge.left + (i / 2) * plotB; }
  function yPx(v: number) {
    return marge.top + plotH - ((v - yMin) / (yMax - yMin)) * plotH;
  }

  const KLEUR_NEPK = '#20808D';   // Nexus chart teal
  const KLEUR_NTPK = '#BCE2E7';   // Nexus chart light cyan (verkleuren voor stroke)
  const KLEUR_NTPK_STROKE = '#5A9AA3';  // donkerder voor betere leesbaarheid

  const padNepk = trend.map((t, i) => `${i === 0 ? 'M' : 'L'}${xPx(i)},${yPx(t.nepk_pct)}`).join(' ');
  const padNtpk = trend.map((t, i) => `${i === 0 ? 'M' : 'L'}${xPx(i)},${yPx(t.ntpk_pct)}`).join(' ');

  // Y-as ticks: 0, geinterpoleerde stappen
  const step = yMax >= 20 ? 5 : yMax >= 10 ? 2 : 1;
  const yTicks: number[] = [];
  for (let v = 0; v <= yMax; v += step) yTicks.push(v);

  return (
    <div className="w-full rounded-lg border border-slate-200 bg-white p-4" data-testid="historische-trend">
      <div className="mb-2">
        <div className="text-sm font-semibold text-slate-800">
          {L.titel}{landLabel ? ` — ${landLabel}` : ''}
        </div>
        <div className="text-xs text-slate-500">{L.subtitel}</div>
      </div>

      <svg viewBox={`0 0 ${breedte} ${hoogte}`} className="w-full h-auto" style={{ maxHeight: 260 }}>
        {/* Horizontale gridlijnen */}
        {yTicks.map(v => (
          <g key={`gy-${v}`}>
            <line x1={marge.left} y1={yPx(v)} x2={breedte - marge.right} y2={yPx(v)}
                  stroke="#e2e8f0" strokeWidth={0.6} />
            <text x={marge.left - 8} y={yPx(v)} fontSize={10} fill="#64748b"
                  textAnchor="end" dy=".33em">{v}%</text>
          </g>
        ))}

        {/* X-as jaar-labels */}
        {trend.map((t, i) => (
          <g key={`gx-${t.jaar}`}>
            <line x1={xPx(i)} y1={marge.top} x2={xPx(i)} y2={marge.top + plotH}
                  stroke="#e2e8f0" strokeWidth={0.4} strokeDasharray="2 3" />
            <text x={xPx(i)} y={marge.top + plotH + 18} fontSize={11} fill="#334155"
                  textAnchor="middle" fontWeight={600}>{t.jaar}</text>
            {t.status === 'interpolatie' && (
              <text x={xPx(i)} y={marge.top + plotH + 32} fontSize={9}
                    fill="#94a3b8" textAnchor="middle" fontStyle="italic">
                {L.interpolatie}
              </text>
            )}
          </g>
        ))}

        {/* Y-as titel */}
        <text x={16} y={marge.top + plotH / 2} fontSize={11} fill="#334155"
              textAnchor="middle" fontWeight={600}
              transform={`rotate(-90 16 ${marge.top + plotH / 2})`}>
          % BBP
        </text>

        {/* NTPK lijn (achterste) */}
        <path d={padNtpk} fill="none" stroke={KLEUR_NTPK_STROKE} strokeWidth={2.2}
              strokeLinecap="round" strokeDasharray="6 3" opacity={0.75} />
        {trend.map((t, i) => (
          <g key={`ntpk-pt-${i}`}>
            <circle cx={xPx(i)} cy={yPx(t.ntpk_pct)} r={4.5}
                    fill="white" stroke={KLEUR_NTPK_STROKE} strokeWidth={2} />
            <text x={xPx(i)} y={yPx(t.ntpk_pct) - 10} fontSize={10}
                  fill={KLEUR_NTPK_STROKE} textAnchor="middle" fontWeight={600}>
              {t.ntpk_pct.toFixed(1)}%
            </text>
          </g>
        ))}

        {/* NEPK lijn (voorste, donker, primair) */}
        <path d={padNepk} fill="none" stroke={KLEUR_NEPK} strokeWidth={3}
              strokeLinecap="round" />
        {trend.map((t, i) => (
          <g key={`nepk-pt-${i}`}>
            <circle cx={xPx(i)} cy={yPx(t.nepk_pct)} r={5.5}
                    fill="white" stroke={KLEUR_NEPK} strokeWidth={2.4} />
            <text x={xPx(i)} y={yPx(t.nepk_pct) + 20} fontSize={11}
                  fill={KLEUR_NEPK} textAnchor="middle" fontWeight={700}>
              {t.nepk_pct.toFixed(1)}%
            </text>
          </g>
        ))}

        {/* Lijn-labels rechts */}
        <text x={breedte - marge.right + 8} y={yPx(trend[2].nepk_pct)}
              fontSize={11} fill={KLEUR_NEPK} fontWeight={700} dy=".3em">
          {L.nepk}
        </text>
        <text x={breedte - marge.right + 8} y={yPx(trend[2].ntpk_pct)}
              fontSize={11} fill={KLEUR_NTPK_STROKE} fontWeight={600} dy=".3em">
          {L.ntpk}
        </text>
      </svg>

      <div className="mt-2 text-[10px] text-slate-500 leading-snug">
        {L.voetnoot}
      </div>
    </div>
  );
}
