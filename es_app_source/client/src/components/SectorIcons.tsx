// 22 SVG-iconen per sector, lijntekeningen op viewBox 0 0 24 24
// Consistente stijl: stroke=currentColor, fill=none, strokeWidth=1.5

import type { ReactNode } from 'react';

interface IconProps {
  className?: string;
}

const wrap = (children: ReactNode, props: IconProps) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={props.className}
  >
    {children}
  </svg>
);

// S1 Zorg & welzijn — stethoscoop
export const IconZorg = (p: IconProps) =>
  wrap(
    <>
      <path d="M4 5v6a4 4 0 0 0 8 0V5" />
      <path d="M4 5h2M10 5h2" />
      <circle cx="8" cy="18" r="2" />
      <path d="M8 15v-3" />
      <circle cx="18" cy="14" r="2" />
      <path d="M18 16v2a3 3 0 0 1-6 0v-1" />
    </>,
    p
  );

// S2 Onderwijs — boek met afstudeerhoed
export const IconOnderwijs = (p: IconProps) =>
  wrap(
    <>
      <path d="M4 6.5v11l8 3 8-3v-11" />
      <path d="M4 6.5l8 3 8-3-8-3-8 3z" />
      <path d="M18 8v4" />
    </>,
    p
  );

// S3 Veiligheid & defensie — schild
export const IconDefensie = (p: IconProps) =>
  wrap(
    <>
      <path d="M12 2 4 5v6c0 5 3.5 9 8 11 4.5-2 8-6 8-11V5z" />
      <path d="M9 12l2 2 4-4" />
    </>,
    p
  );

// S4 Openbaar bestuur — gebouw met zuilen
export const IconBestuur = (p: IconProps) =>
  wrap(
    <>
      <path d="M3 21h18" />
      <path d="M3 10h18" />
      <path d="M12 3 3 10h18z" />
      <path d="M6 10v11M10 10v11M14 10v11M18 10v11" />
    </>,
    p
  );

// S5 Industrie — fabriek met schoorsteen
export const IconIndustrie = (p: IconProps) =>
  wrap(
    <>
      <path d="M3 21V11l5 3V11l5 3V11l5 3v7H3z" />
      <path d="M7 3v6" />
      <path d="M7 7l-2 1M7 7l2 1" />
    </>,
    p
  );

// S6 Bouw — kraan
export const IconBouw = (p: IconProps) =>
  wrap(
    <>
      <path d="M4 21V5h2" />
      <path d="M6 7h14" />
      <path d="M20 7v3l-4-3" />
      <path d="M11 7v6" />
      <rect x="9" y="13" width="4" height="4" />
    </>,
    p
  );

// S7 Logistiek — vrachtwagen
export const IconLogistiek = (p: IconProps) =>
  wrap(
    <>
      <path d="M2 7h11v10H2z" />
      <path d="M13 10h5l3 3v4h-8z" />
      <circle cx="6" cy="18" r="2" />
      <circle cx="17" cy="18" r="2" />
    </>,
    p
  );

// S8 Landbouw — tarwe / graan
export const IconLandbouw = (p: IconProps) =>
  wrap(
    <>
      <path d="M12 21V8" />
      <path d="M12 10c-2-2-2-4 0-6 2 2 2 4 0 6z" />
      <path d="M12 14c-2-2-4-2-6 0 2 2 4 2 6 0z" />
      <path d="M12 14c2-2 4-2 6 0-2 2-4 2-6 0z" />
      <path d="M12 18c-2-2-4-2-6 0 2 2 4 2 6 0z" />
      <path d="M12 18c2-2 4-2 6 0-2 2-4 2-6 0z" />
    </>,
    p
  );

// S9 Handel — winkelwagen
export const IconHandel = (p: IconProps) =>
  wrap(
    <>
      <circle cx="9" cy="20" r="1.5" />
      <circle cx="17" cy="20" r="1.5" />
      <path d="M3 4h2l2 12h12l2-8H6" />
    </>,
    p
  );

// S10 Horeca — vork & mes
export const IconHoreca = (p: IconProps) =>
  wrap(
    <>
      <path d="M7 3v18" />
      <path d="M5 3v6c0 1 1 2 2 2s2-1 2-2V3" />
      <path d="M17 3c-1.5 0-3 2-3 5v4h3v9" />
    </>,
    p
  );

// S11 ICT — monitor + code
export const IconICT = (p: IconProps) =>
  wrap(
    <>
      <rect x="3" y="4" width="18" height="13" rx="1" />
      <path d="M9 21h6" />
      <path d="M12 17v4" />
      <path d="m9 8-2 2 2 2M15 8l2 2-2 2" />
    </>,
    p
  );

// S12 Financiën — euro + grafiek
export const IconFinancien = (p: IconProps) =>
  wrap(
    <>
      <path d="M16 7c-1-1-3-2-5-2-3 0-5 3-5 7s2 7 5 7c2 0 4-1 5-2" />
      <path d="M5 10h7M5 13h7" />
    </>,
    p
  );

// S13 Creatieve sector — penseel
export const IconCreatief = (p: IconProps) =>
  wrap(
    <>
      <path d="M7 21 18 10l-3-3L4 18z" />
      <path d="M14 6l3 3" />
      <path d="M18 4l2 2" />
      <circle cx="6" cy="19" r="1" />
    </>,
    p
  );

// S14 Energie — bliksem
export const IconEnergie = (p: IconProps) =>
  wrap(
    <>
      <path d="M13 2 5 13h6l-2 9 9-12h-6z" />
    </>,
    p
  );

// S15 Vastgoed — huis met sleutel
export const IconVastgoed = (p: IconProps) =>
  wrap(
    <>
      <path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z" />
      <path d="M9 21v-6h6v6" />
    </>,
    p
  );

// S16 ZZP kennis — laptop
export const IconZzpKennis = (p: IconProps) =>
  wrap(
    <>
      <rect x="3" y="5" width="18" height="11" rx="1" />
      <path d="M2 20h20" />
      <path d="M10 9h4M9 12h6" />
    </>,
    p
  );

// S17 ZZP uitvoerend — gereedschap (sleutel + schroevendraaier)
export const IconZzpUitvoerend = (p: IconProps) =>
  wrap(
    <>
      <path d="m14 7 4-4 3 3-4 4z" />
      <path d="M14 7 4 17v3h3L17 10" />
      <circle cx="8" cy="16" r="2" />
    </>,
    p
  );

// S18 MKB — winkelpand
export const IconMKB = (p: IconProps) =>
  wrap(
    <>
      <path d="M3 9V21h18V9" />
      <path d="M3 9 5 4h14l2 5" />
      <path d="M3 9h18" />
      <path d="M10 21v-6h4v6" />
      <path d="M5 12h2v2H5z" />
    </>,
    p
  );

// S19 Grootbedrijf — wolkenkrabber
export const IconGrootbedrijf = (p: IconProps) =>
  wrap(
    <>
      <path d="M6 21V5h6v16" />
      <path d="M12 21V9h6v12" />
      <path d="M3 21h18" />
      <path d="M8 8h2M8 12h2M8 16h2" />
      <path d="M14 12h2M14 16h2" />
    </>,
    p
  );

// S20 Gepensioneerd — wandelstok / zonnewijzer
export const IconGepensioneerd = (p: IconProps) =>
  wrap(
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 3" />
    </>,
    p
  );

// S21 Uitkering — handhulp
export const IconUitkering = (p: IconProps) =>
  wrap(
    <>
      <path d="M5 12c0-4 3-7 7-7s7 3 7 7" />
      <path d="M5 12v4a2 2 0 0 0 2 2h2v-6" />
      <path d="M15 18h2a2 2 0 0 0 2-2v-4" />
      <path d="M12 5V2" />
      <circle cx="12" cy="14" r="1.5" />
    </>,
    p
  );

// S22 Student — pet
export const IconStudent = (p: IconProps) =>
  wrap(
    <>
      <path d="M2 10 12 5l10 5-10 5z" />
      <path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5" />
      <path d="M22 10v6" />
    </>,
    p
  );

// Lookup
export const SECTOR_ICONS: Record<string, (p: IconProps) => ReactNode> = {
  S1_zorg: IconZorg,
  S2_onderwijs: IconOnderwijs,
  S3_defensie: IconDefensie,
  S4_bestuur: IconBestuur,
  S5_industrie: IconIndustrie,
  S6_bouw: IconBouw,
  S7_logistiek: IconLogistiek,
  S8_landbouw: IconLandbouw,
  S9_handel: IconHandel,
  S10_horeca: IconHoreca,
  S11_ict: IconICT,
  S12_financien: IconFinancien,
  S13_creatief: IconCreatief,
  S14_energie: IconEnergie,
  S15_vastgoed: IconVastgoed,
  S16_zzp_kennis: IconZzpKennis,
  S17_zzp_uitvoerend: IconZzpUitvoerend,
  S18_mkb: IconMKB,
  S19_grootbedrijf: IconGrootbedrijf,
  S20_gepensioneerd: IconGepensioneerd,
  S21_uitkering: IconUitkering,
  S22_student: IconStudent,
};

// Cluster mapping voor sectoren
export const SECTOR_CLUSTERS: Record<string, 'publiek' | 'industrie' | 'diensten' | 'overig'> = {
  S1_zorg: 'publiek',
  S2_onderwijs: 'publiek',
  S3_defensie: 'publiek',
  S4_bestuur: 'publiek',
  S5_industrie: 'industrie',
  S6_bouw: 'industrie',
  S7_logistiek: 'industrie',
  S8_landbouw: 'industrie',
  S14_energie: 'industrie',
  S9_handel: 'diensten',
  S10_horeca: 'diensten',
  S11_ict: 'diensten',
  S12_financien: 'diensten',
  S13_creatief: 'diensten',
  S15_vastgoed: 'overig',
  S16_zzp_kennis: 'overig',
  S17_zzp_uitvoerend: 'overig',
  S18_mkb: 'overig',
  S19_grootbedrijf: 'overig',
  S20_gepensioneerd: 'overig',
  S21_uitkering: 'overig',
  S22_student: 'overig',
};

// Cluster kleuren (Tailwind-vriendelijk)
export const CLUSTER_STYLES = {
  publiek: {
    bg: 'bg-sky-50',
    border: 'border-sky-200',
    borderActive: 'border-sky-500',
    icon: 'text-sky-700',
    label: 'Publiek',
  },
  industrie: {
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    borderActive: 'border-amber-500',
    icon: 'text-amber-700',
    label: 'Industrie & primair',
  },
  diensten: {
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    borderActive: 'border-emerald-500',
    icon: 'text-emerald-700',
    label: 'Diensten & handel',
  },
  overig: {
    bg: 'bg-violet-50',
    border: 'border-violet-200',
    borderActive: 'border-violet-500',
    icon: 'text-violet-700',
    label: 'Overig',
  },
};

// Cluster van elk sector-id
export function getClusterStyle(sectorKey: string) {
  const cluster = SECTOR_CLUSTERS[sectorKey] || 'overig';
  return CLUSTER_STYLES[cluster];
}
