import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { PageShell } from "@/components/Chrome";
import { filters } from "@/lib/data";

export default function Methodologie() {
  return (
    <PageShell>
      <article className="mx-auto max-w-2xl px-5 sm:px-8 pt-12 sm:pt-16 pb-8 step-enter">
        <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground mb-3">
          Verantwoording
        </p>
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold tracking-tight">
          Methodologie
        </h1>
        <p className="mt-4 text-muted-foreground text-[15px] leading-relaxed">
          De Gevolgenkaart is een journalistiek model, geen voorspelling. Hieronder
          staat hoe de cijfers tot stand komen en wat zij wel en niet betekenen.
        </p>

        <div className="prose-editorial mt-10 space-y-8">
          <section>
            <h2 className="font-serif text-xl font-semibold mb-2">De drie ordes</h2>
            <p className="text-[15px] leading-relaxed text-foreground/85">
              Elk beleidselement werkt in cascade door. De <strong>1e orde</strong>{" "}
              (jaar 1&ndash;2) vangt de directe, mechanische effecten: een tarief gaat
              omhoog of omlaag, een regeling verschijnt of verdwijnt. De{" "}
              <strong>2e orde</strong> (jaar 3) telt de gedragsreacties mee:
              investeringen verschuiven, talent blijft of vertrekt, bedrijven schalen
              op of af. De <strong>3e orde</strong> (jaar 5&ndash;10) toont de
              structurele uitkomst wanneer die reacties zich hebben opgestapeld in de
              productieve basis van het land.
            </p>
          </section>

          <section>
            <h2 className="font-serif text-xl font-semibold mb-2">
              De negen filters
            </h2>
            <p className="text-[15px] leading-relaxed text-foreground/85 mb-4">
              Ieder element wordt op een schaal van 0&ndash;10 (5 is neutraal)
              gescoord op negen macrofilters. De cascade-waarde is{" "}
              <span className="font-mono text-sm">sign(&Sigma;F&apos;) &times; &radic;(&Sigma;|F&apos;|&sup2;)</span>,
              met F&apos; de afwijking van neutraal.
            </p>
            <dl className="space-y-2.5">
              {Object.entries(filters).map(([id, f]) => (
                <div
                  key={id}
                  className="border-l-2 border-border pl-4 py-1"
                >
                  <dt className="font-medium text-[14px]">
                    <span className="font-mono text-[11px] text-muted-foreground mr-2">
                      {id}
                    </span>
                    {f.naam}
                    <span className="text-muted-foreground font-normal">
                      {" "}
                      &mdash; {f.volledig}
                    </span>
                  </dt>
                  <dd className="text-[13px] text-muted-foreground mt-0.5 leading-relaxed">
                    {f.uitleg}
                  </dd>
                </div>
              ))}
            </dl>
          </section>

          <section>
            <h2 className="font-serif text-xl font-semibold mb-2">
              Empirische verankering: Argenti&euml; &amp; Zuid-Afrika
            </h2>
            <p className="text-[15px] leading-relaxed text-foreground/85">
              De cascade-co&euml;ffici&euml;nten zijn geijkt aan historische
              natuurlijke experimenten. <strong>Argenti&euml;</strong> levert het
              ijkpunt voor herhaalde kapitaalvlucht, vermogensheffingen en
              prijscontroles met meetbare krimp van de productieve basis.{" "}
              <strong>Zuid-Afrika</strong> levert het ijkpunt voor institutionele
              erosie, brain drain van hooggeschoolden en desinvestering. Deze
              casussen kalibreren de orde-op-orde versterkingsfactoren &mdash; zij
              voorspellen geen exacte euro&apos;s, maar de richting en de relatieve
              zwaarte.
            </p>
          </section>

          <section>
            <h2 className="font-serif text-xl font-semibold mb-2">
              Bronnen voor partijposities
            </h2>
            <p className="text-[15px] leading-relaxed text-foreground/85">
              De positie en intensiteit van elke partij per element komen uit de
              verkiezingsprogramma&apos;s 2025&ndash;2030, het CPB-rapport Keuzes in
              Kaart 2025&ndash;2028 en het Kamerstemgedrag 2023&ndash;2026.
            </p>
          </section>

          <section className="bg-accent/60 border border-card-border rounded-md p-5">
            <h2 className="font-serif text-lg font-semibold mb-2">
              Wat de cijfers niet zijn
            </h2>
            <p className="text-[14px] leading-relaxed text-foreground/85">
              De getallen zijn relatieve cascade-indexpunten, geen euro-bedragen en
              geen koopkrachtplaatjes. De kaart vergelijkt geen partijen onderling en
              geeft geen stemadvies. Zij maakt de cascade van &eacute;&eacute;n
              keuze zichtbaar &mdash; geen partij-advies, alleen feiten.
            </p>
          </section>
        </div>

        <div className="mt-10 flex flex-wrap gap-3">
          <Link href="/sector" asChild>
            <Button size="lg">Vind uw gevolgenkaart &rarr;</Button>
          </Link>
          <Link href="/" asChild>
            <Button size="lg" variant="ghost">
              Terug naar start
            </Button>
          </Link>
        </div>
      </article>
    </PageShell>
  );
}
