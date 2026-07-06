import { Download, X, Diamond } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  getUitkomst,
  partijen,
  partijAccent,
  isReferentie,
  ordeLabels,
  fmtGetal,
  type OrdeKey,
} from "@/lib/data";
// jsPDF + html2canvas worden lazy geladen bij eerste klik op PDF-knop —
// scheelt ~400 KB op de initial bundle (sneller laden op iPhone).

interface Props {
  partijId: string;
  sectorId: string;
  onSluit: () => void;
}

const ORDES: OrdeKey[] = ["1e_orde", "2e_orde", "3e_orde"];

/** Inline uitklappaneel met de drie ordes, top-5 versterkend/verzwakkend en PDF-knop. */
export function PartijDetail({ partijId, sectorId, onSluit }: Props) {
  const partij = partijen[partijId];
  const u = getUitkomst(partijId, sectorId);
  if (!partij || !u) return null;

  const ref = isReferentie(partijId);
  const accent = partijAccent[partijId] ?? "#6b6258";

  return (
    <div
      className="step-enter rounded-md border border-card-border bg-card p-5 sm:p-7 mt-3"
      data-testid={`detail-${partijId}`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          {ref ? (
            <Diamond className="h-4 w-4" style={{ color: accent }} fill={accent} />
          ) : (
            <span
              className="inline-block h-3 w-3 rounded-full ring-1 ring-black/10"
              style={{ backgroundColor: accent }}
            />
          )}
          <div>
            <h3 className="font-serif text-xl sm:text-2xl font-semibold leading-tight">
              {partij.naam}
            </h3>
            <p className="text-[13px] text-muted-foreground">
              Profiel voor sector: <span className="text-foreground/80">{u.sector_naam}</span>
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onSluit}
          data-testid={`button-sluit-${partijId}`}
          className="hover-elevate rounded-md p-1.5 text-muted-foreground hover:text-foreground -mr-1"
          aria-label="Samenvouwen"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {ref && (
        <div
          className="mt-3 inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[11px] font-medium uppercase tracking-[0.12em]"
          style={{ borderColor: accent, color: accent }}
        >
          <Diamond className="h-3 w-3" fill={accent} /> Referentiemodel — niet op het stembiljet
        </div>
      )}

      {/* Drie orde-kaarten */}
      <div className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
        {ORDES.map((o) => {
          const meta = ordeLabels[o];
          const val = u[o];
          return (
            <div key={o} className="rounded-md border border-card-border bg-background/60 p-4">
              <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
                {meta.titel}
              </p>
              <p className="text-[11px] text-muted-foreground">{meta.periode}</p>
              <p
                className={`font-serif text-3xl font-semibold mt-2 ${val >= 0 ? "text-positief" : "text-negatief"}`}
                data-testid={`detail-${partijId}-${o}`}
              >
                {fmtGetal(val)}
              </p>
              <p className="text-[11px] text-muted-foreground mt-1">{meta.omschrijving}</p>
            </div>
          );
        })}
      </div>

      {/* Top-5 versterkend / verzwakkend */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
        <div>
          <h4 className="font-serif text-base font-semibold mb-1">Sterkst versterkend</h4>
          <div className="h-0.5 w-12 bg-positief mb-3" />
          <ul className="space-y-2">
            {u.top_positief.slice(0, 5).map((it) => (
              <li key={it.element_id} className="flex items-baseline gap-3 text-[13px]">
                <span className="font-mono text-positief font-semibold tabular-nums w-12 shrink-0">
                  {fmtGetal(it.bijdrage)}
                </span>
                <span className="text-foreground/85 leading-snug">{it.naam}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="font-serif text-base font-semibold mb-1">Sterkst verzwakkend</h4>
          <div className="h-0.5 w-12 bg-negatief mb-3" />
          <ul className="space-y-2">
            {u.top_negatief.slice(0, 5).map((it) => (
              <li key={it.element_id} className="flex items-baseline gap-3 text-[13px]">
                <span className="font-mono text-negatief font-semibold tabular-nums w-12 shrink-0">
                  {fmtGetal(it.bijdrage)}
                </span>
                <span className="text-foreground/85 leading-snug">{it.naam}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <Button
          onClick={async () => {
            const { genereerRapport } = await import("@/lib/pdf");
            await genereerRapport(partijId, partij, sectorId, u);
          }}
          data-testid={`button-pdf-${partijId}`}
          className="gap-2"
        >
          <Download className="h-4 w-4" /> Download PDF-rapport voor deze keuze
        </Button>
        <button
          type="button"
          onClick={onSluit}
          className="text-sm text-muted-foreground hover:text-foreground underline-offset-2 hover:underline"
        >
          Samenvouwen
        </button>
      </div>
    </div>
  );
}
