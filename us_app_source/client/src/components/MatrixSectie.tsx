import { useState } from "react";
import { Diamond } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useIsMobile } from "@/hooks/use-mobile";
import {
  partijIds,
  partijen,
  sectoren,
  sectorIds,
  partijAccent,
  isReferentie,
  getUitkomst,
  heatmapKleur,
  heatmapTekstKleur,
  ordeLabels,
  fmtGetal,
  type OrdeKey,
} from "@/lib/data";

interface Props {
  /** Klik op een cel: selecteer die sector en scroll naar de ranglijst. */
  onCelKlik: (sectorId: string) => void;
}

const ORDE_TABS: { key: OrdeKey; label: string }[] = [
  { key: "1e_orde", label: "1e orde (jaar 1\u20112)" },
  { key: "2e_orde", label: "2e orde (jaar 3)" },
  { key: "3e_orde", label: "3e orde (jaar 5\u201110)" },
];

export function MatrixSectie({ onCelKlik }: Props) {
  // Standaard op 3e orde \u2014 meest impactvol.
  const [orde, setOrde] = useState<OrdeKey>("3e_orde");
  const isMobile = useIsMobile();

  return (
    <div>
      {/* Tabs / dropdown */}
      {isMobile ? (
        <div className="mb-4">
          <label className="block text-[12px] uppercase tracking-[0.14em] text-muted-foreground mb-1.5">
            Tijdsorde
          </label>
          <Select value={orde} onValueChange={(v) => setOrde(v as OrdeKey)}>
            <SelectTrigger data-testid="select-orde-mobiel" className="w-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {ORDE_TABS.map((t) => (
                <SelectItem key={t.key} value={t.key}>
                  {t.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      ) : (
        <div className="mb-5 inline-flex rounded-md border border-border bg-background/60 p-1">
          {ORDE_TABS.map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => setOrde(t.key)}
              data-testid={`tab-orde-${t.key}`}
              className={`px-4 py-2 text-[13px] rounded-[4px] transition-colors ${
                orde === t.key
                  ? "bg-foreground text-background font-medium"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      )}

      {/* Heatmap */}
      <div className="overflow-x-auto rounded-md border border-card-border bg-card -mx-1 sm:mx-0">
        <table className="border-collapse text-[12px]" data-testid="matrix-tabel">
          <thead>
            <tr>
              <th className="sticky left-0 z-20 bg-card border-b border-r border-card-border px-3 py-2 text-left font-semibold min-w-[140px]">
                Partij
              </th>
              {sectorIds.map((sid) => (
                <th
                  key={sid}
                  className="border-b border-card-border px-1 py-2 text-center font-mono font-medium text-muted-foreground min-w-[40px]"
                >
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <span className="cursor-default">{sid}</span>
                    </TooltipTrigger>
                    <TooltipContent>{sectoren[sid].naam}</TooltipContent>
                  </Tooltip>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {partijIds.map((pid) => {
              const p = partijen[pid];
              const ref = isReferentie(pid);
              const accent = partijAccent[pid] ?? "#6b6258";
              return (
                <tr key={pid} className="group">
                  <th
                    scope="row"
                    className="sticky left-0 z-10 bg-card border-r border-card-border px-3 py-1.5 text-left font-normal whitespace-nowrap"
                    style={ref ? { background: `${accent}14` } : undefined}
                  >
                    <span className="flex items-center gap-2">
                      {ref ? (
                        <Diamond className="h-3 w-3 shrink-0" style={{ color: accent }} fill={accent} />
                      ) : (
                        <span
                          className="inline-block h-2.5 w-2.5 rounded-full shrink-0 ring-1 ring-black/10"
                          style={{ backgroundColor: accent }}
                        />
                      )}
                      <span className={ref ? "font-medium" : ""} style={ref ? { color: accent } : undefined}>
                        {pid}
                      </span>
                      {ref && (
                        <span
                          className="text-[9px] uppercase tracking-wide font-semibold rounded px-1 py-0.5"
                          style={{ color: accent, background: `${accent}1f` }}
                        >
                          ref
                        </span>
                      )}
                    </span>
                  </th>
                  {sectorIds.map((sid) => {
                    const u = getUitkomst(pid, sid);
                    const val = u ? u[orde] : 0;
                    return (
                      <td
                        key={sid}
                        className="text-center px-0.5 py-0 border-b border-card-border/40"
                      >
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <button
                              type="button"
                              onClick={() => onCelKlik(sid)}
                              data-testid={`cel-${pid}-${sid}`}
                              className="w-full h-7 tabular-nums font-mono text-[11px] cursor-pointer transition-transform hover:scale-[1.18] hover:relative hover:z-10 hover:ring-2 hover:ring-foreground/40"
                              style={{
                                backgroundColor: heatmapKleur(val, orde),
                                color: heatmapTekstKleur(val, orde),
                              }}
                            >
                              {Math.round(val)}
                            </button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <span className="font-medium">{p.naam}</span> &times;{" "}
                            {sectoren[sid].naam}
                            <br />
                            {ordeLabels[orde].titel}: <span className="font-mono">{fmtGetal(val)}</span>
                          </TooltipContent>
                        </Tooltip>
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Legenda */}
      <div className="mt-4 flex flex-wrap items-center gap-x-6 gap-y-2 text-[12px] text-muted-foreground">
        <span className="flex items-center gap-2">
          <span className="inline-flex">
            <span className="h-3 w-5" style={{ background: "rgba(182,55,44,0.6)" }} />
            <span className="h-3 w-5" style={{ background: "rgba(182,55,44,0.25)" }} />
            <span className="h-3 w-5 border border-card-border" style={{ background: "transparent" }} />
            <span className="h-3 w-5" style={{ background: "rgba(41,102,71,0.25)" }} />
            <span className="h-3 w-5" style={{ background: "rgba(41,102,71,0.6)" }} />
          </span>
          Verzwakkend &larr; neutraal &rarr; versterkend
        </span>
        <span className="flex items-center gap-1.5">
          <Diamond className="h-3 w-3" style={{ color: "#9a7b1f" }} fill="#9a7b1f" /> VMP /
          <Diamond className="h-3 w-3 ml-1" style={{ color: "#1f6b4e" }} fill="#1f6b4e" /> CARB =
          referentiemodellen
        </span>
        <span>Klik een cel om de ranglijst voor die sector te openen.</span>
      </div>
    </div>
  );
}
