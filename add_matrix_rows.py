#!/usr/bin/env python3
"""Add 24 new rows to nl/_data/vizier.xlsx (Knopen sheet) for the 6 translated articles x 4 languages."""
import openpyxl

WB_PATH = "nl/_data/vizier.xlsx"

wb = openpyxl.load_workbook(WB_PATH)
ws = wb["Knopen"]

headers = [c.value for c in ws[2]]
idx = {h: i for i, h in enumerate(headers) if h}
ncols = len(headers)

def make_row(code, ouder, taal, naam, ondertitel, beschrijving, url, hero, volgorde, tags, datum, hero_positie="center", hero_filter="standaard"):
    row = [None] * ncols
    row[idx['Code']] = code
    row[idx['Ouder']] = ouder
    row[idx['Taal']] = taal
    row[idx['Type']] = 'artikel'
    row[idx['Naam']] = naam
    row[idx['Ondertitel']] = ondertitel
    row[idx['Beschrijving']] = beschrijving
    row[idx['URL']] = url
    row[idx['Hero']] = hero
    row[idx['Hero-positie']] = hero_positie
    row[idx['Hero-filter']] = hero_filter
    row[idx['Tekst-positie']] = 'auto'
    row[idx['Tekst-kleur']] = 'licht'
    row[idx['Klik-actie']] = 'auto'
    row[idx['Doel-open']] = 'self'
    row[idx['Status']] = 'live'
    row[idx['Volgorde']] = volgorde
    row[idx['Actief']] = True
    row[idx['Tags']] = tags
    row[idx['Datum publicatie']] = datum
    row[idx['Auteur']] = 'Jacobus van Merksteijn'
    row[idx['Talen beschikbaar']] = taal
    return row

# Parent codes per language
PARENTS = {'fr': '5.1.1', 'es': '6.1.1', 'it': '7.1.1', 'pt': '8.1.1'}

# Article definitions: (article_index, next_code_suffix, hero, datum, tags)
articles = [
    {
        'suffix': '.3',
        'hero': '../assets/wat-opkomt/eerlijkheid/hero_zandloper.png',
        'datum': '2026-07-20',
        'tags': 'honesty, governance, gdp, transparency',
        'urls': {
            'es': 'lo-que-emerge/honestidad-hace-posible-gobernar.html',
            'fr': 'ce-qui-emerge/honnetete-rend-la-gouvernance-possible.html',
            'it': 'cio-che-emerge/onesta-rende-possibile-governare.html',
            'pt': 'o-que-emerge/honestidade-torna-governar-possivel.html',
        },
        'naam': {
            'es': 'La honestidad hace posible gobernar',
            'fr': "L'honnêteté rend la gouvernance possible",
            'it': "L'onestà rende possibile governare",
            'pt': 'A honestidade torna governar possível',
        },
        'ondertitel': {
            'es': 'La fórmula PBW: 419 mil millones de euros del PIB neerlandés no son productivos',
            'fr': 'La formule PBW : 419 milliards d\'euros du PIB néerlandais ne sont pas productifs',
            'it': 'La formula PBW: 419 miliardi di euro del PIL olandese non sono produttivi',
            'pt': 'A fórmula PBW: 419 mil milhões de euros do PIB holandês não são produtivos',
        },
        'beschrijving': {
            'es': 'La fórmula del Bienestar Productivo Bruto muestra que 419.000 millones de euros del PIB oficial neerlandés no son productivos — dissimulados por ficciones contables como el alquiler imputado y el paradoja de las prestaciones. Sin un panel honesto, toda política pública es solo tratamiento de síntomas.',
            'fr': 'La formule du Bien-être Productif Brut montre que 419 milliards d\'euros du PIB officiel néerlandais ne sont pas productifs — dissimulés par des fictions comptables comme le loyer imputé et le paradoxe des prestations. Sans un panneau honnête, toute politique n\'est que traitement des symptômes.',
            'it': 'La formula del Benessere Produttivo Grezzo mostra che 419 miliardi di euro del PIL ufficiale olandese non sono produttivi — dissimulati da finzioni contabili come l\'affitto imputato e il paradosso delle prestazioni. Senza un pannello onesto, ogni politica è solo cura dei sintomi.',
            'pt': 'A fórmula do Bem-Estar Produtivo Bruto mostra que 419 mil milhões de euros do PIB oficial holandês não são produtivos — dissimulados por ficções contabilísticas como a renda imputada e o paradoxo das prestações. Sem um painel honesto, toda política pública é apenas tratamento de sintomas.',
        },
    },
    {
        'suffix': '.4',
        'hero': '../assets/wat-opkomt/beslissen/hero_uitzicht.png',
        'datum': '2026-07-20',
        'tags': 'decision-making, legislation, sunset-clause, gdp',
        'urls': {
            'es': 'lo-que-emerge/decidir-sin-vista.html',
            'fr': 'ce-qui-emerge/decider-sans-visibilite.html',
            'it': 'cio-che-emerge/decidere-senza-visuale.html',
            'pt': 'o-que-emerge/decidir-sem-visao.html',
        },
        'naam': {
            'es': 'Decidir sin vista',
            'fr': 'Décider sans visibilité',
            'it': 'Decidere senza visuale',
            'pt': 'Decidir sem visão',
        },
        'ondertitel': {
            'es': 'Leyes sin fecha de caducidad fosilizan el sistema',
            'fr': 'Des lois sans date de validité fossilisent le système',
            'it': 'Leggi senza data di scadenza fossilizzano il sistema',
            'pt': 'Leis sem data de validade fossilizam o sistema',
        },
        'beschrijving': {
            'es': 'Leyes de los años sesenta y noventa rigidizan el sistema sin fecha de caducidad. La cláusula de extinción propuesta hace que las leyes caduquen automáticamente, forzando una revisión periódica basada en el conocimiento actual en lugar de perpetuar el pasado.',
            'fr': 'Les lois des années soixante et quatre-vingt-dix rigidifient le système sans date de validité. La clause d\'extinction proposée fait expirer automatiquement les lois, forçant une révision périodique basée sur les connaissances actuelles plutôt que de perpétuer le passé.',
            'it': 'Leggi degli anni sessanta e novanta irrigidiscono il sistema senza data di scadenza. La clausola di estinzione proposta fa scadere automaticamente le leggi, imponendo una revisione periodica basata sulla conoscenza attuale invece di perpetuare il passato.',
            'pt': 'Leis dos anos sessenta e noventa tornam o sistema rígido sem data de validade. A cláusula de extinção proposta faz as leis caducarem automaticamente, forçando uma revisão periódica baseada no conhecimento atual em vez de perpetuar o passado.',
        },
    },
    {
        'suffix': '.5',
        'hero': '../assets/wat-opkomt/eind/hero_pinokkio.png',
        'datum': '2026-07-20',
        'tags': 'nepk, biotech, learning-function, base-zero',
        'urls': {
            'es': 'lo-que-emerge/al-final-no-nos-queda-nada.html',
            'fr': 'ce-qui-emerge/a-la-fin-il-ne-nous-reste-rien.html',
            'it': 'cio-che-emerge/alla-fine-non-ci-resta-nulla.html',
            'pt': 'o-que-emerge/no-fim-nao-nos-resta-nada.html',
        },
        'naam': {
            'es': 'Al final no nos queda nada',
            'fr': 'À la fin il ne nous reste rien',
            'it': 'Alla fine non ci resta nulla',
            'pt': 'No fim não nos resta nada',
        },
        'ondertitel': {
            'es': 'Colapso del NEPK, fuga biotech y la función de aprendizaje que nunca tuvimos',
            'fr': 'Effondrement du NEPK, fuite biotech et la fonction d\'apprentissage que nous n\'avons jamais eue',
            'it': 'Crollo del NEPK, fuga biotech e la funzione di apprendimento che non abbiamo mai avuto',
            'pt': 'Colapso do NEPK, fuga biotech e a função de aprendizagem que nunca tivemos',
        },
        'beschrijving': {
            'es': '5 de las 6 grandes empresas biotecnológicas neerlandesas están en venta. El NEPK está en 2,95%, ya por debajo del umbral crítico del 3%. La solución es una función de aprendizaje: base cero con convergencia 1/5 al año, ejecutada por equipos de alta competencia.',
            'fr': '5 des 6 grandes entreprises biotech néerlandaises sont à vendre. Le NEPK est à 2,95 %, déjà sous le seuil critique de 3 %. La solution est une fonction d\'apprentissage : base zéro avec convergence 1/5 par an, exécutée par des équipes de haute compétence.',
            'it': '5 delle 6 grandi aziende biotech olandesi sono in vendita. Il NEPK è al 2,95%, già sotto la soglia critica del 3%. La soluzione è una funzione di apprendimento: base zero con convergenza 1/5 all\'anno, eseguita da team ad alta competenza.',
            'pt': '5 das 6 grandes empresas biotech holandesas estão à venda. O NEPK está em 2,95%, já abaixo do limiar crítico de 3%. A solução é uma função de aprendizagem: base zero com convergência 1/5 por ano, executada por equipas de alta competência.',
        },
    },
    {
        'suffix': '.6',
        'hero': '../assets/wat-opkomt/historisch/central_talkshow_jacobin.jpg',
        'datum': '2026-07-19',
        'tags': 'media, polarization, history, talkshow',
        'urls': {
            'es': 'lo-que-emerge/la-prensa-es-la-arena.html',
            'fr': 'ce-qui-emerge/la-presse-est-l-arene.html',
            'it': 'cio-che-emerge/la-stampa-e-l-arena.html',
            'pt': 'o-que-emerge/a-imprensa-e-a-arena.html',
        },
        'naam': {
            'es': 'La prensa es la arena',
            'fr': 'La presse est l\'arène',
            'it': 'La stampa è l\'arena',
            'pt': 'A imprensa é a arena',
        },
        'ondertitel': {
            'es': 'Cómo se fabrica la división antes de que llegue el golpe',
            'fr': 'Comment la division est fabriquée avant que le choc n\'arrive',
            'it': 'Come si fabbrica la divisione prima che arrivi il colpo',
            'pt': 'Como se fabrica a divisão antes de chegar o golpe',
        },
        'beschrijving': {
            'es': 'El talk show es el club jacobino moderno. Seis precedentes históricos (Francia 1789, Rusia 1917, Weimar 1932, Camboya 1975, Irán 1979, Venezuela 2013) muestran que la prensa produjo división en lugar de diagnóstico antes de cada colapso sistémico.',
            'fr': 'Le talk-show est le club jacobin moderne. Six précédents historiques (France 1789, Russie 1917, Weimar 1932, Cambodge 1975, Iran 1979, Venezuela 2013) montrent que la presse a produit de la division plutôt qu\'un diagnostic avant chaque effondrement systémique.',
            'it': 'Il talk show è il moderno club giacobino. Sei precedenti storici (Francia 1789, Russia 1917, Weimar 1932, Cambogia 1975, Iran 1979, Venezuela 2013) mostrano che la stampa ha prodotto divisione invece di diagnosi prima di ogni collasso sistemico.',
            'pt': 'O talk show é o clube jacobino moderno. Seis precedentes históricos (França 1789, Rússia 1917, Weimar 1932, Camboja 1975, Irão 1979, Venezuela 2013) mostram que a imprensa produziu divisão em vez de diagnóstico antes de cada colapso sistémico.',
        },
    },
    {
        'suffix': '.7',
        'hero': '../assets/wat-opkomt/H_vijf_landen_vijf_curves.jpg',
        'datum': '2026-07-19',
        'tags': 'europe, debt, phase-3, prediction',
        'urls': {
            'es': 'lo-que-emerge/cinco-paises-cinco-curvas.html',
            'fr': 'ce-qui-emerge/cinq-pays-cinq-courbes.html',
            'it': 'cio-che-emerge/cinque-paesi-cinque-curve.html',
            'pt': 'o-que-emerge/cinco-paises-cinco-curvas.html',
        },
        'naam': {
            'es': 'Cinco países, cinco curvas',
            'fr': 'Cinq pays, cinq courbes',
            'it': 'Cinque paesi, cinque curve',
            'pt': 'Cinco países, cinco curvas',
        },
        'ondertitel': {
            'es': 'Predicción 2028-2055 para Francia, Reino Unido, Italia, Alemania y España',
            'fr': 'Prévision 2028-2055 pour la France, le Royaume-Uni, l\'Italie, l\'Allemagne et l\'Espagne',
            'it': 'Previsione 2028-2055 per Francia, Regno Unito, Italia, Germania e Spagna',
            'pt': 'Previsão 2028-2055 para França, Reino Unido, Itália, Alemanha e Espanha',
        },
        'beschrijving': {
            'es': 'Cinco grandes países europeos muestran a la vez señales tempranas de crisis sistémica de fase 3. Francia primero, luego el Reino Unido, Italia y Alemania casi simultáneamente, España al final. Cada cifra anclada a una fuente publicada.',
            'fr': 'Cinq grands pays européens montrent en même temps des signaux précoces de crise systémique de phase 3. La France en premier, puis le Royaume-Uni, l\'Italie et l\'Allemagne presque simultanément, l\'Espagne en dernier. Chaque chiffre ancré à une source publiée.',
            'it': 'Cinque grandi paesi europei mostrano contemporaneamente segnali precoci di crisi sistemica di fase 3. La Francia prima, poi il Regno Unito, Italia e Germania quasi simultaneamente, la Spagna per ultima. Ogni cifra ancorata a una fonte pubblicata.',
            'pt': 'Cinco grandes países europeus mostram ao mesmo tempo sinais precoces de crise sistémica de fase 3. França primeiro, depois o Reino Unido, Itália e Alemanha quase simultaneamente, Espanha por último. Cada número ancorado a uma fonte publicada.',
        },
    },
    {
        'suffix': '.8',
        'hero': '../assets/wat-opkomt/H_nl_revolutie_voorspelling.jpg',
        'datum': '2026-07-18',
        'tags': 'netherlands, debt, revolution, prediction',
        'urls': {
            'es': 'lo-que-emerge/la-revolucion-neerlandesa-2028-2055.html',
            'fr': 'ce-qui-emerge/la-revolution-neerlandaise-2028-2055.html',
            'it': 'cio-che-emerge/la-rivoluzione-olandese-2028-2055.html',
            'pt': 'o-que-emerge/a-revolucao-holandesa-2028-2055.html',
        },
        'naam': {
            'es': 'La Revolución Neerlandesa',
            'fr': 'La Révolution néerlandaise',
            'it': 'La Rivoluzione Olandese',
            'pt': 'A Revolução Holandesa',
        },
        'ondertitel': {
            'es': 'Predicción 2028-2055 — la deuda neerlandesa es realmente 65% del PIB, no 44%',
            'fr': 'Prévision 2028-2055 — la dette néerlandaise est réellement de 65 % du PIB, pas 44 %',
            'it': 'Previsione 2028-2055 — il debito olandese è realmente al 65% del PIL, non al 44%',
            'pt': 'Previsão 2028-2055 — a dívida holandesa é realmente 65% do PIB, não 44%',
        },
        'beschrijving': {
            'es': 'La explosión de fase 3 llega entre 2032 y 2035, más probablemente 2033-2034. Cuatro países históricos señalan la misma curva. La deuda neerlandesa es realmente del 65% del PIB, no del 44%. Alemania está en la misma línea.',
            'fr': 'L\'explosion de phase 3 arrive entre 2032 et 2035, le plus probablement 2033-2034. Quatre pays historiques indiquent la même courbe. La dette néerlandaise est réellement de 65 % du PIB, pas 44 %. L\'Allemagne est sur la même ligne.',
            'it': 'L\'esplosione di fase 3 arriva tra il 2032 e il 2035, più probabilmente 2033-2034. Quattro paesi storici indicano la stessa curva. Il debito olandese è realmente al 65% del PIL, non al 44%. La Germania è sulla stessa linea.',
            'pt': 'A explosão de fase 3 chega entre 2032 e 2035, mais provavelmente 2033-2034. Quatro países históricos apontam para a mesma curva. A dívida holandesa é realmente 65% do PIB, não 44%. A Alemanha está na mesma linha.',
        },
    },
]

new_rows = []
volgorde = 58
for art in articles:
    for lang in ['fr', 'es', 'it', 'pt']:
        parent = PARENTS[lang]
        code = parent + art['suffix']
        row = make_row(
            code=code,
            ouder=parent,
            taal=lang,
            naam=art['naam'][lang],
            ondertitel=art['ondertitel'][lang],
            beschrijving=art['beschrijving'][lang],
            url=art['urls'][lang],
            hero=art['hero'],
            volgorde=str(volgorde),
            tags=art['tags'],
            datum=art['datum'],
        )
        new_rows.append(row)
        volgorde += 1

print(f"Prepared {len(new_rows)} new rows")

# Append to worksheet
for row in new_rows:
    ws.append(row)

wb.save(WB_PATH)
print("Saved.")

# Print summary of codes added
for row in new_rows:
    print(row[idx['Code']], '|', row[idx['Taal']], '|', row[idx['Naam']], '|', row[idx['URL']])
