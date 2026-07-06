interface LogoProps {
  size?: number;
  className?: string;
  withWordmark?: boolean;
}

/** Een oog met een kaart-grid in de iris — neutraal beeldmerk. */
export function LogoMark({ size = 32, className }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      fill="none"
      className={className}
      aria-label="De Gevolgenkaart logo"
      role="img"
    >
      {/* ooglid / kaart-omtrek */}
      <path
        d="M4 24C9 14 16 9 24 9C32 9 39 14 44 24C39 34 32 39 24 39C16 39 9 34 4 24Z"
        stroke="currentColor"
        strokeWidth="2"
        fill="none"
      />
      {/* iris */}
      <circle cx="24" cy="24" r="8.5" stroke="currentColor" strokeWidth="1.6" fill="none" />
      {/* kaart-grid binnen de iris */}
      <path d="M24 15.5V32.5M15.5 24H32.5" stroke="currentColor" strokeWidth="1.1" opacity="0.8" />
      <path d="M19 18.5L29 29.5M29 18.5L19 29.5" stroke="currentColor" strokeWidth="0.7" opacity="0.4" />
      {/* pupil als accent */}
      <circle cx="24" cy="24" r="2.6" fill="hsl(var(--negatief))" />
    </svg>
  );
}

export function Logo({ size = 32, className, withWordmark = true }: LogoProps) {
  return (
    <div className={`flex items-center gap-3 ${className ?? ""}`}>
      <LogoMark size={size} className="text-foreground" />
      {withWordmark && (
        <div className="flex flex-col leading-none">
          <span className="font-serif text-base font-semibold tracking-tight text-foreground">
            De Gevolgenkaart
          </span>
          <span className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground mt-0.5">
            GEVOLGENKAART.NL
          </span>
        </div>
      )}
    </div>
  );
}
