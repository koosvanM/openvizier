# -*- coding: utf-8 -*-
# Herbruikbare NL -> PT (Portugal) vertalingen voor boilerplate strings
# die in vrijwel alle wat-opkomt/*.html bestanden voorkomen.

BOILERPLATE = [
    # lang attribute
    ('<html lang="nl">', '<html lang="pt">'),

    # masthead / taal-switcher
    ('title="Taal: Nederlands"', 'title="Idioma: Neerlandês"'),
    ('title="Taal: · Nederlands"', 'title="Idioma: · Neerlandês"'),
    ('<span class="masthead__taal__label">Taal</span>', '<span class="masthead__taal__label">Idioma</span>'),
    ('<span class="masthead__taal__cur">· Nederlands</span>', '<span class="masthead__taal__cur">· Neerlandês</span>'),
    ('<p class="masthead__tagline">Wat opkomt — onafhankelijke journalistiek vanuit Malta</p>',
     '<p class="masthead__tagline">O que emerge — jornalismo independente a partir de Malta</p>'),
    ('<h1 class="masthead__titel">Het Open Vizier</h1>', '<h1 class="masthead__titel">Het Open Vizier</h1>'),

    # gratis-band
    ('Gratis informatieblad zonder reclame', 'Boletim gratuito sem publicidade'),
    ('<strong class="gratis-band__mid">Onafhankelijk, geen mening, geen verkoop van gegevens</strong>',
     '<strong class="gratis-band__mid">Independente, sem opinião, sem venda de dados</strong>'),
    ('Houd mij op de hoogte →', 'Mantenha-me informado →'),
    ('Houd mij op de hoogte', 'Mantenha-me informado'),

    # top nav
    ('aria-label="Hoofdmenu"', 'aria-label="Menu principal"'),
    ('<a class="ov-nav__item" href="../">Voorpagina</a>', '<a class="ov-nav__item" href="../">Capa</a>'),
    ('href="../filosofie/">Filosofie <span aria-hidden="true" class="ov-nav__caret">▾</span></a>',
     'href="../filosofie/">Filosofia <span aria-hidden="true" class="ov-nav__caret">▾</span></a>'),
    ('<a class="ov-nav__subitem" href="../filosofie/">Filosofie</a>', '<a class="ov-nav__subitem" href="../filosofie/">Filosofia</a>'),
    ('<a class="ov-nav__subitem" href="../sprookjes/">Sprookje</a>', '<a class="ov-nav__subitem" href="../sprookjes/">Conto</a>'),
    ('<a class="ov-nav__subitem" href="../leesboek/">Leesboek</a>', '<a class="ov-nav__subitem" href="../leesboek/">Livro</a>'),
    ('<a class="ov-nav__subitem" href="../7-dim-film/">7-Dim Film</a>', '<a class="ov-nav__subitem" href="../7-dim-film/">7-Dim Film</a>'),
    ('<a class="ov-nav__subitem" href="../kosaris-film/">Kosaris Film</a>', '<a class="ov-nav__subitem" href="../kosaris-film/">Filme Kosaris</a>'),
    ('<a class="ov-nav__item" href="../wat-opkomt/">Klimaat</a>', '<a class="ov-nav__item" href="../wat-opkomt/">Clima</a>'),
    ('<a class="ov-nav__item" href="../verkennen.html">Overzicht</a>', '<a class="ov-nav__item" href="../verkennen.html">Vista geral</a>'),
    ('<a class="ov-nav__item" href="../editie-6/">Nova Democratia</a>', '<a class="ov-nav__item" href="../editie-6/">Nova Democratia</a>'),
    ('<a class="ov-nav__item" href="../editie-2/">Belasting</a>', '<a class="ov-nav__item" href="../editie-2/">Impostos</a>'),
    ('<a class="ov-nav__item" href="../onderzoeken/">Onderzoek</a>', '<a class="ov-nav__item" href="../onderzoeken/">Pesquisa</a>'),
    ('<a class="ov-nav__item" href="../colofon.html">Colofon</a>', '<a class="ov-nav__item" href="../colofon.html">Créditos</a>'),

    # share dropdown (deel-menu)
    ('data-msg-copied="Link gekopieerd"', 'data-msg-copied="Link copiado"'),
    ('data-msg-copy-prompt="Kopieer deze link:"', 'data-msg-copy-prompt="Copie este link:"'),
    ('data-mail-subject="Artikel van Het Open Vizier: "', 'data-mail-subject="Artigo de Het Open Vizier: "'),
    ('data-mail-footer="Gedeeld via openvizier.org"', 'data-mail-footer="Partilhado via openvizier.org"'),
    ('data-pdf-building="PDF wordt gemaakt…"', 'data-pdf-building="A criar PDF…"'),
    ('data-pdf-done="PDF gedownload"', 'data-pdf-done="PDF baixado"'),
    ('data-pdf-fail="PDF maken mislukte — probeer Cmd+P"', 'data-pdf-fail="Falha no PDF — tente Cmd+P"'),
    ('data-pdf-source="Bron"', 'data-pdf-source="Fonte"'),
    ('data-pdf-note="Gedeeld via openvizier.org — de meertalige opiniekrant."',
     'data-pdf-note="Partilhado via openvizier.org — o jornal de opinião multilingue."'),
    ('data-gate-title="Toegangscode"', 'data-gate-title="Código de acesso"'),
    ('data-gate-body="Voer uw toegangscode in om artikelen als PDF te downloaden."',
     'data-gate-body="Insira o seu código de acesso para descarregar artigos em PDF."'),
    ('data-gate-submit="Ontgrendelen"', 'data-gate-submit="Desbloquear"'),
    ('data-gate-cancel="Annuleren"', 'data-gate-cancel="Cancelar"'),
    ('data-gate-checking="Bezig…"', 'data-gate-checking="A verificar…"'),
    ('data-gate-invalid="Voer een geldige code in."', 'data-gate-invalid="Insira um código válido."'),
    ('data-gate-wrong="Onjuiste of verlopen code."', 'data-gate-wrong="Código incorreto ou expirado."'),
    ('data-gate-server-error="Kon codes niet raadplegen. Probeer het later opnieuw."',
     'data-gate-server-error="Não foi possível verificar o código. Tente mais tarde."'),
    ('data-gate-note="Nog geen code? Neem contact op met Het Open Vizier."',
     'data-gate-note="Sem código? Contacte Het Open Vizier."'),
    ('href="#delen">Delen <span aria-hidden="true" class="ov-nav__caret">▾</span></a>',
     'href="#partilhar">Partilhar <span aria-hidden="true" class="ov-nav__caret">▾</span></a>'),
    ('<span class="ov-deel-label">🔒 PDF downloaden</span>', '<span class="ov-deel-label">🔒 Baixar PDF</span>'),
    ('<span class="ov-deel-label">Op Facebook delen</span>', '<span class="ov-deel-label">Partilhar no Facebook</span>'),
    ('<span class="ov-deel-label">Link kopiëren</span>', '<span class="ov-deel-label">Copiar link</span>'),
    ('<span class="ov-deel-label">Per e-mail versturen</span>', '<span class="ov-deel-label">Enviar por e-mail</span>'),

    # verkennen-crumb common bits
    ('<a href="../verkennen.html" style="color:#1c5760;text-decoration:none;border-bottom:1px solid rgba(28,87,96,0.3);">Verkennen</a>',
     '<a href="../verkennen.html" style="color:#1c5760;text-decoration:none;border-bottom:1px solid rgba(28,87,96,0.3);">Explorar</a>'),

    # terug/back links
    ('← Terug naar Wat opkomt', '← Voltar a O que emerge'),
    ('aria-label="Voorpagina"', 'aria-label="Capa"'),
    ('class="navbar__home">⌂ Voorpagina</a>', 'class="navbar__home">⌂ Capa</a>'),
    ('class="navbar__verk">↻ Verkennen</a>', 'class="navbar__verk">↻ Explorar</a>'),

    # footer
    ('Het Open Vizier · Onafhankelijke journalistiek vanuit Malta', 'Het Open Vizier · Jornalismo independente a partir de Malta'),
    ('Auteur: Jacobus van Merksteijn', 'Autor: Jacobus van Merksteijn'),
    ('<a href="../colofon.html">Colofon</a>', '<a href="../colofon.html">Créditos</a>'),
]
