import { Link } from "wouter";
import { Logo } from "./Logo";

export function Header() {
  return (
    <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-40">
      <div className="mx-auto max-w-5xl px-5 sm:px-8 h-16 flex items-center justify-between">
        <Link href="/" data-testid="link-home" className="hover-elevate rounded-md -ml-1 px-1 py-1">
          <Logo size={30} />
        </Link>
        <Link
          href="/"
          data-testid="link-start"
          className="hidden sm:inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
        >
          Naar de gevolgenkaart &rarr;
        </Link>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-border mt-20">
      <div className="mx-auto max-w-5xl px-5 sm:px-8 py-10 grid gap-8 sm:grid-cols-3 text-sm">
        <div>
          <Logo size={28} />
          <p className="mt-3 text-muted-foreground leading-relaxed text-[13px]">
            Een persoonlijke politieke bijsluiter. Geen partij-vergelijking, geen
            stemadvies &mdash; alleen de cascade van &eacute;&eacute;n keuze.
          </p>
        </div>
        <div>
          <h4 className="font-serif font-semibold mb-2">Verantwoording</h4>
          <ul className="space-y-1.5 text-muted-foreground text-[13px]">
            <li>
              <Link
                href="/methodologie"
                data-testid="link-methodologie"
                className="hover:text-foreground underline-offset-2 hover:underline"
              >
                Methodologie &amp; de drie ordes
              </Link>
            </li>
            <li>Bron: verkiezingsprogramma&apos;s 2025&ndash;2030, CPB Keuzes in Kaart, Kamerstemgedrag</li>
            <li>Empirische ijking: Argenti&euml; &amp; Zuid-Afrika</li>
          </ul>
        </div>
        <div>
          <h4 className="font-serif font-semibold mb-2">Bron</h4>
          <p className="text-muted-foreground text-[13px] leading-relaxed">
            Een interdisciplinair onderzoeksteam
            <br />
            gevolgenkaart.nl
          </p>
          <p className="mt-3 text-[11px] uppercase tracking-[0.15em] text-muted-foreground">
            Geen partij-advies, alleen feiten
          </p>
        </div>
      </div>

      <div className="border-t border-border/60">
        <div className="mx-auto max-w-5xl px-5 sm:px-8 py-8 text-muted-foreground">
          <div className="grid gap-7 sm:grid-cols-3">
            <div>
              <h5 className="text-[11px] font-semibold uppercase tracking-[0.18em] text-foreground/70 mb-2">
                Disclaimer
              </h5>
              <p className="text-[12px] leading-relaxed">
                De Gevolgenkaart geeft geen stemadvies. Het instrument toont
                modelmatige cascade-effecten van programmapunten op de
                Spaanse productie- en welvaartsbasis, gekalibreerd op
                historische precedenten (Argenti&euml; 2024, Zuid-Afrika
                2010&ndash;2026, Frankrijk ISF 1988&ndash;2017, eigen
                modelvergelijking).
              </p>
              <p className="text-[12px] leading-relaxed mt-2">
                De gebruiker beoordeelt zelf de betekenis voor zijn of haar stem.
                Bandbreedtes en aannames worden in de methodologie-pagina
                toegelicht.
              </p>
              <p className="text-[12px] leading-relaxed mt-2">
                VMP/Nova Democratia en Carbon-Alert/BiCRS staan in de matrix als
                referentiemodellen &mdash; zij zijn geen partij op het
                stembiljet.
              </p>
            </div>
            <div>
              <h5 className="text-[11px] font-semibold uppercase tracking-[0.18em] text-foreground/70 mb-2">
                Privacy
              </h5>
              <p className="text-[12px] leading-relaxed">
                Deze website gebruikt geen cookies, geen tracking-pixels, geen
                analytics. Er worden geen IP-adressen gelogd. Er wordt geen
                enkele persoonsgegeven opgeslagen of doorgegeven aan derden. De
                berekening gebeurt volledig in uw browser.
              </p>
            </div>
            <div>
              <h5 className="text-[11px] font-semibold uppercase tracking-[0.18em] text-foreground/70 mb-2">
                Contact
              </h5>
              <p className="text-[12px] leading-relaxed">
                Correcties, vragen of opmerkingen via:
                <br />
                <a
                  href="mailto:contact@gevolgenkaart.nl"
                  data-testid="link-contact"
                  className="hover:text-foreground underline-offset-2 hover:underline"
                >
                  contact@gevolgenkaart.nl
                </a>
              </p>
            </div>
          </div>
          <p className="mt-7 text-[11px] text-muted-foreground/70">
            (Disclaimer + privacy versie 28 juni 2026)
          </p>
        </div>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col paper-bg">
      <Header />
      <main className="flex-1 w-full">{children}</main>
      <Footer />
    </div>
  );
}

export function StepIndicator({ current }: { current: 1 | 2 | 3 }) {
  const steps = [
    { n: 1, label: "Uw sector" },
    { n: 2, label: "De partij" },
    { n: 3, label: "Uw gevolgenkaart" },
  ];
  return (
    <ol className="flex items-center justify-center gap-2 sm:gap-4 text-xs sm:text-sm mb-10">
      {steps.map((s, i) => (
        <li key={s.n} className="flex items-center gap-2 sm:gap-4">
          <div className="flex items-center gap-2">
            <span
              className={`flex h-6 w-6 items-center justify-center rounded-full border text-[11px] font-medium ${
                s.n === current
                  ? "border-foreground bg-foreground text-background"
                  : s.n < current
                    ? "border-foreground/40 text-foreground/60"
                    : "border-border text-muted-foreground"
              }`}
            >
              {s.n}
            </span>
            <span
              className={`${s.n === current ? "text-foreground font-medium" : "text-muted-foreground"} hidden sm:inline`}
            >
              {s.label}
            </span>
          </div>
          {i < steps.length - 1 && <span className="h-px w-5 sm:w-8 bg-border" />}
        </li>
      ))}
    </ol>
  );
}
