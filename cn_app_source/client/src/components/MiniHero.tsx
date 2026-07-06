// Mini-hero: 150×150 gekleurde tegel met icoon + label voor een keuze
// Wordt zowel gebruikt als KEUZE in de vraag, als TROFEE in het profielblok na keuze
import type { ReactNode } from 'react';

export type HeroAccent = 'sky' | 'amber' | 'emerald' | 'violet' | 'rose' | 'cyan' | 'fuchsia';

const ACCENT_STYLES: Record<HeroAccent, { bg: string; bgActive: string; border: string; tekst: string; tekstLabel: string; glow: string }> = {
  sky:     { bg: 'from-sky-50 to-white',     bgActive: 'from-sky-100 to-sky-50',     border: 'border-sky-300',     tekst: 'text-sky-700',     tekstLabel: 'text-sky-900',     glow: 'shadow-sky-300/50' },
  amber:   { bg: 'from-amber-50 to-white',   bgActive: 'from-amber-100 to-amber-50', border: 'border-amber-300', tekst: 'text-amber-700',   tekstLabel: 'text-amber-900',   glow: 'shadow-amber-300/50' },
  emerald: { bg: 'from-emerald-50 to-white', bgActive: 'from-emerald-100 to-emerald-50', border: 'border-emerald-300', tekst: 'text-emerald-700', tekstLabel: 'text-emerald-900', glow: 'shadow-emerald-300/50' },
  violet:  { bg: 'from-violet-50 to-white',  bgActive: 'from-violet-100 to-violet-50',  border: 'border-violet-300',  tekst: 'text-violet-700',  tekstLabel: 'text-violet-900',  glow: 'shadow-violet-300/50' },
  rose:    { bg: 'from-rose-50 to-white',    bgActive: 'from-rose-100 to-rose-50',    border: 'border-rose-300',    tekst: 'text-rose-700',    tekstLabel: 'text-rose-900',    glow: 'shadow-rose-300/50' },
  cyan:    { bg: 'from-cyan-50 to-white',    bgActive: 'from-cyan-100 to-cyan-50',    border: 'border-cyan-300',    tekst: 'text-cyan-700',    tekstLabel: 'text-cyan-900',    glow: 'shadow-cyan-300/50' },
  fuchsia: { bg: 'from-fuchsia-50 to-white', bgActive: 'from-fuchsia-100 to-fuchsia-50', border: 'border-fuchsia-300', tekst: 'text-fuchsia-700', tekstLabel: 'text-fuchsia-900', glow: 'shadow-fuchsia-300/50' },
};

interface MiniHeroProps {
  icon: ReactNode;       // icoon/emoji/SVG
  label: string;         // korte label
  sublabel?: string;     // kleine ondertekst (bv. categorie/vraag)
  accent: HeroAccent;
  size?: 'sm' | 'md';    // sm=110 (profielblok), md=150 (keuze)
  variant?: 'keuze' | 'trofee';  // keuze=onaangeklikt, trofee=gekozen
  onClick?: () => void;
  onWissen?: () => void;
  testId?: string;
}

export function MiniHero({ icon, label, sublabel, accent, size = 'md', variant = 'keuze', onClick, onWissen, testId }: MiniHeroProps) {
  const stijl = ACCENT_STYLES[accent];
  const dim = size === 'md' ? 'w-[150px] h-[150px]' : 'w-[110px] h-[110px]';
  const padding = size === 'md' ? 'px-2 py-2.5' : 'px-1.5 py-2';
  const iconSize = size === 'md' ? 'text-[26px]' : 'text-xl';
  const labelSize = size === 'md' ? 'text-[12px]' : 'text-[10px]';

  const innerBg = variant === 'trofee' ? stijl.bgActive : stijl.bg;
  const shadow = variant === 'trofee' ? `shadow-lg ${stijl.glow}` : 'hover:shadow-md hover:scale-[1.03]';

  return (
    <div className={`relative ${dim} flex-shrink-0`}>
      <button
        onClick={onClick}
        className={`w-full h-full rounded-xl border-2 ${stijl.border} bg-gradient-to-br ${innerBg} ${padding} flex flex-col items-center justify-center gap-1.5 text-center transition-all ${shadow} ${variant === 'keuze' ? 'cursor-pointer' : 'cursor-default'}`}
        data-testid={testId}
        disabled={!onClick}
      >
        {sublabel && (
          <span className={`text-[9px] uppercase tracking-widest font-bold ${stijl.tekst} opacity-80`}>
            {sublabel}
          </span>
        )}
        <span className={`${iconSize} ${stijl.tekst} leading-none`}>{icon}</span>
        <span className={`${labelSize} font-semibold ${stijl.tekstLabel} leading-[1.15] break-words hyphens-auto`} style={{ wordBreak: 'break-word' }}>{label}</span>
      </button>
      {variant === 'trofee' && onWissen && (
        <button
          onClick={(e) => { e.stopPropagation(); onWissen(); }}
          className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-white border border-slate-300 text-slate-500 shadow-sm hover:bg-rose-500 hover:text-white hover:border-rose-500 text-xs flex items-center justify-center transition"
          data-testid={`${testId}-wissen`}
          title="wissen"
        >
          ×
        </button>
      )}
    </div>
  );
}

// Hulp: bepaal de accent-kleur per vraag
export function accentVoorVraag(vraagId: string): HeroAccent {
  return ({
    Q1_sector: 'sky',
    Q2_wonen: 'amber',
    Q3_gezin: 'emerald',
    Q4_leeftijd: 'violet',
    Q5_regio: 'rose',
    Q6_bedrijfslaag: 'cyan',
    Q7_netwerk: 'fuchsia',
  } as Record<string, HeroAccent>)[vraagId] || 'sky';
}

// Hulp: kies een icoon (emoji) per antwoord
export function iconVoorAntwoord(vraagId: string, antwoordKey: string): string {
  const map: Record<string, string> = {
    // Q2 wonen — NL-sleutels
    huurder_schuld: '🏚️', huurder_spaarder: '🏘️', starter_koper: '🔑',
    koper_aflossend: '🏠', vermogend_koper: '🏡',
    // Q2 wonen — ES-sleutels
    huurder_zonder_buffer: '🏚️', huurder_met_buffer: '🏘️',
    starter_op_koopmarkt: '🔑', huiseigenaar_aflossend: '🏠',
    huiseigenaar_afbetaald: '🏡',
    // Q3 gezin — NL-sleutels
    alleenstaand: '🧍', koppel_zonder_kinderen: '👥',
    gezin_kinderen: '👨‍👩‍👧', eenoudergezin: '👩‍👧',
    // Q3 gezin — ES-sleutels
    alleen: '🧍', paar_zonder_kinderen: '👥',
    paar_met_kinderen: '👨‍👩‍👧', eenouder: '👩‍👧',
    meergeneraties: '👨‍👩‍👧‍👦',
    // Q4 leeftijd — NL-sleutels
    onder_30: '🌱', '30_tot_50': '💼', '50_tot_67': '⚓', '67_plus': '🎩',
    // Q4 leeftijd — ES-sleutels
    jong: '🌱', werkend_jong: '💼', werkend_ouder: '⚓',
    pre_pensioen: '🎩', senior: '🧓',
    // Q5 regio — NL-sleutels
    randstad: '🏙️', middenstad: '🏘️', krimpregio: '🌾', grensregio: '🛤️',
    // Q5 regio — ES-sleutels
    grote_stad: '🏘️', kleine_gemeente: '🏠',
    // Q6 bedrijfslaag — subset (NL)
    akker: '🌾', melkvee: '🐄', intensief: '🐖',
    kennis: '💡', uitvoerend: '🔧', sector: '🏢',
    grootte_klein: '🏪', grootte_mid: '🏬', grootte_groot: '🏭',
    // Q7 netwerk — NL
    sterk_net: '⚡', zwak_net: '🔌', gas_afhankelijk: '🛢️', warmtenet: '♨️',
  };
  if (map[antwoordKey]) return map[antwoordKey];
  return '•';
}

export function iconVoorVraag(vraagId: string): string {
  return ({
    Q1_sector: '🎯',
    Q2_wonen: '🏠',
    Q3_gezin: '👥',
    Q4_leeftijd: '⏳',
    Q5_regio: '📍',
    Q6_bedrijfslaag: '🏢',
    Q7_netwerk: '🌐',
  } as Record<string, string>)[vraagId] || '•';
}
