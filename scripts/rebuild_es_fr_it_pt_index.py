#!/usr/bin/env python3
"""
Bouw ES/FR/IT/PT voorpagina's opnieuw als landingpagina's
die helder en uitnodigend naar Editie Europa leiden,
met direct ook de twee Brussel-artikelen prominent.

Geen claim dat 'de rest in NL/DE/EN/RU is' — alleen wat in deze taal bestaat.
"""
from pathlib import Path

REPO = Path("/tmp/gh-repo")

T = {
    "es": {
        "lang": "es",
        "title": "Het Open Vizier — un periódico para pensar sin anteojeras",
        "meta": "La campaña sobre Bruselas en español — el periódico mensual independiente de Jacobus van Merksteijn.",
        "month": "junio 2026",
        "home_label": "Inicio",
        "ed0_label": "Edición Europa",
        "wo_label": "Lo que emerge",
        "delen_label": "Compartir",
        "lang_menu": "⌂ Idioma",
        "ed0_path": "edicion-0/",
        "wo_path": "lo-que-emerge/",
        "h1": "Bienvenido",
        "intro": "Esta versión española de Het Open Vizier contiene la <strong>campaña sobre Bruselas</strong>: la Edición Europa y los dos artículos centrales que describen, como diagnóstico, la enfermedad anti-inmune que empobrece al ciudadano europeo.",
        "ed0_kop": "Edición Europa",
        "ed0_lead": "La edición sobre Bruselas — análisis completo de los mecanismos de la UE que vacían el tejido productivo.",
        "ed0_cta": "Leer la Edición Europa →",
        "brussel_kop": "Los dos artículos centrales",
        "brussel_intro": "Un diagnóstico, no un ataque.",
        "art1_titel": "La enfermedad anti-inmune de Bruselas nos empobrece",
        "art1_lead": "CBAM, ETS y Pillar Two — tres ataques al mismo tiempo. La ruta BiCRS/Etanol es ignorada.",
        "art1_path": "lo-que-emerge/la-enfermedad-anti-inmune-de-bruselas.html",
        "art2_titel": "Matan sus arterias vitales",
        "art2_lead": "El diagnóstico en toda su amplitud: seis sectores, una dirigencia, una enfermedad anti-inmune.",
        "art2_path": "lo-que-emerge/matan-sus-arterias-vitales-bruselas.html",
        "andere_kop": "El periódico completo",
        "andere_intro": "Het Open Vizier en su totalidad — siete ediciones, dosieres e investigación — está disponible en cuatro idiomas:",
        "footer": "Periódico mensual independiente · Jacobus van Merksteijn · Malta · junio 2026",
    },
    "fr": {
        "lang": "fr",
        "title": "Het Open Vizier — un journal pour penser sans œillères",
        "meta": "La campagne sur Bruxelles en français — le journal mensuel indépendant de Jacobus van Merksteijn.",
        "month": "juin 2026",
        "home_label": "Accueil",
        "ed0_label": "Édition Europe",
        "wo_label": "Ce qui émerge",
        "delen_label": "Partager",
        "lang_menu": "⌂ Langue",
        "ed0_path": "edition-0/",
        "wo_path": "ce-qui-emerge/",
        "h1": "Bienvenue",
        "intro": "Cette version française de Het Open Vizier contient la <strong>campagne sur Bruxelles</strong> : l'Édition Europe et les deux articles centraux qui décrivent, en tant que diagnostic, la maladie anti-immunitaire qui appauvrit le citoyen européen.",
        "ed0_kop": "Édition Europe",
        "ed0_lead": "L'édition sur Bruxelles — analyse complète des mécanismes de l'UE qui vident le tissu productif.",
        "ed0_cta": "Lire l'Édition Europe →",
        "brussel_kop": "Les deux articles centraux",
        "brussel_intro": "Un diagnostic, pas une attaque.",
        "art1_titel": "La maladie anti-immunitaire de Bruxelles nous appauvrit",
        "art1_lead": "CBAM, ETS et Pillar Two — trois attaques simultanées. La route BiCRS/Éthanol est ignorée.",
        "art1_path": "ce-qui-emerge/la-maladie-anti-immunitaire-de-bruxelles.html",
        "art2_titel": "Ils tuent leurs artères vitales",
        "art2_lead": "Le diagnostic dans toute son ampleur : six secteurs, une direction, une maladie anti-immunitaire.",
        "art2_path": "ce-qui-emerge/ils-tuent-leurs-arteres-vitales-bruxelles.html",
        "andere_kop": "Le journal complet",
        "andere_intro": "Het Open Vizier dans son intégralité — sept éditions, dossiers et recherche — est disponible en quatre langues :",
        "footer": "Journal mensuel indépendant · Jacobus van Merksteijn · Malte · juin 2026",
    },
    "it": {
        "lang": "it",
        "title": "Het Open Vizier — un giornale per pensare senza paraocchi",
        "meta": "La campagna su Bruxelles in italiano — il giornale mensile indipendente di Jacobus van Merksteijn.",
        "month": "giugno 2026",
        "home_label": "Home",
        "ed0_label": "Edizione Europa",
        "wo_label": "Ciò che emerge",
        "delen_label": "Condividi",
        "lang_menu": "⌂ Lingua",
        "ed0_path": "edizione-0/",
        "wo_path": "cio-che-emerge/",
        "h1": "Benvenuto",
        "intro": "Questa versione italiana di Het Open Vizier contiene la <strong>campagna su Bruxelles</strong>: l'Edizione Europa e i due articoli centrali che descrivono, come diagnosi, la malattia anti-immune che impoverisce il cittadino europeo.",
        "ed0_kop": "Edizione Europa",
        "ed0_lead": "L'edizione su Bruxelles — analisi completa dei meccanismi dell'UE che svuotano il tessuto produttivo.",
        "ed0_cta": "Leggi l'Edizione Europa →",
        "brussel_kop": "I due articoli centrali",
        "brussel_intro": "Una diagnosi, non un attacco.",
        "art1_titel": "La malattia anti-immune di Bruxelles ci impoverisce",
        "art1_lead": "CBAM, ETS e Pillar Two — tre attacchi contemporaneamente. La rotta BiCRS/Etanolo è ignorata.",
        "art1_path": "cio-che-emerge/la-malattia-anti-immune-di-bruxelles.html",
        "art2_titel": "Uccidono le loro arterie vitali",
        "art2_lead": "La diagnosi in tutta la sua ampiezza: sei settori, una dirigenza, una malattia anti-immune.",
        "art2_path": "cio-che-emerge/uccidono-le-loro-arterie-vitali-bruxelles.html",
        "andere_kop": "Il giornale completo",
        "andere_intro": "Het Open Vizier nella sua interezza — sette edizioni, dossier e ricerche — è disponibile in quattro lingue:",
        "footer": "Giornale mensile indipendente · Jacobus van Merksteijn · Malta · giugno 2026",
    },
    "pt": {
        "lang": "pt",
        "title": "Het Open Vizier — um jornal para pensar sem antolhos",
        "meta": "A campanha sobre Bruxelas em português — o jornal mensal independente de Jacobus van Merksteijn.",
        "month": "junho 2026",
        "home_label": "Início",
        "ed0_label": "Edição Europa",
        "wo_label": "O que emerge",
        "delen_label": "Partilhar",
        "lang_menu": "⌂ Idioma",
        "ed0_path": "edicao-0/",
        "wo_path": "o-que-emerge/",
        "h1": "Bem-vindo",
        "intro": "Esta versão portuguesa de Het Open Vizier contém a <strong>campanha sobre Bruxelas</strong>: a Edição Europa e os dois artigos centrais que descrevem, como diagnóstico, a doença anti-imune que empobrece o cidadão europeu.",
        "ed0_kop": "Edição Europa",
        "ed0_lead": "A edição sobre Bruxelas — análise completa dos mecanismos da UE que esvaziam o tecido produtivo.",
        "ed0_cta": "Ler a Edição Europa →",
        "brussel_kop": "Os dois artigos centrais",
        "brussel_intro": "Um diagnóstico, não um ataque.",
        "art1_titel": "A doença anti-imune de Bruxelas empobrece-nos",
        "art1_lead": "CBAM, ETS e Pillar Two — três ataques em simultâneo. A rota BiCRS/Etanol é ignorada.",
        "art1_path": "o-que-emerge/a-doenca-anti-imune-de-bruxelas.html",
        "art2_titel": "Matam as suas artérias vitais",
        "art2_lead": "O diagnóstico em toda a sua amplitude: seis setores, uma liderança, uma doença anti-imune.",
        "art2_path": "o-que-emerge/matam-as-suas-arterias-vitais-bruxelas.html",
        "andere_kop": "O jornal completo",
        "andere_intro": "Het Open Vizier na sua totalidade — sete edições, dossiês e investigação — está disponível em quatro idiomas:",
        "footer": "Jornal mensal independente · Jacobus van Merksteijn · Malta · junho 2026",
    },
}

def build_index(t):
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["meta"]}">
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<style>
  body {{ background:#faf8f3; color:#1a1a1a; margin:0; font-family: Georgia, serif; }}
  .masthead {{ text-align:center; padding: 2.5rem 1.5rem 1.5rem; }}
  .top-band {{ background:#f5f3ee; border-bottom:1px solid #d4d1ca; }}
  .top-band a.masthead__logo {{ display:inline-block; font-family:Georgia,serif; font-style:italic; font-weight:700; font-size:clamp(2rem,5vw,3.4rem); color:#1a1a1a !important; text-decoration:none !important; }}
  .masthead__date {{ font-size:0.85rem; letter-spacing:0.08em; text-transform:uppercase; color:#1c5760; margin-top:0.5rem; }}
  .nav {{ background:#fff; border-bottom:1px solid #d4d1ca; }}
  .nav__inner {{ max-width:1200px; margin:0 auto; padding:0.6rem 1.25rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }}
  .nav__links {{ list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:0; }}
  .nav__links li {{ margin:0; }}
  .nav__links a {{ display:inline-block; padding:0.55rem 0.9rem; color:#1c5760; text-decoration:none; font-size:0.92rem; font-family:Georgia,serif; }}
  .nav__links a:hover {{ background:#f0e9da; }}
  .nav__links a.active {{ font-weight:700; border-bottom:2px solid #1c5760; }}
  .nav__lang a {{ color:#1c5760; text-decoration:none; font-size:0.9rem; }}
  main {{ max-width:1100px; margin:0 auto; padding:0 1.5rem; }}
  .intro {{ padding:3.5rem 0 2rem; text-align:center; max-width:780px; margin:0 auto; }}
  .intro h1 {{ font-family:Georgia,serif; font-size:clamp(2.2rem,5vw,3.4rem); margin:0 0 1.2rem; }}
  .intro p {{ font-family:Georgia,serif; font-size:1.15rem; line-height:1.6; color:#4a5263; margin:0; }}
  .editie-cta {{ display:block; margin:3rem auto; max-width:880px; padding:2.5rem 2rem; background:#1c5760; color:#f5f0e6; text-decoration:none; border-left:6px solid #a8c5c1; }}
  .editie-cta:hover {{ background:#155054; }}
  .editie-cta__label {{ font-size:0.85rem; letter-spacing:0.12em; text-transform:uppercase; color:#a8c5c1; margin:0 0 0.4rem; }}
  .editie-cta__titel {{ font-family:Georgia,serif; font-size:clamp(1.8rem,4vw,2.6rem); margin:0 0 0.7rem; line-height:1.15; font-weight:700; color:#f5f0e6; }}
  .editie-cta__lead {{ font-family:Georgia,serif; font-size:1.05rem; line-height:1.55; color:#e8e3d1; margin:0 0 1rem; }}
  .editie-cta__pijl {{ display:inline-block; font-family:Georgia,serif; font-size:1rem; color:#f5f0e6; font-weight:700; border-bottom:1px solid #a8c5c1; padding-bottom:2px; }}
  .twee-kop {{ text-align:center; max-width:740px; margin:3.5rem auto 1rem; }}
  .twee-kop h2 {{ font-family:Georgia,serif; font-size:clamp(1.6rem,3.5vw,2.2rem); margin:0 0 0.6rem; }}
  .twee-kop p {{ font-family:Georgia,serif; font-style:italic; color:#4a5263; margin:0; }}
  .twee-lijst {{ display:grid; grid-template-columns:1fr; gap:1.25rem; max-width:980px; margin:0 auto 4rem; }}
  @media (min-width:780px) {{ .twee-lijst {{ grid-template-columns:1fr 1fr; }} }}
  .twee-lijst a {{ display:block; padding:1.6rem 1.7rem; background:#faf8f3; border:1px solid #d4d1ca; border-left:4px solid #1c5760; text-decoration:none; color:inherit; transition:box-shadow 0.2s; }}
  .twee-lijst a:hover {{ box-shadow:0 4px 12px rgba(0,0,0,0.08); }}
  .twee-lijst h3 {{ font-family:Georgia,serif; font-size:1.35rem; margin:0 0 0.55rem; color:#1a1a1a; line-height:1.2; }}
  .twee-lijst .lead {{ font-family:Georgia,serif; color:#4a5263; line-height:1.55; margin:0; font-size:0.97rem; }}
  .andere {{ margin:4rem auto 3rem; max-width:900px; padding:2rem; background:#f5f3ee; border:1px solid #d4d1ca; text-align:center; }}
  .andere h2 {{ font-family:Georgia,serif; font-size:1.4rem; margin:0 0 0.6rem; }}
  .andere p {{ font-family:Georgia,serif; color:#4a5263; margin:0 0 1rem; line-height:1.5; }}
  .andere .talen {{ display:flex; flex-wrap:wrap; justify-content:center; gap:0.6rem 1rem; font-family:Georgia,serif; }}
  .andere .talen a {{ color:#1c5760; text-decoration:none; border-bottom:1px solid #1c5760; padding-bottom:1px; font-weight:700; }}
  footer.eindvoet {{ padding:2.5rem 1.5rem 3rem; text-align:center; color:#6b7280; font-family:Georgia,serif; font-size:0.9rem; border-top:1px solid #d4d1ca; margin-top:3rem; }}
</style>
</head>
<body>

<div class="top-band">
  <header class="masthead">
    <a href="index.html" class="masthead__logo">Het Open Vizier</a>
    <div class="masthead__date">{t["month"]}</div>
  </header>
</div>

<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
      <li><a href="./" class="active">{t["home_label"]}</a></li>
      <li><a href="{t["ed0_path"]}">{t["ed0_label"]}</a></li>
      <li><a href="{t["wo_path"]}">{t["wo_label"]}</a></li>
      <li><a href="index-talenring.html">{t["lang_menu"].replace("⌂ ","")}</a></li>
    </ul>
    <div class="nav__lang"><a href="index-talenring.html">{t["lang_menu"]}</a></div>
  </div>
</nav>

<main>

<section class="intro">
  <h1>{t["h1"]}</h1>
  <p>{t["intro"]}</p>
</section>

<a href="{t["ed0_path"]}" class="editie-cta">
  <p class="editie-cta__label">{t["ed0_kop"]}</p>
  <h2 class="editie-cta__titel">{t["ed0_kop"]}</h2>
  <p class="editie-cta__lead">{t["ed0_lead"]}</p>
  <span class="editie-cta__pijl">{t["ed0_cta"]}</span>
</a>

<div class="twee-kop">
  <h2>{t["brussel_kop"]}</h2>
  <p>{t["brussel_intro"]}</p>
</div>
<div class="twee-lijst">
  <a href="{t["art1_path"]}">
    <h3>{t["art1_titel"]}</h3>
    <p class="lead">{t["art1_lead"]}</p>
  </a>
  <a href="{t["art2_path"]}">
    <h3>{t["art2_titel"]}</h3>
    <p class="lead">{t["art2_lead"]}</p>
  </a>
</div>

<section class="andere">
  <h2>{t["andere_kop"]}</h2>
  <p>{t["andere_intro"]}</p>
  <div class="talen">
    <a href="../nl/">Nederlands</a>
    <a href="../de/">Deutsch</a>
    <a href="../en/">English</a>
    <a href="../ru/">Русский</a>
  </div>
</section>

</main>

<footer class="eindvoet">
  <p>{t["footer"]}</p>
</footer>

</body>
</html>
'''

changed = []
for lang, t in T.items():
    path = REPO / lang / "index.html"
    path.write_text(build_index(t), encoding="utf-8")
    changed.append(str(path.relative_to(REPO)))

print(f"=== Bijgewerkt ({len(changed)}) ===")
for c in changed: print(" -", c)
