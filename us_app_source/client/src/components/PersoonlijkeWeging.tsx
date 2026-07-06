import { useState } from "react";
import { Plus, X, Diamond } from "lucide-react";
import { Slider } from "@/components/ui/slider";
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
  sectorIds,
  partijAccent,
  isReferentie,
  gewogenRanglijst,
  fmtGetal,
} from "@/lib/data";

interface Props {
  /** Genormaliseerde gewichten (sectorId -> 0..100). */
  weights: Record<string, number>;
  onChange: (weights: Record<string, number>) => void;
  onPartijKlik: (partijId: string) => void;
  actievePartij: string | null;
}

const MAX_SECTOREN = 5;

// Snel-knoppen met realistische combinaties.
const SUGGESTIES: { label: string; weights: Record<string, number> }[] = [
  { label: "Werknemer + huiseigenaar + spaargeld", weights: { S5: 60, S15: 25, S20: 15 } },
  { label: "ZZP'er die ook belegt", weights: { S16: 70, S19: 30 } },
  { label: "Zorgmedewerker met pensioenopbouw", weights: { S1: 75, S20: 25 } },
];

export function PersoonlijkeWeging({
  weights,
  onChange,
  onPartijKlik,
  actievePartij,
}: Props) {
  const [toevoegen, setToevoegen] = useState<string>("");
  const geselecteerd = Object.keys(weights);
  const ranglijst = gewogenRanglijst(weights);

  const totaal = geselecteerd.reduce((acc, s) => acc + (weights[s] || 0), 0);

  function voegToe(sid: string) {
    if (!sid || geselecteerd.includes(sid) || geselecteerd.length >= MAX_SECTOREN) return;
    // Nieuw gewicht: gelijk verdelen rond bestaande, simpel default 25.
    onChange({ ...weights, [sid]: 25 });
    setToevoegen("");
  }

  function verwijder(sid: string) {
    const next = { ...weights };
    delete next[sid];
    onChange(next);
  }

  function zetGewicht(sid: string, val: number) {
    onChange({ ...weights, [sid]: val });
  }

  const beschikbaar = sectorIds.filter((s) => !geselecteerd.includes(s));

  return (
    <div>
      <h3 className="font-serif text-2xl sm:text-3xl font-semibold tracking-tight">
        Klopt deze rangschikking voor u?
      </h3>
      <p className="mt-2 text-muted-foreground text-[15px] leading-relaxed max-w-2xl">
        Voeg meer sectoren toe met een eigen gewicht. U kunt tot {MAX_SECTOREN} sectoren
        combineren. De sliders normaliseren naar 100%.
      </p>

      {/* Suggesties */}
      <div className="mt-5 flex flex-wrap gap-2">
        <span className="text-[13px] text-muted-foreground self-center mr-1">
          Veel mensen werken in één sector maar zijn ook huiseigenaar en hebben spaargeld:
        </span>
        {SUGGESTIES.map((s) => (
          <button
            key={s.label}
            type="button"
            onClick={() => onChange(s.weights)}
            data-testid={`suggestie-${s.label}`}
            className="hover-elevate rounded-full border border-border bg-background/60 px-3 py-1.5 text-[13px] text-foreground/80"
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* Sliders */}
      <div className="mt-6 space-y-4">
        {geselecteerd.length === 0 && (
          <p className="text-[14px] text-muted-foreground italic">
            Nog geen sectoren toegevoegd — kies hieronder of gebruik een suggestie.
          </p>
        )}
        {geselecteerd.map((sid) => {
          const pct = totaal > 0 ? Math.round(((weights[sid] || 0) / totaal) * 100) : 0;
          return (
            <div key={sid} className="flex items-center gap-3 sm:gap-4" data-testid={`weging-${sid}`}>
              <div className="w-40 sm:w-52 shrink-0">
                <span className="font-mono text-[12px] text-muted-foreground mr-1.5">{sid}</span>
                <span className="text-[14px]">{sectoren[sid].naam}</span>
              </div>
              <div className="flex-1">
                <Slider
                  value={[weights[sid] || 0]}
                  min={0}
                  max={100}
                  step={1}
                  onValueChange={(v) => zetGewicht(sid, v[0])}
                  data-testid={`slider-${sid}`}
                />
              </div>
              <span className="w-12 text-right font-mono text-[13px] tabular-nums">{pct}%</span>
              <button
                type="button"
                onClick={() => verwijder(sid)}
                data-testid={`verwijder-${sid}`}
                className="hover-elevate rounded-md p-1 text-muted-foreground hover:text-foreground"
                aria-label={`Verwijder ${sectoren[sid].naam}`}
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          );
        })}
      </div>

      {/* Sector toevoegen */}
      {geselecteerd.length < MAX_SECTOREN && (
        <div className="mt-5 flex items-center gap-2">
          <Select value={toevoegen} onValueChange={voegToe}>
            <SelectTrigger className="w-full sm:w-96" data-testid="select-weging-toevoegen">
              <span className="flex items-center gap-2 text-muted-foreground">
                <Plus className="h-4 w-4" />
                <SelectValue placeholder="Sector toevoegen…" />
              </span>
            </SelectTrigger>
            <SelectContent>
              {Object.entries(sectorGroepen).map(([groep, ids]) => {
                const opties = ids.filter((id) => beschikbaar.includes(id));
                if (opties.length === 0) return null;
                return (
                  <SelectGroup key={groep}>
                    <SelectLabel>{groep}</SelectLabel>
                    {opties.map((id) => (
                      <SelectItem key={id} value={id}>
                        <span className="font-mono text-muted-foreground mr-2">{id}</span>
                        {sectoren[id].naam}
                      </SelectItem>
                    ))}
                  </SelectGroup>
                );
              })}
            </SelectContent>
          </Select>
        </div>
      )}

      {/* Persoonlijke ranglijst */}
      {ranglijst.length > 0 && geselecteerd.length > 0 && (
        <div className="step-enter mt-10">
          <h4 className="font-serif text-xl sm:text-2xl font-semibold tracking-tight">
            Uw persoonlijke ranglijst
          </h4>
          <p className="mt-1.5 text-[13px] text-muted-foreground">
            Partijen gesorteerd op het gewogen gemiddelde van de 3e orde over uw{" "}
            {geselecteerd.length} sector{geselecteerd.length > 1 ? "en" : ""}.
          </p>
          <ol className="mt-4 divide-y divide-border rounded-md border border-card-border bg-card overflow-hidden">
            {ranglijst.map((r, i) => {
              const ref = isReferentie(r.partijId);
              const accent = partijAccent[r.partijId] ?? "#6b6258";
              const actief = actievePartij === r.partijId;
              return (
                <li key={r.partijId}>
                  <button
                    type="button"
                    onClick={() => onPartijKlik(r.partijId)}
                    data-testid={`gewogen-regel-${r.partijId}`}
                    className={`hover-elevate w-full flex items-center gap-3 px-4 py-2.5 text-left ${
                      actief ? "bg-accent" : ""
                    }`}
                  >
                    <span className="w-6 font-mono text-[13px] text-muted-foreground tabular-nums">
                      {i + 1}
                    </span>
                    {ref ? (
                      <Diamond className="h-3.5 w-3.5 shrink-0" style={{ color: accent }} fill={accent} />
                    ) : (
                      <span
                        className="inline-block h-2.5 w-2.5 rounded-full shrink-0 ring-1 ring-black/10"
                        style={{ backgroundColor: accent }}
                      />
                    )}
                    <span className="flex-1 text-[15px]">
                      {r.partij.naam}
                      {ref && (
                        <span className="ml-2 text-[10px] uppercase tracking-wide font-semibold" style={{ color: accent }}>
                          ref
                        </span>
                      )}
                    </span>
                    <span
                      className={`font-mono text-[15px] font-semibold tabular-nums ${r.gewogen >= 0 ? "text-positief" : "text-negatief"}`}
                    >
                      {fmtGetal(r.gewogen)}
                    </span>
                  </button>
                </li>
              );
            })}
          </ol>
        </div>
      )}
    </div>
  );
}
