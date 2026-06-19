#!/usr/bin/env python3
"""
Voeg twee vaste kaderzinnen toe — boven en onder elk Brussel-artikel.
Bestaande tekst blijft woordelijk ongemoeid; alleen het frame wordt toegevoegd.

Master-formulering (NL, door auteur aangeleverd):
OPENING:
"Dit stuk is geschreven als een DIAGNOSE van een ziek bestuurlijk en
economisch systeem. Het is geen persoonlijke aanval, maar een poging
om de feitelijke toestand zo helder mogelijk te beschrijven zodat
gerichte behandeling mogelijk wordt."

AFSLUITING:
"Alles wat hierboven is beschreven, is bedoeld als DIAGNOSE, niet als
aanval. Alleen door het ziektebeeld scherp onder ogen te zien, kunnen
we voorkomen dat het verder doorwoekert en kunnen we werken aan herstel."

Vertaalprincipe: betekenis exact behouden — beschrijving, geen vendetta.
"""
import re
from pathlib import Path

# Per taal: top + bottom. {DIAG} wordt vervangen door <strong>diagnose-woord</strong>.
DIAG_WORD = {
    "nl": "diagnose",
    "de": "Diagnose",
    "en": "diagnosis",
    "es": "diagnóstico",
    "fr": "diagnostic",
    "it": "diagnosi",
    "pt": "diagnóstico",
    "ru": "диагноз",
}

KADERS = {
    "nl": {
        "top": "Dit stuk is geschreven als een {DIAG} van een ziek bestuurlijk en economisch systeem. Het is geen persoonlijke aanval, maar een poging om de feitelijke toestand zo helder mogelijk te beschrijven zodat gerichte behandeling mogelijk wordt.",
        "bottom": "Alles wat hierboven is beschreven, is bedoeld als {DIAG}, niet als aanval. Alleen door het ziektebeeld scherp onder ogen te zien, kunnen we voorkomen dat het verder doorwoekert en kunnen we werken aan herstel.",
    },
    "de": {
        "top": "Dieser Text ist als {DIAG} eines kranken Verwaltungs- und Wirtschaftssystems geschrieben. Er ist kein persönlicher Angriff, sondern ein Versuch, den tatsächlichen Zustand so klar wie möglich zu beschreiben, damit eine gezielte Behandlung möglich wird.",
        "bottom": "Alles, was oben beschrieben wurde, ist als {DIAG} gemeint, nicht als Angriff. Nur wenn wir das Krankheitsbild klar ins Auge fassen, können wir verhindern, dass es weiter wuchert, und an der Genesung arbeiten.",
    },
    "en": {
        "top": "This piece is written as a {DIAG} of a sick administrative and economic system. It is not a personal attack, but an attempt to describe the actual condition as clearly as possible so that targeted treatment becomes possible.",
        "bottom": "Everything described above is meant as a {DIAG}, not as an attack. Only by looking the disease squarely in the eye can we prevent it from spreading further and begin working towards recovery.",
    },
    "es": {
        "top": "Este texto está escrito como un {DIAG} de un sistema administrativo y económico enfermo. No es un ataque personal, sino un intento de describir el estado real con la mayor claridad posible para que sea posible un tratamiento dirigido.",
        "bottom": "Todo lo descrito arriba está pensado como un {DIAG}, no como un ataque. Solo mirando el cuadro clínico de frente podemos impedir que siga avanzando y empezar a trabajar en la recuperación.",
    },
    "fr": {
        "top": "Ce texte est écrit comme un {DIAG} d'un système administratif et économique malade. Ce n'est pas une attaque personnelle, mais une tentative de décrire l'état réel avec la plus grande clarté possible afin qu'un traitement ciblé devienne possible.",
        "bottom": "Tout ce qui est décrit ci-dessus est conçu comme un {DIAG}, non comme une attaque. Ce n'est qu'en regardant le tableau clinique en face que nous pouvons empêcher sa progression et travailler à la guérison.",
    },
    "it": {
        "top": "Questo testo è scritto come una {DIAG} di un sistema amministrativo ed economico malato. Non è un attacco personale, ma un tentativo di descrivere la condizione reale nel modo più chiaro possibile affinché diventi possibile un trattamento mirato.",
        "bottom": "Tutto quanto descritto sopra è inteso come una {DIAG}, non come un attacco. Solo guardando in faccia il quadro clinico possiamo impedire che si diffonda ulteriormente e iniziare a lavorare per il recupero.",
    },
    "pt": {
        "top": "Este texto foi escrito como um {DIAG} de um sistema administrativo e económico doente. Não é um ataque pessoal, mas uma tentativa de descrever o estado real com a maior clareza possível para que se torne possível um tratamento dirigido.",
        "bottom": "Tudo o que foi descrito acima é pensado como um {DIAG}, não como um ataque. Só olhando o quadro clínico de frente podemos impedir que continue a alastrar e começar a trabalhar na recuperação.",
    },
    "ru": {
        "top": "Этот текст написан как {DIAG} больной административной и экономической системы. Это не личное нападение, а попытка как можно яснее описать фактическое положение дел, чтобы стало возможным целенаправленное лечение.",
        "bottom": "Всё, что описано выше, задумано как {DIAG}, а не как нападение. Только глядя клинической картине прямо в лицо, мы можем не дать ей расползтись дальше и начать работать на выздоровление.",
    },
}

LANG_DIRS = {
    "nl/wat-opkomt": "nl",
    "de/was-aufkommt": "de",
    "en/what-surfaces": "en",
    "es/lo-que-emerge": "es",
    "fr/ce-qui-emerge": "fr",
    "it/cio-che-emerge": "it",
    "pt/o-que-emerge": "pt",
    "ru/chto-vsplyvaet": "ru",
}

FILES = {
    "nl": ["de-anti-immuunziekte-van-brussel.html", "zij-doden-hun-levensaders-brussel.html"],
    "de": ["die-anti-immunkrankheit-bruessels.html", "sie-toeten-ihre-lebensadern-bruessel.html"],
    "en": ["the-anti-immune-disease-of-brussels.html", "they-kill-their-lifelines-brussels.html"],
    "es": ["la-enfermedad-anti-inmune-de-bruselas.html", "matan-sus-arterias-vitales-bruselas.html"],
    "fr": ["la-maladie-anti-immunitaire-de-bruxelles.html", "ils-tuent-leurs-arteres-vitales-bruxelles.html"],
    "it": ["la-malattia-anti-immune-di-bruxelles.html", "uccidono-le-loro-arterie-vitali-bruxelles.html"],
    "pt": ["a-doenca-anti-imune-de-bruxelas.html", "matam-as-suas-arterias-vitais-bruxelas.html"],
    "ru": ["anti-immunnaya-bolezn-bryusselya.html", "oni-ubivayut-svoi-zhiznennye-arterii-bryussel.html"],
}

MARKER = "<!-- diagnose-kader v3 -->"
OLD_MARKERS = ["<!-- diagnose-kader v1 -->", "<!-- diagnose-kader v2 -->"]

def fmt(s, diag):
    return s.replace("{DIAG}", f"<strong>{diag}</strong>")

def top_block(k, diag):
    body = fmt(k["top"], diag)
    return f'''{MARKER}
<aside class="diagnose-kader diagnose-kader--top" style="max-width:920px;margin:1.5rem auto 2rem auto;padding:1.4rem 1.75rem;background:#f4ece0;border:1px solid #c9b896;border-left:5px solid #1c5760;font-family:Georgia,serif;color:#1a1a1a;line-height:1.6;">
  <p style="margin:0;font-size:1rem;">{body}</p>
</aside>
'''

def bottom_block(k, diag):
    body = fmt(k["bottom"], diag)
    return f'''{MARKER}
<aside class="diagnose-kader diagnose-kader--bottom" style="max-width:920px;margin:2.5rem auto 1.5rem auto;padding:1.4rem 1.75rem;background:#f4ece0;border:1px solid #c9b896;border-left:5px solid #1c5760;font-family:Georgia,serif;color:#1a1a1a;line-height:1.6;">
  <p style="margin:0;font-size:1rem;">{body}</p>
</aside>
'''

REPO = Path("/tmp/gh-repo")
changed, skipped = [], []

# Bottom anchor: alle bekende comment-varianten + Cyrillisch
BOTTOM_COMMENT_RE = re.compile(
    r'<!--\s*(?:Verwijzingenblok|Further reading block|Weiterführend[^>]*|Bloc références|Bloque de referencias|Blocco di letture|Bloco de referências|Блок ссылок)[^>]*-->',
    re.IGNORECASE,
)

# Bottom fallback: eerste "verder lezen"-aside (#faf6ec achtergrond)
BOTTOM_ASIDE_RE = re.compile(
    r'</div>\s*\n\s*(<aside[^>]*max-width:920px[^>]*background:#faf6ec)'
)

for subdir, lang in LANG_DIRS.items():
    k = KADERS[lang]
    diag = DIAG_WORD[lang]
    top = top_block(k, diag)
    bot = bottom_block(k, diag)
    for fname in FILES[lang]:
        path = REPO / subdir / fname
        if not path.exists():
            skipped.append(f"MISSING: {path}")
            continue
        html = path.read_text(encoding="utf-8")

        # Verwijder ALLE oudere kader-versies (v1, v2) ongeacht inhoud
        for om in OLD_MARKERS:
            html = re.sub(
                re.escape(om) + r'\s*<aside class="diagnose-kader[^"]*"[^>]*>.*?</aside>\s*',
                '', html, flags=re.DOTALL,
            )
        # Ook al ingevoegde v3 weghalen voor schone herinjectie (idempotent)
        html = re.sub(
            re.escape(MARKER) + r'\s*<aside class="diagnose-kader[^"]*"[^>]*>.*?</aside>\s*',
            '', html, flags=re.DOTALL,
        )

        new_html = html

        # TOP-anchor: direct na <p class="wo-artikel__auteur">...</p>
        m_auteur = re.search(r'(<p class="wo-artikel__auteur">[^<]*</p>)', new_html)
        if not m_auteur:
            skipped.append(f"no top anchor: {path}")
            continue
        idx = m_auteur.end()
        new_html = new_html[:idx] + "\n\n" + top + new_html[idx:]

        # BOTTOM-anchor: vóór alarm-strook, anders vóór "verder lezen"-comment, anders vóór eerste faf6ec-aside
        m_alarm = re.search(r'(\s*)(<div class="alarm-strook")', new_html)
        if m_alarm:
            idx = m_alarm.start()
            new_html = new_html[:idx] + "\n\n" + bot + new_html[idx:]
        else:
            m_comment = BOTTOM_COMMENT_RE.search(new_html)
            if m_comment:
                idx = m_comment.start()
                new_html = new_html[:idx] + bot + "\n" + new_html[idx:]
            else:
                m_aside = BOTTOM_ASIDE_RE.search(new_html)
                if m_aside:
                    idx = m_aside.start(1)
                    new_html = new_html[:idx] + bot + "\n" + new_html[idx:]
                else:
                    skipped.append(f"no bottom anchor: {path}")
                    continue

        path.write_text(new_html, encoding="utf-8")
        changed.append(str(path.relative_to(REPO)))

print(f"=== CHANGED ({len(changed)}) ===")
for c in changed:
    print(" -", c)
print(f"\n=== SKIPPED ({len(skipped)}) ===")
for s in skipped:
    print(" -", s)
