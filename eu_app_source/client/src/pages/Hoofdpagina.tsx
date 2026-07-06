import { useState, useEffect, useRef } from "react";
import { Link } from "wouter";
import { ChevronDown, Diamond } from "lucide-react";
import { Footer } from "@/components/Chrome";
import { LogoMark } from "@/components/Logo";
import { MatrixSectie } from "@/components/MatrixSectie";
import { PersoonlijkeWeging } from "@/components/PersoonlijkeWeging";
import { PartijDetail } from "@/components/PartijDetail";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  sectoren,
  sectorGroepen,
  partijAccent,
  isReferentie,
  ranglijstVoorSector,
  ordeLabels,
  fmtGetal,
  filters,
  type OrdeKey,
} from "@/lib/data";
import { useHashState, scrollToId } from "@/lib/hashstate";

const ORDE_TOGGLES: { key: OrdeKey; label: string }[] = [
  { key: "1e_orde", label: "1e orde" },
  { key: "2e_orde", label: "2e orde" },
  { key: "3e_orde", label: "3e orde" },
];

export default function Hoofdpagina() {
  const [state, setState] = useHashState();
  const { sector, weights, partij } = state;
  const [sorteer, setSorteer] = useState<OrdeKey>("3e_orde");
  const ranglijstRef = useRef<HTMLDivElement>(null);

  // Bij eerste binnenkomst met een sector in de hash: scroll erheen.
  const eersteRender = useRef(true);
  useEffect(() => {
    if (eersteRender.current && sector) {
      eersteRender.current = false;
      setTimeout(() => scrollToId("ranglijst"), 250);
    } else {
      eersteRender.current = false;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function kiesSector(sid: string) {
    setState({ sector: sid, partij: null });
    setTimeout(() => scrollToId("ranglijst"), 80);
  }

  function celKlik(sid: string) {
    setState({ sector: sid, partij: null });
    setTimeout(() => scrollToId("ranglijst"), 80);
  }

  function partijKlik(pid: string) {
    setState({ partij: partij === pid ? null : pid });
  }

  const ranglijst = sector ? ranglijstVoorSector(sector, sorteer) : [];

  return (
    <div className="min-h-screen flex flex-col paper-bg">
      {/* Minimale top-balk met logo */}
      <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-40">
        <div className="mx-auto max-w-6xl px-5 sm:px-8 h-16 flex items-center justify-between">
          <button
            type="button"
            onClick={() => scrollToId("hero")}
            data-testid="link-home"
            className="hover-elevate rounded-md -ml-1 px-1 py-1 flex items-center gap-3"
          >
            <LogoMark size={30} className="text-foreground" />
            <div className="flex flex-col leading-none text-left">
              <span className="font-serif text-base font-semibold tracking-tight">
                De Gevolgenkaart
              </span>
              <span className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground mt-0.5">
                GEVOLGENKAART.NL
              </span>
            </div>
          </button>
          <button
            type="button"
            onClick={() => scrollToId("kies-sector")}
            data-testid="link-start"
            className="hidden sm:inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            Kies uw sector &darr;
          </button>
        </div>
      </header>

      <main className="flex-1 w-full">
        {/* ============ SECTIE 1 — HERO ============ */}
        <section
          id="hero"
          className="mx-auto max-w-3xl px-5 sm:px-8 pt-20 sm:pt-28 pb-16 text-center"
        >
          <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground mb-6">
            Een politieke bijsluiter — geen stemadvies
          </p>
          <h1 className="font-serif text-4xl sm:text-5xl md:text-6xl font-semibold tracking-tight leading-[1.08]">
            Wat als de StemWijzer u zou vertellen wát u stemt?
          </h1>
          <p className="mt-7 text-[16px] sm:text-[17px] leading-relaxed text-foreground/75 max-w-2xl mx-auto">
            Onderstaande tabel toont voor elke partij wat hun programma betekent voor 22
            sectoren van de Spaanse maatschappij — direct, op middellange en op lange
            termijn. Geen voorkeur, alleen rekenkundige cascade-effecten.
          </p>
          <button
            type="button"
            onClick={() => scrollToId("matrix")}
            className="mt-12 inline-flex flex-col items-center gap-1 text-muted-foreground hover:text-foreground transition-colors"
            data-testid="button-scroll-matrix"
          >
            <span className="text-[12px] uppercase tracking-[0.18em]">scroll voor de matrix</span>
            <ChevronDown className="h-5 w-5 animate-bounce" />
          </button>
        </section>

        {/* ============ SECTIE 2 — VOLLEDIGE MATRIX ============ */}
        <section id="matrix" className="mx-auto max-w-6xl px-5 sm:px-8 py-12 scroll-mt-20">
          <div className="mb-6 max-w-2xl">
            <h2 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight">
              De volledige gevolgenkaart
            </h2>
            <p className="mt-2 text-muted-foreground text-[15px] leading-relaxed">
              17 partijen, 22 sectoren. Elke cel is het cascade-effect van het programma op
              die sector. Wissel tussen de drie tijdsordes; standaard ziet u de structurele
              uitkomst op lange termijn.
            </p>
          </div>
          <MatrixSectie onCelKlik={celKlik} />
        </section>

        {/* ============ SECTIE 3 — UITNODIGING ============ */}
        <section
          id="kies-sector"
          className="mx-auto max-w-3xl px-5 sm:px-8 py-16 text-center scroll-mt-20"
        >
          <div className="h-px w-24 bg-border mx-auto mb-10" />
          <h2 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight">
            Wilt u zien hoe dit voor u uitpakt?
          </h2>
          <p className="mt-2 text-muted-foreground text-[15px]">
            Kies uw sector hieronder.
          </p>
          <div className="mt-7 flex justify-center">
            <Select value={sector ?? ""} onValueChange={kiesSector}>
              <SelectTrigger
                className="w-full sm:w-[26rem] h-12 text-[15px]"
                data-testid="select-sector"
              >
                <SelectValue placeholder="Selecteer uw sector…" />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(sectorGroepen).map(([groep, ids]) => (
                  <SelectGroup key={groep}>
                    <SelectLabel>{groep}</SelectLabel>
                    {ids.map((id) => (
                      <SelectItem key={id} value={id}>
                        <span className="font-mono text-muted-foreground mr-2">{id}</span>
                        {sectoren[id].naam}
                      </SelectItem>
                    ))}
                  </SelectGroup>
                ))}
              </SelectContent>
            </Select>
          </div>
        </section>

        {/* ============ SECTIE 4 — RANGLIJST ============ */}
        {sector && (
          <section
            id="ranglijst"
            ref={ranglijstRef}
            className="step-enter mx-auto max-w-4xl px-5 sm:px-8 py-10 scroll-mt-20"
          >
            <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground mb-1">
                  Ranglijst voor uw sector
                </p>
                <h2 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight">
                  {sectoren[sector].naam}
                </h2>
              </div>
              <div className="inline-flex rounded-md border border-border bg-background/60 p-1 self-start">
                {ORDE_TOGGLES.map((t) => (
                  <button
                    key={t.key}
                    type="button"
                    onClick={() => setSorteer(t.key)}
                    data-testid={`sorteer-${t.key}`}
                    className={`px-3 py-1.5 text-[13px] rounded-[4px] transition-colors ${
                      sorteer === t.key
                        ? "bg-foreground text-background font-medium"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Koprij */}
            <div className="mt-6 grid grid-cols-[2rem_1fr_4rem_4rem_4rem] sm:grid-cols-[2.5rem_1fr_5rem_5rem_5rem] gap-2 px-4 pb-2 text-[11px] uppercase tracking-[0.1em] text-muted-foreground">
              <span>#</span>
              <span>Partij</span>
              <span className={`text-right ${sorteer === "1e_orde" ? "font-bold text-foreground" : ""}`}>1e</span>
              <span className={`text-right ${sorteer === "2e_orde" ? "font-bold text-foreground" : ""}`}>2e</span>
              <span className={`text-right ${sorteer === "3e_orde" ? "font-bold text-foreground" : ""}`}>3e</span>
            </div>

            <ol className="divide-y divide-border rounded-md border border-card-border bg-card overflow-hidden">
              {ranglijst.map((r, i) => {
                const ref = isReferentie(r.partijId);
                const accent = partijAccent[r.partijId] ?? "#6b6258";
                const actief = partij === r.partijId;
                return (
                  <li key={r.partijId}>
                    <button
                      type="button"
                      onClick={() => partijKlik(r.partijId)}
                      data-testid={`regel-${r.partijId}`}
                      className={`hover-elevate w-full grid grid-cols-[2rem_1fr_4rem_4rem_4rem] sm:grid-cols-[2.5rem_1fr_5rem_5rem_5rem] gap-2 items-center px-4 py-2.5 text-left ${
                        actief ? "bg-accent" : ""
                      }`}
                    >
                      <span className="font-mono text-[13px] text-muted-foreground tabular-nums">
                        {i + 1}
                      </span>
                      <span className="flex items-center gap-2.5 min-w-0">
                        {ref ? (
                          <Diamond className="h-3.5 w-3.5 shrink-0" style={{ color: accent }} fill={accent} />
                        ) : (
                          <span
                            className="inline-block h-2.5 w-2.5 rounded-full shrink-0 ring-1 ring-black/10"
                            style={{ backgroundColor: accent }}
                          />
                        )}
                        <span className="text-[15px] truncate">{r.partij.naam}</span>
                        <span className="hidden sm:inline text-[11px] rounded-full border border-border px-2 py-0.5 text-muted-foreground capitalize shrink-0">
                          {r.partij.type.replace(/-/g, " ")}
                        </span>
                        {ref && (
                          <span className="text-[10px] uppercase tracking-wide font-semibold shrink-0" style={{ color: accent }}>
                            ref
                          </span>
                        )}
                      </span>
                      <span className={`text-right font-mono text-[13px] tabular-nums ${sorteer === "1e_orde" ? "font-bold" : ""} ${r.een >= 0 ? "text-positief" : "text-negatief"}`}>
                        {fmtGetal(r.een)}
                      </span>
                      <span className={`text-right font-mono text-[13px] tabular-nums ${sorteer === "2e_orde" ? "font-bold" : ""} ${r.twee >= 0 ? "text-positief" : "text-negatief"}`}>
                        {fmtGetal(r.twee)}
                      </span>
                      <span className={`text-right font-mono text-[13px] tabular-nums ${sorteer === "3e_orde" ? "font-bold" : ""} ${r.drie >= 0 ? "text-positief" : "text-negatief"}`}>
                        {fmtGetal(r.drie)}
                      </span>
                    </button>
                    {/* Inline partij-detail */}
                    {partij === r.partijId && (
                      <div className="px-2 sm:px-4 pb-4 bg-background/40">
                        <PartijDetail
                          partijId={r.partijId}
                          sectorId={sector}
                          onSluit={() => setState({ partij: null })}
                        />
                      </div>
                    )}
                  </li>
                );
              })}
            </ol>
          </section>
        )}

        {/* ============ SECTIE 5 — PERSOONLIJKE WEGING ============ */}
        {sector && (
          <section
            id="weging"
            className="step-enter mx-auto max-w-4xl px-5 sm:px-8 py-12 scroll-mt-20"
          >
            <div className="h-px w-24 bg-border mb-10" />
            <PersoonlijkeWeging
              weights={weights}
              onChange={(w) => setState({ weights: w })}
              onPartijKlik={partijKlik}
              actievePartij={partij}
            />
          </section>
        )}

        {/* ============ SECTIE 7 — METHODOLOGIE (uitklap) ============ */}
        <section className="mx-auto max-w-3xl px-5 sm:px-8 py-16 scroll-mt-20">
          <div className="h-px w-24 bg-border mb-10" />
          <h2 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight mb-6">
            Hoe lezen we deze kaart?
          </h2>
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="ordes">
              <AccordionTrigger data-testid="acc-ordes" className="font-serif text-lg">
                De drie ordes
              </AccordionTrigger>
              <AccordionContent className="text-[15px] leading-relaxed text-foreground/85 space-y-3">
                <p>
                  Elk beleidselement werkt in cascade door. De <strong>1e orde</strong> (
                  {ordeLabels["1e_orde"].periode}) vangt de directe, mechanische effecten: een
                  tarief gaat omhoog of omlaag, een regeling verschijnt of verdwijnt.
                </p>
                <p>
                  De <strong>2e orde</strong> ({ordeLabels["2e_orde"].periode}) telt de
                  gedragsreacties mee: investeringen verschuiven, talent blijft of vertrekt,
                  bedrijven schalen op of af.
                </p>
                <p>
                  De <strong>3e orde</strong> ({ordeLabels["3e_orde"].periode}) toont de
                  structurele uitkomst wanneer die reacties zich hebben opgestapeld in de
                  productieve basis van het land. Daarom staat de matrix standaard op de 3e orde.
                </p>
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="bronnen">
              <AccordionTrigger data-testid="acc-bronnen" className="font-serif text-lg">
                Bronnen en kalibratie
              </AccordionTrigger>
              <AccordionContent className="text-[15px] leading-relaxed text-foreground/85 space-y-3">
                <p>
                  Ieder element wordt gescoord op negen macrofilters:{" "}
                  {Object.values(filters)
                    .map((f) => f.naam)
                    .join(", ")}
                  . De cascade-waarde is sign(Σ F′) × √(Σ F′²), gewogen met de positie en de
                  programmatische intensiteit van de partij.
                </p>
                <p>
                  De coëfficiënten zijn geijkt aan historische natuurlijke experimenten —
                  Argentinië (kapitaalvlucht, vermogensheffingen) en Zuid-Afrika (institutionele
                  erosie, brain drain) dragen het zwaarst. Zij voorspellen geen exacte euro's,
                  maar de richting en de relatieve zwaarte.
                </p>
                <p className="text-[14px] text-muted-foreground">
                  De volledige verantwoording staat op de{" "}
                  <Link href="/methodologie" data-testid="link-methodologie-detail" className="underline underline-offset-2 hover:text-foreground">
                    methodologie-pagina
                  </Link>
                  .
                </p>
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="niet">
              <AccordionTrigger data-testid="acc-niet" className="font-serif text-lg">
                Wat dit instrument NIET is
              </AccordionTrigger>
              <AccordionContent className="text-[15px] leading-relaxed text-foreground/85 space-y-3">
                <p>
                  De getallen zijn relatieve cascade-indexpunten, geen euro-bedragen en geen
                  koopkrachtplaatjes. De kaart geeft <strong>geen stemadvies</strong> en spreekt
                  geen voorkeur uit — zij maakt enkel de cascade van een keuze zichtbaar.
                </p>
                <p>
                  VMP / Nova Democratia en Carbon-Alert / BiCRS staan in de matrix als{" "}
                  <strong>referentiemodellen</strong> (ruit-icoon) — zij zijn geen partij op het
                  stembiljet, maar dienen als ijkpunt.
                </p>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </section>
      </main>

      {/* ============ SECTIE 8 — FOOTER (ongewijzigd) ============ */}
      <Footer />
    </div>
  );
}
