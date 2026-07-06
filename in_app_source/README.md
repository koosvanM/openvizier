# es_app bron-archief

Deze map bevat de TypeScript-broncode van de Spanje-app (`/es/mapa-app/`),
gereconstrueerd uit sourcemaps op 2026-07-05 na verlies van de originele
sandbox. Doel: canoniek referentie-archief voor volgende sessies.

**Bevat NIET**: `package.json`, `vite.config.ts`, `tsconfig.json`,
`gevolgenkaart-persona.json`, `data.ts` (persona-data zit ingebakken
in de gebuilde bundel). Voor volledige rebuild moeten deze uit een
snapshot of nieuwe research-run worden aangevuld.

**Actuele patch**: v3.20.11 — orde-multipliers voor VMP en CARB in
`client/src/lib/levensloopEngine.ts` functie `partijGroeiPerJaar`:
- VMP: mult2=1.4, mult3=1.8
- CARB: mult2=1.8, mult3=2.5

Deze bronnen zijn ook direct in de gebuilde bundel
`/es/mapa-app/assets/PersonaFlow-*.js` gepatcht (regex-substitutie),
omdat een schone `npm run build` niet mogelijk was zonder
config-bestanden.
