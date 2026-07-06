import { useEffect, useState, useCallback } from "react";

export type Orde = "1e_orde" | "2e_orde" | "3e_orde";

export interface AppState {
  sector: string | null;
  weights: Record<string, number>; // sectorId -> 0..100 (genormaliseerd elders)
  partij: string | null;
}

const EMPTY: AppState = { sector: null, weights: {}, partij: null };

/**
 * Wouter gebruikt de hash voor routing (#/...). Wij hangen onze applicatie-state
 * als query-string achter dat route-pad: bv. "#/?sector=S5&weights=S5:60,S15:40&partij=VVD".
 * Zo blijft de pagina deelbaar en compatibel met de hash-router.
 */
function parseHash(): AppState {
  const hash = window.location.hash.replace(/^#/, ""); // "/?sector=..."
  const qIndex = hash.indexOf("?");
  if (qIndex === -1) return { ...EMPTY };
  const params = new URLSearchParams(hash.slice(qIndex + 1));

  const sector = params.get("sector");
  const partij = params.get("partij");

  const weights: Record<string, number> = {};
  const weightsRaw = params.get("weights");
  if (weightsRaw) {
    for (const pair of weightsRaw.split(",")) {
      const [sid, val] = pair.split(":");
      const n = Number(val);
      if (sid && Number.isFinite(n)) weights[sid] = n;
    }
  }

  return {
    sector: sector || null,
    weights,
    partij: partij || null,
  };
}

function serialize(state: AppState): string {
  const params = new URLSearchParams();
  if (state.sector) params.set("sector", state.sector);
  const weightKeys = Object.keys(state.weights);
  if (weightKeys.length > 0) {
    params.set(
      "weights",
      weightKeys.map((k) => `${k}:${Math.round(state.weights[k])}`).join(","),
    );
  }
  if (state.partij) params.set("partij", state.partij);
  const qs = params.toString();
  return qs ? `/?${qs}` : "/";
}

export function useHashState(): [AppState, (next: Partial<AppState>) => void] {
  const [state, setState] = useState<AppState>(() => parseHash());

  useEffect(() => {
    const onHash = () => setState(parseHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  const update = useCallback((next: Partial<AppState>) => {
    setState((prev) => {
      const merged: AppState = { ...prev, ...next };
      const path = serialize(merged);
      const newHash = `#${path}`;
      if (window.location.hash !== newHash) {
        // pushState voorkomt een extra hashchange-loop; we updaten state direct
        window.history.replaceState(null, "", newHash);
      }
      return merged;
    });
  }, []);

  return [state, update];
}

/** Smooth scroll naar een element-id, met inachtneming van prefers-reduced-motion. */
export function scrollToId(id: string) {
  const el = document.getElementById(id);
  if (!el) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
}
