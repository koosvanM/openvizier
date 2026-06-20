#!/usr/bin/env python3
"""
Voeg op DE/EN/RU voorpagina's de proloog-card + 2 Brussel-artikel-blokken toe,
direct vóór de 'Alle .. stukken →' link.
Identiek qua opbouw aan NL voorpagina (verplaatst), maar hier ALLEEN toegevoegd
(er is geen anti-immuun-cluster om eerst te verplaatsen).
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
MARKER = "<!-- voorpagina-proloog-onderaan v1 -->"

LANGS = {
    "de": {
        "path": "de/index.html",
        "wo_dir": "was-aufkommt",
        "label_sectie": "Die Diagnose — am Ende",
        "h2_sectie": "Erst das Bild. Dann die Anwendung.",
        "lead_sectie": "Unten auf dieser Seite steht ein ruhiger Prolog, der die medizinische Metapher erklärt, gefolgt von zwei Artikeln, die das Bild konkret auf die Brüsseler Wirklichkeit anwenden.",
        "proloog_slug": "die-metapher-autoimmunkrankheit.html",
        "proloog_label": "Prolog · das Bild",
        "proloog_titel": "Ein Staat mit einer Autoimmunkrankheit",
        "proloog_lead": "Ein Bild zum Mitdenken, nicht zum Zuschlagen. Ruhig erklärt, in einem Zug zu folgen — die Metapher, mit der die beiden Brüssel-Stücke gelesen werden können.",
        "proloog_cta": "Lesen Sie den Prolog →",
        "art1_slug": "die-anti-immunkrankheit-bruessels.html",
        "art1_tag": "★★★ Lead Brüssel · 19. Juni 2026 · Europa wird arm",
        "art1_titel": "Die Anti-Immunkrankheit Brüssels macht uns arm",
        "art1_lead": "CBAM, ETS und Pillar Two — drei Angriffe gleichzeitig. Die BiCRS-Route wird ignoriert.",
        "art1_cta": "Lesen Sie die Brüsseler Diagnose →",
        "art2_slug": "sie-toeten-ihre-lebensadern-bruessel.html",
        "art2_tag": "★★ Diagnose Brüssel · grundlegender Artikel",
        "art2_titel": "Sie töten ihre Lebensadern",
        "art2_lead": "Die Diagnose in ihrer ganzen Breite: sechs Sektoren, eine Führung, eine Anti-Immunkrankheit.",
        "art2_cta": "Lesen Sie die Sektor-Diagnose →",
    },
    "en": {
        "path": "en/index.html",
        "wo_dir": "what-surfaces",
        "label_sectie": "The diagnosis — at the end",
        "h2_sectie": "First the image. Then the application.",
        "lead_sectie": "At the bottom of this page is a calm prologue explaining the medical metaphor, followed by two articles that apply the image concretely to the Brussels reality.",
        "proloog_slug": "the-metaphor-autoimmune-disease.html",
        "proloog_label": "Prologue · the image",
        "proloog_titel": "A state with an autoimmune disease",
        "proloog_lead": "An image to think with, not to strike with. Calmly explained, followable in one read — the metaphor with which the two Brussels pieces can be understood.",
        "proloog_cta": "Read the prologue →",
        "art1_slug": "the-anti-immune-disease-of-brussels.html",
        "art1_tag": "★★★ Lead Brussels · 19 June 2026 · Europe is becoming poor",
        "art1_titel": "The anti-immune disease of Brussels is making us poor",
        "art1_lead": "CBAM, ETS and Pillar Two — three attacks at once. The BiCRS route is ignored.",
        "art1_cta": "Read the Brussels diagnosis →",
        "art2_slug": "they-kill-their-lifelines-brussels.html",
        "art2_tag": "★★ Diagnosis Brussels · underlying article",
        "art2_titel": "They kill their lifelines",
        "art2_lead": "The diagnosis in its full breadth: six sectors, one leadership, one anti-immune disease.",
        "art2_cta": "Read the sector diagnosis →",
    },
    "ru": {
        "path": "ru/index.html",
        "wo_dir": "chto-vsplyvaet",
        "label_sectie": "Диагноз — в конце",
        "h2_sectie": "Сначала образ. Потом применение.",
        "lead_sectie": "Внизу этой страницы — спокойный пролог, объясняющий медицинскую метафору, за ним два материала, которые применяют этот образ к реальности Брюсселя.",
        "proloog_slug": "metafora-autoimmunnoy-bolezni.html",
        "proloog_label": "Пролог · образ",
        "proloog_titel": "Государство с аутоиммунной болезнью",
        "proloog_lead": "Образ, с которым можно думать, а не бить. Спокойно объяснён, читается в один заход — метафора, через которую можно прочесть два следующих материала о Брюсселе.",
        "proloog_cta": "Читать пролог →",
        "art1_slug": "anti-immunnaya-bolezn-bryusselya.html",
        "art1_tag": "★★★ Главный материал · Брюссель · 19 июня 2026 · Европа беднеет",
        "art1_titel": "Анти-иммунная болезнь Брюсселя делает нас беднее",
        "art1_lead": "CBAM, ETS и Pillar Two — три удара одновременно. Маршрут BiCRS игнорируется.",
        "art1_cta": "Читать брюссельский диагноз →",
        "art2_slug": "oni-ubivayut-svoi-zhiznennye-arterii-bryussel.html",
        "art2_tag": "★★ Диагноз · Брюссель · базовая статья",
        "art2_titel": "Они убивают свои жизненные артерии",
        "art2_lead": "Диагноз во всей полноте: шесть секторов, одно руководство, одна анти-иммунная болезнь.",
        "art2_cta": "Читать секторный диагноз →",
    },
}

def build_cluster(t):
    return f'''
{MARKER}
<section style="grid-column: 1 / -1; margin:3rem auto 1rem auto; padding:0 1.25rem; text-align:center;">
  <p style="font-size:0.8rem;letter-spacing:0.12em;text-transform:uppercase;color:#5a7a78;margin:0 0 0.4rem 0;font-family:Georgia,serif;font-weight:600;">{t["label_sectie"]}</p>
  <h2 style="font-family:Georgia,serif;font-size:clamp(1.7rem,3.6vw,2.3rem);color:#1a1a1a;margin:0 0 0.7rem 0;font-weight:700;font-style:italic;">{t["h2_sectie"]}</h2>
  <p style="font-family:Georgia,serif;font-style:italic;color:#4a5263;max-width:720px;margin:0 auto;line-height:1.6;">{t["lead_sectie"]}</p>
</section>

<a href="{t["wo_dir"]}/{t["proloog_slug"]}" style="grid-column: 1 / -1; display:block;text-decoration:none;color:inherit;background:#eef1e8;border:1px solid #c8d2bb;border-left:5px solid #5a7a52;padding:2rem 2rem;margin:0 auto 2rem auto;max-width:960px;border-radius:4px;transition:box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 6px 18px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
  <p style="font-size:0.78rem;letter-spacing:0.12em;text-transform:uppercase;color:#5a7a52;margin:0 0 0.5rem 0;font-family:Georgia,serif;font-weight:600;">{t["proloog_label"]}</p>
  <h3 style="font-family:Georgia,serif;font-size:clamp(1.5rem,3vw,2rem);color:#1a1a1a;margin:0 0 0.7rem 0;font-weight:700;line-height:1.2;">{t["proloog_titel"]}</h3>
  <p style="font-family:Georgia,serif;font-style:italic;color:#3a4a35;margin:0 0 0.8rem 0;font-size:1.05rem;line-height:1.6;">{t["proloog_lead"]}</p>
  <span style="display:inline-block;color:#5a7a52;font-weight:700;border-bottom:1px solid #5a7a52;padding-bottom:1px;font-size:0.95rem;font-family:Georgia,serif;">{t["proloog_cta"]}</span>
</a>

<a href="{t["wo_dir"]}/{t["art1_slug"]}" class="home-wo__rij-breed" style="background:#0a1428;color:#f5f0e6;padding:0;border-left:6px solid #ffd700;display:block;text-decoration:none;margin-bottom:1.5rem;">
  <div style="padding:2rem 1.75rem;">
    <p style="color:#ffd700;font-weight:700;letter-spacing:0.18em;font-size:0.85rem;margin:0 0 0.8rem 0;text-transform:uppercase;font-family:Georgia,serif;">{t["art1_tag"]}</p>
    <h3 style="color:#f5f0e6;font-size:clamp(1.7rem,4vw,2.3rem);margin:0 0 0.7rem 0;line-height:1.15;font-weight:700;font-family:Georgia,serif;">{t["art1_titel"]}</h3>
    <p style="color:#e8efe9;font-size:1.05rem;line-height:1.6;margin:0 0 1rem 0;font-family:Georgia,serif;">{t["art1_lead"]}</p>
    <span style="color:#ffd700;font-weight:700;border-bottom:1px solid #ffd700;padding-bottom:1px;font-family:Georgia,serif;">{t["art1_cta"]}</span>
  </div>
</a>

<a href="{t["wo_dir"]}/{t["art2_slug"]}" class="home-wo__rij-breed" style="background:#3a0a14;color:#f5f0e6;padding:0;border-left:5px solid #7a1224;display:block;text-decoration:none;margin-bottom:1.5rem;">
  <div style="padding:2rem 1.75rem;">
    <p style="color:#ffd8c8;font-weight:700;letter-spacing:0.18em;font-size:0.85rem;margin:0 0 0.8rem 0;text-transform:uppercase;font-family:Georgia,serif;">{t["art2_tag"]}</p>
    <h3 style="color:#f5f0e6;font-size:clamp(1.6rem,3.8vw,2.2rem);margin:0 0 0.5rem 0;line-height:1.2;font-weight:700;font-family:Georgia,serif;">{t["art2_titel"]}</h3>
    <p style="color:#e8efe9;font-size:1.02rem;line-height:1.6;margin:0 0 1rem 0;font-family:Georgia,serif;">{t["art2_lead"]}</p>
    <span style="color:#ffd8c8;font-weight:700;border-bottom:1px solid #ffd8c8;padding-bottom:1px;font-family:Georgia,serif;">{t["art2_cta"]}</span>
  </div>
</a>
'''

changed = []
skipped = []
for lang, t in LANGS.items():
    p = REPO / t["path"]
    html = p.read_text(encoding="utf-8")
    if MARKER in html:
        skipped.append(f"al toegevoegd: {p}")
        continue
    m = re.search(r'\s*<p class="home-wo__naar_alles">', html)
    if not m:
        skipped.append(f"naar_alles niet gevonden: {p}")
        continue
    insert_idx = m.start()
    cluster = build_cluster(t)
    new = html[:insert_idx] + cluster + html[insert_idx:]
    p.write_text(new, encoding="utf-8")
    changed.append(t["path"])

print("OK:", changed)
print("SKIPPED:", skipped)
