#!/usr/bin/env python3
"""
Bouw alle talenring-pagina's opnieuw.

Hoofdkrant: 4 actieve talen (NL, DE, EN, RU)
Editie Europa: 8 actieve talen (NL, DE, EN, ES, FR, IT, PT, RU)

Voor NL/DE/EN/RU: toon alle 4 hoofdtalen + verwijzing naar Editie Europa met 8 talen.
Voor ES/FR/IT/PT: deze taal bestaat alleen in Editie Europa — duidelijke verwijzing.
"""
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Per UI-taal: alle teksten
T = {
    "nl": {
        "lang": "nl",
        "title": "Het Open Vizier — Kies een taal",
        "h1": "Het Open Vizier",
        "subtitle": "Kies een taal · Choose a language · Wählen Sie eine Sprache",
        "main_kop": "De volledige krant",
        "main_intro": "Beschikbaar in vier talen.",
        "ed0_kop": "Editie Europa",
        "ed0_intro": "De Brussel-campagne — beschikbaar in acht talen.",
        "available": "beschikbaar",
        "footer": "Onafhankelijke maandelijkse krant · Jacobus van Merksteijn · Malta",
    },
    "de": {
        "lang": "de",
        "title": "Het Open Vizier — Sprache wählen",
        "h1": "Het Open Vizier",
        "subtitle": "Wählen Sie eine Sprache · Choose a language · Kies een taal",
        "main_kop": "Die vollständige Zeitung",
        "main_intro": "Verfügbar in vier Sprachen.",
        "ed0_kop": "Ausgabe Europa",
        "ed0_intro": "Die Brüssel-Kampagne — verfügbar in acht Sprachen.",
        "available": "verfügbar",
        "footer": "Unabhängige Monatszeitung · Jacobus van Merksteijn · Malta",
    },
    "en": {
        "lang": "en",
        "title": "Het Open Vizier — Choose a language",
        "h1": "Het Open Vizier",
        "subtitle": "Choose a language · Wählen Sie eine Sprache · Kies een taal",
        "main_kop": "The complete newspaper",
        "main_intro": "Available in four languages.",
        "ed0_kop": "Edition Europe",
        "ed0_intro": "The Brussels campaign — available in eight languages.",
        "available": "available",
        "footer": "Independent monthly newspaper · Jacobus van Merksteijn · Malta",
    },
    "ru": {
        "lang": "ru",
        "title": "Het Open Vizier — Выберите язык",
        "h1": "Het Open Vizier",
        "subtitle": "Выберите язык · Choose a language · Kies een taal",
        "main_kop": "Полная газета",
        "main_intro": "Доступна на четырёх языках.",
        "ed0_kop": "Выпуск Европа",
        "ed0_intro": "Кампания о Брюсселе — доступна на восьми языках.",
        "available": "доступно",
        "footer": "Независимая ежемесячная газета · Jacobus van Merksteijn · Мальта",
    },
    "es": {
        "lang": "es",
        "title": "Het Open Vizier — Elija un idioma",
        "h1": "Het Open Vizier",
        "subtitle": "Elija un idioma · Choose a language · Kies een taal",
        "main_kop": "El periódico completo",
        "main_intro": "Disponible en cuatro idiomas (NL, DE, EN, RU).",
        "ed0_kop": "Edición Europa",
        "ed0_intro": "La campaña de Bruselas — disponible también en español.",
        "available": "disponible",
        "footer": "Periódico mensual independiente · Jacobus van Merksteijn · Malta",
    },
    "fr": {
        "lang": "fr",
        "title": "Het Open Vizier — Choisir une langue",
        "h1": "Het Open Vizier",
        "subtitle": "Choisir une langue · Choose a language · Kies een taal",
        "main_kop": "Le journal complet",
        "main_intro": "Disponible en quatre langues (NL, DE, EN, RU).",
        "ed0_kop": "Édition Europe",
        "ed0_intro": "La campagne de Bruxelles — disponible aussi en français.",
        "available": "disponible",
        "footer": "Journal mensuel indépendant · Jacobus van Merksteijn · Malte",
    },
    "it": {
        "lang": "it",
        "title": "Het Open Vizier — Scegli una lingua",
        "h1": "Het Open Vizier",
        "subtitle": "Scegli una lingua · Choose a language · Kies een taal",
        "main_kop": "Il giornale completo",
        "main_intro": "Disponibile in quattro lingue (NL, DE, EN, RU).",
        "ed0_kop": "Edizione Europa",
        "ed0_intro": "La campagna di Bruxelles — disponibile anche in italiano.",
        "available": "disponibile",
        "footer": "Giornale mensile indipendente · Jacobus van Merksteijn · Malta",
    },
    "pt": {
        "lang": "pt",
        "title": "Het Open Vizier — Escolha um idioma",
        "h1": "Het Open Vizier",
        "subtitle": "Escolha um idioma · Choose a language · Kies een taal",
        "main_kop": "O jornal completo",
        "main_intro": "Disponível em quatro idiomas (NL, DE, EN, RU).",
        "ed0_kop": "Edição Europa",
        "ed0_intro": "A campanha de Bruxelas — disponível também em português.",
        "available": "disponível",
        "footer": "Jornal mensal independente · Jacobus van Merksteijn · Malta",
    },
}

# 4 hoofdtalen (volledige krant)
MAIN_LANGS = [
    ("nl", "Nederlands", "Het Open Vizier", "🇳🇱"),
    ("de", "Deutsch",    "Das offene Visier", "🇩🇪"),
    ("en", "English",    "The Open Visor", "🇬🇧"),
    ("ru", "Русский",    "Открытое забрало", "🇷🇺"),
]

# 8 edities-talen
ED0_LANGS = [
    ("nl", "Nederlands", "Editie Europa", "🇳🇱", "editie-0/"),
    ("de", "Deutsch",    "Ausgabe Europa", "🇩🇪", "ausgabe-0/"),
    ("en", "English",    "Edition Europe", "🇬🇧", "edition-0/"),
    ("ru", "Русский",    "Выпуск Европа",  "🇷🇺", "vypusk-0/"),
    ("es", "Español",    "Edición Europa", "🇪🇸", "edicion-0/"),
    ("fr", "Français",   "Édition Europe", "🇫🇷", "edition-0/"),
    ("it", "Italiano",   "Edizione Europa","🇮🇹", "edizione-0/"),
    ("pt", "Português",  "Edição Europa",  "🇵🇹", "edicao-0/"),
]

def build_page(ui_lang):
    t = T[ui_lang]
    main_html = []
    for code, naam, ondertitel, vlag in MAIN_LANGS:
        href = f"../{code}/"
        main_html.append(f'''      <a href="{href}" class="taal">
        <div class="vlag">{vlag}</div>
        <div class="naam">{naam}</div>
        <div class="naam-ondertitel" style="font-size:0.85rem;font-weight:400;color:#cdc3a8;font-style:italic;">{ondertitel}</div>
        <div class="status" style="color:#a3b8a8">{t["available"]}</div>
      </a>''')
    ed0_html = []
    for code, naam, ondertitel, vlag, ed0_pad in ED0_LANGS:
        href = f"../{code}/{ed0_pad}"
        ed0_html.append(f'''      <a href="{href}" class="taal">
        <div class="vlag">{vlag}</div>
        <div class="naam">{naam}</div>
        <div class="naam-ondertitel" style="font-size:0.8rem;font-weight:400;color:#cdc3a8;font-style:italic;">{ondertitel}</div>
        <div class="status" style="color:#a3b8a8">{t["available"]}</div>
      </a>''')

    main_block = "\n".join(main_html)
    ed0_block = "\n".join(ed0_html)

    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<title>{t["title"]}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root{{--bg:#2e2519;--cream:#f6f1e6;--muted:#9a9385}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{min-height:100%;background:var(--bg);color:var(--cream);
    font-family:Georgia,"Times New Roman",serif;-webkit-font-smoothing:antialiased;
    overflow-x:hidden}}
  .stage{{min-height:100vh;display:flex;flex-direction:column;align-items:center;
         justify-content:flex-start;padding:48px 20px 60px;text-align:center}}
  .wapen{{width:min(28vw,180px);aspect-ratio:1/1.05;
         background:url('../assets/wat-opkomt/wapen_nova_democratia.png') center top/contain no-repeat;
         filter:drop-shadow(0 18px 50px rgba(0,0,0,.55));margin-bottom:18px}}
  h1{{font-size:clamp(1.6rem,3vw,2.4rem);font-weight:700;letter-spacing:1px;
     color:#f7efdc;margin-bottom:8px;line-height:1}}
  .ondertitel{{font-size:clamp(.9rem,1.2vw,1.05rem);font-style:italic;color:#cdc3a8;
              margin-bottom:36px;letter-spacing:.4px;max-width:700px}}
  .sectie-kop{{font-size:1.15rem;font-weight:700;color:#f7efdc;margin:34px 0 4px;
              letter-spacing:.4px;text-transform:uppercase}}
  .sectie-intro{{font-size:.95rem;font-style:italic;color:#cdc3a8;margin-bottom:18px;
                max-width:640px}}
  .talen-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
              gap:12px;max-width:880px;width:100%;margin-bottom:8px}}
  .talen-grid.acht{{grid-template-columns:repeat(auto-fit,minmax(150px,1fr));max-width:1050px}}
  .taal{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);
        border-radius:8px;padding:18px 12px;cursor:pointer;
        transition:all .25s ease;text-align:center;text-decoration:none;
        color:inherit;display:flex;flex-direction:column;align-items:center;gap:6px}}
  .taal:hover{{background:rgba(255,255,255,.10);border-color:rgba(255,255,255,.30);
              transform:translateY(-2px)}}
  .vlag{{font-size:1.9rem;line-height:1;filter:drop-shadow(0 2px 4px rgba(0,0,0,.3))}}
  .naam{{font-size:1.05rem;font-weight:700;letter-spacing:.3px;color:#f7efdc}}
  .status{{font-size:.7rem;font-style:italic;color:#9a9385;letter-spacing:.5px;
          text-transform:uppercase;margin-top:2px}}
  .footer{{margin-top:46px;font-size:.8rem;color:var(--muted);font-style:italic;
          max-width:600px;line-height:1.5}}
  hr.scheidslijn{{width:80%;max-width:520px;border:0;border-top:1px solid rgba(255,255,255,.10);
                  margin:34px auto 0}}
</style>
</head>
<body>
  <div class="stage">
    <div class="wapen"></div>
    <h1>{t["h1"]}</h1>
    <p class="ondertitel">{t["subtitle"]}</p>

    <p class="sectie-kop">{t["main_kop"]}</p>
    <p class="sectie-intro">{t["main_intro"]}</p>
    <div class="talen-grid vier">
{main_block}
    </div>

    <hr class="scheidslijn">

    <p class="sectie-kop">{t["ed0_kop"]}</p>
    <p class="sectie-intro">{t["ed0_intro"]}</p>
    <div class="talen-grid acht">
{ed0_block}
    </div>

    <p class="footer">{t["footer"]}</p>
  </div>
</body>
</html>
'''

# Schrijf per taal — bestandsnaam volgens conventie per taal
TARGET = {
    "nl": "nl/talenring.html",
    "de": "de/index-talenring.html",
    "en": "en/index-talenring.html",
    "ru": "ru/index-talenring.html",
    "es": "es/index-talenring.html",
    "fr": "fr/index-talenring.html",
    "it": "it/index-talenring.html",
    "pt": "pt/index-talenring.html",
}

changed = []
for ui_lang, rel in TARGET.items():
    path = REPO / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_page(ui_lang), encoding="utf-8")
    changed.append(rel)

# Ook NL behoeft een index-talenring.html spiegelpad (NL gebruikt 'talenring.html' maar voor uniformiteit ook deze)
nl_mirror = REPO / "nl/index-talenring.html"
nl_mirror.write_text(build_page("nl"), encoding="utf-8")
changed.append("nl/index-talenring.html")

print(f"=== Talenring herbouwd ({len(changed)}) ===")
for c in changed: print(" -", c)
