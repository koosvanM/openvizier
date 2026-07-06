import { jsPDF } from "jspdf";
import type { Uitkomst, Partij } from "./data";
import { ordeLabels } from "./data";

const INK = "#2b2723";
const MUTED = "#6b6258";
const GREEN = "#2f5a3f";
const RED = "#9c352a";
const CREAM = "#f6f1e6";
const LINE = "#cfc6b4";

// jsPDF's standaard fonts (Helvetica/Times) ondersteunen alleen WinAnsi.
// Vervang Unicode-tekens die buiten dat bereik vallen door veilige equivalenten,
// anders raakt de letterafstand corrupt.
function san(s: string): string {
  return s
    .replace(/\u2011/g, "-") // non-breaking hyphen
    .replace(/\u2013/g, "-") // en dash
    .replace(/\u2010/g, "-")
    .replace(/\u2212/g, "-") // minus sign
    .replace(/\u00a0/g, " ") // non-breaking space
    .replace(/\u03a3/g, "som ") // Sigma
    .replace(/\u221a/g, "wortel") // sqrt
    .replace(/\u00d7/g, "x") // times
    .replace(/\u00b2/g, "2") // superscript 2
    .replace(/\u2032/g, "'"); // prime
}

function fmt(n: number): string {
  const r = Math.round(n);
  return (r > 0 ? "+" : "") + r.toLocaleString("nl-NL");
}

function vandaag(): string {
  return new Date().toLocaleDateString("nl-NL", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function genereerRapport(
  partijId: string,
  partij: Partij,
  sectorId: string,
  u: Uitkomst,
) {
  const doc = new jsPDF({ unit: "pt", format: "a4" });
  const W = doc.internal.pageSize.getWidth();
  const H = doc.internal.pageSize.getHeight();
  const M = 48; // margin
  const CW = W - M * 2;
  let y = 0;

  const setColor = (hex: string) => doc.setTextColor(hex);

  // Gesaniteerde text-helpers (vervangen alle directe doc.text-aanroepen).
  const T = (txt: string | string[], x: number, y2: number, opts?: any) => {
    const v = Array.isArray(txt) ? txt.map(san) : san(txt);
    doc.text(v as any, x, y2, opts);
  };
  const SPLIT = (txt: string, w: number): string[] =>
    doc.splitTextToSize(san(txt), w);

  // ---- paper background per page ----
  const paintBg = () => {
    doc.setFillColor(CREAM);
    doc.rect(0, 0, W, H, "F");
  };

  const footer = (page: number) => {
    doc.setDrawColor(LINE);
    doc.setLineWidth(0.6);
    doc.line(M, H - 40, W - M, H - 40);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    setColor(MUTED);
    T("De Gevolgenkaart \u00b7 gevolgenkaart.nl", M, H - 28);
    T(`Pagina ${page}`, W - M, H - 28, { align: "right" });
    T(
      "Geen partij-advies, alleen feiten.",
      M,
      H - 18,
    );
  };

  // ===================== PAGE 1 =====================
  paintBg();
  y = M;

  // Logo mark (simple drawn eye + grid)
  const lx = M + 11,
    ly = y + 6,
    r = 11;
  doc.setDrawColor(INK);
  doc.setLineWidth(1.4);
  // eye outline (ellipse)
  doc.ellipse(lx, ly, r, r * 0.62, "S");
  doc.setLineWidth(1.1);
  doc.circle(lx, ly, 5.4, "S");
  doc.setLineWidth(0.7);
  doc.line(lx, ly - 5.4, lx, ly + 5.4);
  doc.line(lx - 5.4, ly, lx + 5.4, ly);
  doc.setFillColor(RED);
  doc.circle(lx, ly, 1.8, "F");

  doc.setFont("times", "bold");
  doc.setFontSize(15);
  setColor(INK);
  T("De Gevolgenkaart", M + 30, y + 4);
  doc.setFont("helvetica", "normal");
  doc.setFontSize(8);
  setColor(MUTED);
  T("GEVOLGENKAART.NL", M + 30, y + 15);
  T(vandaag(), W - M, y + 4, { align: "right" });
  T("Persoonlijk rapport", W - M, y + 15, { align: "right" });

  y += 34;
  doc.setDrawColor(INK);
  doc.setLineWidth(1.6);
  doc.line(M, y, W - M, y);
  y += 30;

  // Title block
  doc.setFont("times", "normal");
  doc.setFontSize(11);
  setColor(MUTED);
  T(`Persoonlijk rapport voor: ${u.sector_naam}`, M, y);
  y += 24;
  doc.setFont("times", "bold");
  doc.setFontSize(21);
  setColor(INK);
  const titel = `Onder ${partij.naam}`;
  T(titel, M, y);
  y += 20;
  doc.setFont("helvetica", "normal");
  doc.setFontSize(9.5);
  setColor(MUTED);
  const introTekst = partij.referentie
    ? `Dit is een referentiemodel (niet op het stembiljet). Deze gevolgenkaart toont hoe een consequent doorgevoerd ${partij.naam} beleid doorwerkt voor wie actief is in de sector ${u.sector_naam}. De effecten zijn berekend over drie tijdsordes en samengesteld uit ${u.aantal_actieve_elementen} actieve beleidselementen.`
    : `Deze gevolgenkaart toont hoe een stem op ${partij.naam} doorwerkt voor wie actief is in de sector ${u.sector_naam}. De effecten zijn berekend over drie tijdsordes en samengesteld uit ${u.aantal_actieve_elementen} actieve beleidselementen.`;
  const intro = SPLIT(introTekst, CW);
  T(intro, M, y);
  y += intro.length * 12 + 14;

  // Three order cards
  const cardW = (CW - 24) / 3;
  const orders: { key: keyof typeof ordeLabels; val: number }[] = [
    { key: "1e_orde", val: u["1e_orde"] },
    { key: "2e_orde", val: u["2e_orde"] },
    { key: "3e_orde", val: u["3e_orde"] },
  ];
  const cardY = y;
  const cardH = 78;
  orders.forEach((o, i) => {
    const cx = M + i * (cardW + 12);
    doc.setFillColor("#ffffff");
    doc.setDrawColor(LINE);
    doc.setLineWidth(0.8);
    doc.roundedRect(cx, cardY, cardW, cardH, 4, 4, "FD");
    const meta = ordeLabels[o.key];
    doc.setFont("helvetica", "bold");
    doc.setFontSize(8);
    setColor(MUTED);
    T(meta.titel.toUpperCase(), cx + 12, cardY + 18);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    T(meta.periode, cx + 12, cardY + 30);
    doc.setFont("times", "bold");
    doc.setFontSize(22);
    setColor(o.val >= 0 ? GREEN : RED);
    T(fmt(o.val), cx + 12, cardY + 58);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7);
    setColor(MUTED);
    T(meta.omschrijving, cx + 12, cardY + 70);
  });
  y = cardY + cardH + 26;

  // Versterkende elementen
  const drawList = (
    titel: string,
    items: typeof u.top_positief,
    color: string,
    startY: number,
  ): number => {
    let yy = startY;
    doc.setFont("times", "bold");
    doc.setFontSize(12);
    setColor(INK);
    T(titel, M, yy);
    yy += 6;
    doc.setDrawColor(color);
    doc.setLineWidth(2);
    doc.line(M, yy, M + 60, yy);
    yy += 16;
    doc.setFontSize(9);
    items.forEach((it, idx) => {
      doc.setFont("helvetica", "bold");
      setColor(color);
      T(fmt(it.bijdrage), M, yy);
      doc.setFont("helvetica", "normal");
      setColor(INK);
      const naam = SPLIT(`${it.naam}`, CW - 110);
      T(naam[0], M + 48, yy);
      doc.setFontSize(7.5);
      setColor(MUTED);
      T(`#${it.element_id}`, W - M, yy, { align: "right" });
      doc.setFontSize(9);
      yy += 18;
    });
    return yy + 6;
  };

  y = drawList("Vijf sterkst versterkende elementen", u.top_positief, GREEN, y);
  y = drawList("Vijf sterkst verzwakkende elementen", u.top_negatief, RED, y);

  footer(1);

  // ===================== PAGE 2 =====================
  doc.addPage();
  paintBg();
  y = M;
  doc.setFont("times", "bold");
  doc.setFontSize(16);
  setColor(INK);
  T("Methodologie", M, y);
  y += 8;
  doc.setDrawColor(INK);
  doc.setLineWidth(1.4);
  doc.line(M, y, W - M, y);
  y += 22;

  const para = (kop: string, tekst: string) => {
    doc.setFont("times", "bold");
    doc.setFontSize(11);
    setColor(INK);
    T(kop, M, y);
    y += 15;
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9.5);
    setColor("#3a352e");
    const lines = SPLIT(tekst, CW);
    T(lines, M, y);
    y += lines.length * 13 + 16;
  };

  para(
    "De drie ordes",
    "Elk beleidselement werkt niet \u00e9\u00e9nmalig maar in cascade door. De 1e orde (jaar 1\u20112) vangt de directe, mechanische effecten: een tarief gaat omhoog of omlaag, een regeling verschijnt of verdwijnt. De 2e orde (jaar 3) telt de gedragsreacties mee: investeringen die verschuiven, talent dat blijft of vertrekt, bedrijven die op- of afschalen. De 3e orde (jaar 5\u201110) toont de structurele uitkomst wanneer die reacties zich hebben opgestapeld in de productieve basis van het land.",
  );
  para(
    "De negen filters",
    "Ieder element wordt gescoord op negen macrofilters: Netto Economisch Productiekapitaal, Bedrijvigheid, Investeringsklimaat, Talentmobiliteit, Begrotingshouding, Energie-autonomie, Demografische houdbaarheid, Institutionele kwaliteit en Wereldhandel-positie. De cascade-waarde van een element is sign(som F') x wortel(som van F'-kwadraten), met F' de afwijking van neutraal (5). De bijdrage weegt die cascade met de positie en de programmatische intensiteit van de partij.",
  );
  para(
    "Empirische verankering",
    "De cascade-co\u00ebffici\u00ebnten zijn geijkt aan historische natuurlijke experimenten waar beleid in vergelijkbare richting de productieve basis raakte. Twee referentiecasussen dragen het zwaarst: Argenti\u00eb (herhaalde kapitaalvlucht, vermogensheffingen en prijscontroles met meetbare krimp van de productieve basis) en Zuid-Afrika (institutionele erosie, brain drain van hooggeschoolden en desinvestering). Deze casussen kalibreren de orde-op-orde versterkingsfactoren \u2014 zij voorspellen geen exacte euro's, maar de richting en de relatieve zwaarte.",
  );
  para(
    "Wat de cijfers wel en niet zijn",
    "De getallen zijn relatieve cascade-indexpunten, geen euro-bedragen en geen koopkrachtplaatjes. Een hoger negatief getal betekent een zwaardere structurele verzwakking voor uw sector; een hoger positief getal een sterkere versterking. De kaart vergelijkt geen partijen onderling en geeft geen stemadvies \u2014 zij maakt de cascade van \u00e9\u00e9n keuze zichtbaar.",
  );

  // Disclaimer box
  doc.setFillColor("#efe7d6");
  doc.setDrawColor(LINE);
  doc.setLineWidth(0.8);
  const dbH = 64;
  doc.roundedRect(M, y, CW, dbH, 4, 4, "FD");
  doc.setFont("times", "bolditalic");
  doc.setFontSize(10);
  setColor(INK);
  T("Disclaimer", M + 14, y + 18);
  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  setColor("#4a443b");
  const dl = SPLIT(
    "Dit rapport is een journalistiek model, geen voorspelling en geen financieel of electoraal advies. Uitkomsten zijn modelmatig en afhankelijk van aannames over partijposities en cascade-co\u00ebffici\u00ebnten. Raadpleeg de volledige methodologie en brondata op gevolgenkaart.nl.",
    CW - 28,
  );
  T(dl, M + 14, y + 32);

  footer(2);

  const fileName = `gevolgenkaart-${partijId}-${sectorId}.pdf`;
  doc.save(fileName);
}
