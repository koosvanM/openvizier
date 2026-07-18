"""
Volledige lokalisatie van de body-tekst voor DE/RU/FR/ES/IT/PT.
Herbouwt de HTML-bestanden met echte vertalingen (i.p.v. EN-fallback).
"""
from pathlib import Path

REPO = Path('/home/user/workspace/openvizier')

# Configuratie per taal (masthead/nav/meta)
TALEN = {
    'de': {
        'lang_attr': 'de', 'wo_map': 'was-aufkommt', 'slug': 'welt-guertel-2040-2050',
        'titel': 'Der Welt-Gürtel — Klimaplan 2040-2050',
        'ondertitel': '425 Korridor-Segmente wissenschaftlich durchgerechnet. 290 rentabel bei €40 pro Tonne CO₂. Klimaneutral bis 2040, mindestens 50% negativ bis 2050 — mit 840.000 neuen Arbeitsplätzen in Europa und Zukunftsperspektive in Afrika.',
        'masthead_date': 'Was aufkommt',
        'masthead_tagline': 'Eine Zeitung über das Denken ohne Scheuklappen',
        'meta_line': 'Malta, 18. Juli 2026 · Untersuchung · Klimaindustrie',
        'back_link': '← Zurück zu Was aufkommt',
        'author_line': 'Jacobus van Merksteijn',
        'nav_lang': 'DE',
        'nav_links': [('../', 'Startseite'), ('./', 'Neu'), ('../verkennen.html', 'Erkunden')],
    },
    'ru': {
        'lang_attr': 'ru', 'wo_map': 'chto-vsplyvaet', 'slug': 'mirovoy-poyas-2040-2050',
        'titel': 'Мировой Пояс — климатический план 2040-2050',
        'ondertitel': '425 сегментов коридоров научно рассчитаны. 290 рентабельны при €40 за тонну CO₂. Углеродная нейтральность к 2040, минимум −50% к 2050 — с 840 000 новых рабочих мест в Европе и будущим для мигрантов в Африке.',
        'masthead_date': 'Что всплывает',
        'masthead_tagline': 'Газета о мышлении без шор',
        'meta_line': 'Мальта, 18 июля 2026 · Исследование · Климатическая индустрия',
        'back_link': '← Назад к «Что всплывает»',
        'author_line': 'Якобус ван Мерксстейн',
        'nav_lang': 'RU',
        'nav_links': [('../', 'Главная'), ('./', 'Новое'), ('../verkennen.html', 'Обзор')],
    },
    'fr': {
        'lang_attr': 'fr', 'wo_map': 'ce-qui-emerge', 'slug': 'ceinture-mondiale-2040-2050',
        'titel': 'La Ceinture-Mondiale — plan climatique 2040-2050',
        'ondertitel': '425 segments de corridor calculés scientifiquement. 290 rentables à €40 par tonne de CO₂. Neutralité climatique en 2040, au moins 50% négatif en 2050 — avec 840 000 nouveaux emplois en Europe et un avenir en Afrique.',
        'masthead_date': 'Ce qui émerge',
        'masthead_tagline': 'Un journal sur la pensée sans œillères',
        'meta_line': 'Malte, 18 juillet 2026 · Recherche · Industrie climatique',
        'back_link': '← Retour à Ce qui émerge',
        'author_line': 'Jacobus van Merksteijn',
        'nav_lang': 'FR',
        'nav_links': [('../', 'Une'), ('./', 'Nouveau'), ('../verkennen.html', 'Explorer')],
    },
    'es': {
        'lang_attr': 'es', 'wo_map': 'lo-que-emerge', 'slug': 'cinturon-mundial-2040-2050',
        'titel': 'El Cinturón-Mundial — plan climático 2040-2050',
        'ondertitel': '425 segmentos de corredor calculados científicamente. 290 rentables a €40 por tonelada de CO₂. Neutralidad climática en 2040, al menos 50% negativo en 2050 — con 840.000 nuevos empleos en Europa y un futuro en África.',
        'masthead_date': 'Lo que emerge',
        'masthead_tagline': 'Un periódico sobre pensar sin anteojeras',
        'meta_line': 'Malta, 18 de julio de 2026 · Investigación · Industria climática',
        'back_link': '← Volver a Lo que emerge',
        'author_line': 'Jacobus van Merksteijn',
        'nav_lang': 'ES',
        'nav_links': [('../', 'Portada'), ('./', 'Nuevo'), ('../verkennen.html', 'Explorar')],
    },
    'it': {
        'lang_attr': 'it', 'wo_map': 'cio-che-emerge', 'slug': 'cintura-mondiale-2040-2050',
        'titel': 'La Cintura-Mondiale — piano climatico 2040-2050',
        'ondertitel': "425 segmenti di corridoio calcolati scientificamente. 290 redditizi a €40 per tonnellata di CO₂. Neutralità climatica nel 2040, almeno 50% negativo nel 2050 — con 840.000 nuovi posti di lavoro in Europa e un futuro in Africa.",
        'masthead_date': 'Ciò che emerge',
        'masthead_tagline': 'Un giornale sul pensare senza paraocchi',
        'meta_line': 'Malta, 18 luglio 2026 · Ricerca · Industria climatica',
        'back_link': '← Torna a Ciò che emerge',
        'author_line': 'Jacobus van Merksteijn',
        'nav_lang': 'IT',
        'nav_links': [('../', 'Prima pagina'), ('./', 'Nuovo'), ('../verkennen.html', 'Esplorare')],
    },
    'pt': {
        'lang_attr': 'pt', 'wo_map': 'o-que-emerge', 'slug': 'cinturao-mundial-2040-2050',
        'titel': 'O Cinturão-Mundial — plano climático 2040-2050',
        'ondertitel': '425 segmentos de corredor calculados cientificamente. 290 rentáveis a €40 por tonelada de CO₂. Neutralidade climática em 2040, pelo menos 50% negativo em 2050 — com 840.000 novos empregos na Europa e um futuro em África.',
        'masthead_date': 'O que emerge',
        'masthead_tagline': 'Um jornal sobre pensar sem antolhos',
        'meta_line': 'Malta, 18 de julho de 2026 · Pesquisa · Indústria climática',
        'back_link': '← Voltar a O que emerge',
        'author_line': 'Jacobus van Merksteijn',
        'nav_lang': 'PT',
        'nav_links': [('../', 'Primeira página'), ('./', 'Novo'), ('../verkennen.html', 'Explorar')],
    },
}

# ============ VOLLEDIGE BODY-VERTALINGEN ============
INHOUD = {
    'de': {
        'lead': "Das Klimaproblem braucht keine ideologische Lösung mehr. Es braucht einen differenzierten Bauplan, aufgebaut aus Hektaren, Tonnen CO₂ und Euro pro Tonne. Diese Zeitung hat diese Rechnung für 425 Korridor-Segmente von 100 km rund um die Sahara, entlang der Anden, über Nord-Australien, durch Anatolien und entlang der russischen und kasachischen Steppen durchgeführt. Was dabei herauskommt, ist eine Strategie, die drei Tabus gleichzeitig bricht: sie erklärt, welche Gebiete unrentabel sind und daher übersprungen werden müssen, sie verlangt kein Opfer sondern bietet 840.000 neue Arbeitsplätze in Europa, und sie gibt Asylsuchenden eine konkrete Zukunftsperspektive in Afrika, die unsere eigene Demokratie ihnen nicht bieten kann.",
        'kpi': [('290', 'rentable Zonen bei €40/tCO₂ — von 425 durchgerechneten'),
                ('21,1 Gt', 'CO₂-Bindung pro Jahr bei Basisbreite 100 km'),
                ('80,8 Gt', 'CO₂ bei maximaler Erweiterung — 84% mehr als selbst das 2050-Ziel'),
                ('840.000', 'neue EU-Arbeitsplätze in Maschinenbau, Elektronik und Zulieferern')],
        'h2_1': 'Die Frage ist nicht "können wir es", sondern "wo und wie breit"',
        'p_q1': 'Fünfzehn Jahre Klimadebatte haben die Diskussion immer bei derselben Frage gehalten — wie viel müssen wir reduzieren, wie schnell, und wer trägt die Kosten. Die umgekehrte Frage kommt selten zur Sprache: wie viel CO₂ kann die Erde mit vorhandenen industriellen Mitteln wieder aufnehmen, und was kostet das pro Tonne? Diese Zeitung hat diese Berechnung an 425 konkreten Stellen durchgeführt, jede 100 Kilometer lang, in Abschnitten von 100 Kilometern Breite. Jedes Segment wurde nach Temperatur, Niederschlag, Tau, Feldgröße und Maschineneinsatz durchgerechnet.',
        'p_q2': '<strong>Das Ergebnis ist erschreckend einfach.</strong> Von den 425 Zonen erweisen sich nur 290 als wirklich rentabel bei einem Marktpreis von €40 pro Tonne CO₂. Der Rest — 135 Zonen — hat einen Kostenpreis über €40. Diese bekommen auf der Karte ein rotes Kreuz. Sie liegen alle in zu trockenen oder zu zersplitterten Gebieten: das ägyptische Landesinnere, die Levante, Teile der Arabischen Halbinsel, und die am stärksten zersplitterten Teile Südeuropas.',
        'quote_1': 'Die Verbreiterung rentabler Zonen liefert mehr Klimawirkung pro investiertem Euro als die Erweiterung in unrentable Zonen. Das scheint offensichtlich. Doch keine Klimaorganisation hat es jemals so formuliert.',
        'fig1_cap': 'Die 12 Korridore unterscheiden sich enorm in physischem Raum. Nord-Australien hat 600 km verfügbar, Südeuropa nur 30. Überall die gleiche Breite anzuwenden ist naiv.',
        'h2_2': 'Die Antwort ist differenziert — hier 30 km, dort 600 km',
        'p_diff': 'Klimapläne wollen gerne mit einer einzigen Zahl sprechen. Diese Studie kann das nicht. Die physische Maximalbreite pro Korridor variiert um den Faktor zwanzig: von 30 km in Südeuropa (zersplittert durch Dörfer, Olivenhaine, Weinberge und Meer) bis 600 km im australischen Top End (leer bis zum Horizont, mit Aborigine-Zusammenarbeit). Jeder Korridor erhält genau so viel Breite, wie seine Geografie zulässt.',
        'tabel1_cap_col': ['Korridor', 'Max. Breite', 'Max. CO₂ Gt/Jr', 'Kostenpreis', 'Begrenzender Faktor'],
        'tabel1_data': [
            ('<strong>Nord-Australien</strong>', '600 km', '13,4', '€10,53', 'Top End leer, Aboriginal Land Use Agreements'),
            ('<strong>Sahara Küste-zu-Küste</strong>', '500 km', '24,9', '€14,49', 'Sahara-Südrand von Mauretanien bis Djibouti'),
            ('<strong>Süd-Amerika Anden-Amazonas</strong>', '400 km', '29,1', '€7,50', 'Vorgebirge; nicht im Regenwald'),
            ('Süd-Russland Steppen', '400 km', '5,1', '€17,68', 'Sowjetische Erbschaft großer Blöcke'),
            ('Zentralasiatische Steppen', '500 km', '2,8', '€26,44', 'Kasachische Steppen, wenig Besiedlung'),
            ('Anatolien-Kaukasus-Iran', '200 km', '2,3', '€20,74', 'Hochland-Zersplitterung, Besiedlung in den Tälern'),
            ('Arabische Halbinsel', '400 km', '0,8', '€23,24', 'Wasser ist limitierender Faktor'),
            ('Nord-Sahara (Marokko-Ägypten)', '300 km', '0,8', '€32,62', 'Politische Fragmentierung Libyen, Ägypten'),
            ('Balkan-Steppenrand', '80 km', '0,6', '€22,06', 'Marginale Plateaus zwischen Landwirtschaft'),
            ('Iberisches Randland', '60 km', '0,5', '€29,83', 'Zersplittert durch Dörfer'),
            ('Levante', '50 km', '0,09', '€28,59', 'Politische Instabilität, dichte Besiedlung'),
            ('Süd-Europa Mediterran', '30 km', '0,4', '€30,61', 'Stark zersplittert durch Dörfer, Meer'),
        ],
        'tabel1_totaal': ['GESAMT', 'variiert', '80,8', 'gew. €14,91', 'Physisches globales Maximum'],
        'p_kost': 'Der durchschnittliche Kostenpreis über alle 290 rentablen Zonen bei Basisbreite 100 km beträgt <strong>€14,91 pro Tonne CO₂</strong>. Süd-Amerika kommt mit €7,50 am besten weg; Südeuropa am schlechtesten mit €30,61. Das ist keine politische Entscheidung sondern Physik: Photosyntheseeffizienz ist Temperatur × Licht × Wasser. In den Tropen sind alle drei ganzjährig vorhanden, in Europa nur 5 bis 7 Monate.',
        'h2_3': 'Die Ziele 2040 und 2050 — mit Marktpreisen, die niemand wegreden muss',
        'p_targets': 'Wenn die weltweiten CO₂-Emissionen nach realistischer Reduktionspolitik von 37,4 Gt im Jahr 2024 auf 29,3 Gt im Jahr 2040 und 17,5 Gt im Jahr 2050 sinken, dann muss unsere Bindung im Jahr 2040 mindestens diese 29,3 Gt kompensieren, um klimaneutral zu sein. Für 2050 mindestens 25% negativ müssen 26,9 Gt pro Jahr zurückgeholt werden; für 50% negativ 36,2 Gt pro Jahr.',
        'fig2_cap': 'Die rote Linie zeigt Business-as-usual mit +1%/Jahr Wachstum. Die goldene Linie zeigt eine allmähliche Reduktion durch Klimapolitik. Die dunkelgrüne Linie unsere Bindung durch den Welt-Gürtel — stetig aufbauend von null im Jahr 2026 auf 36 Gt/Jahr im Jahr 2050.',
        'p_marktprijs': 'Der Marktpreis für CO₂-Entfernung liegt heute zwischen €40 und €80 pro Tonne. Dieser Marktpreis wird im Plan beibehalten — kein Preisdruck, kein Dumping. Bei einem Marktpreis von €40 beträgt die Nettomarge über die 290 Zonen €25,09 pro Tonne; bei €80 wird das €65,09 pro Tonne. Was als Gewinn übrig bleibt, ist beträchtlich aber nicht ekstatisch: <strong>€529 Milliarden pro Jahr bei €40, €1.373 Milliarden bei €80</strong>. Ausreichend um alle Maschinen zu bauen, die gesamte Infrastruktur anzulegen und Afrika eine strukturelle Wirtschaft zu geben — und den Gastländern ihren rechtmäßigen Anteil an der weltweiten Klimaoperation zu geben.',
        'fig3_cap': 'Nettogewinn pro Korridor pro Jahr. Süd-Amerika und Sahara liefern zusammen fast zwei Drittel des globalen Gewinns — bei sowohl €40 als auch €80 Marktpreis.',
        'tabel2_col': ['Marktpreis', 'Marge/Tonne', 'Gewinn bei Basis 100 km', 'Gewinn bei physischem Max.'],
        'tabel2_data': [
            ('<strong>€40/tCO₂</strong>', '€25,09', '€529 Mrd./Jahr', '€2.027 Mrd./Jahr'),
            ('<strong>€60/tCO₂</strong>', '€45,09', '€951 Mrd./Jahr', '€3.643 Mrd./Jahr'),
        ],
        'tabel2_totaal': ['€80/tCO₂', '€65,09', '€1.373 Mrd./Jahr', '€5.259 Mrd./Jahr'],
        'h2_4': 'Wie breit muss jedes Gebiet werden?',
        'p_uitrol': 'Die optimale Umsetzung folgt dem Ertrag pro Schritt. Jede 100 Kilometer Verbreiterung wird nach Gewinn pro Hektar geordnet — und die profitabelste kommt zuerst. Die Antwort ist nicht "175 km überall". Sie ist: Süd-Amerika zuerst bis zur vollen 400 Kilometer, dann Nord-Australien bis 400 km, dann Sahara Küste-zu-Küste bis 500 km. Südeuropa erhält nur seine physischen 30 km — oder null, wenn nicht nötig.',
        'fig4_cap': 'Bei einer durchschnittlichen Breite von 139 km über alle 290 rentablen Zonen ist 2040 klimaneutral erreichbar. Bei 172 km durchschnittlich ist 2050 −50% negativ in Sicht.',
        'p_2040': '<strong>2040-Umsetzung:</strong> Süd-Amerika Anden-Amazonas auf voller 400 km (29,1 Gt/Jahr, €527 Mrd. Gewinn @€80); Nord-Australien auf 100 km (2,2 Gt/Jahr, €155 Mrd. Gewinn); Sahara Küste-zu-Küste in Pilotphase 15 km für Infrastruktur und Great-Green-Wall-Koordination. Alle anderen Korridore: noch nicht aktiv.',
        'p_2050': '<strong>2050-Umsetzung (−50% negativ):</strong> Süd-Amerika auf voller 400 km; Nord-Australien erweitert auf 400 km (8,9 Gt/Jahr); Sahara weiterhin als Reserve. Alle europäischen Korridore: alle noch 0 km. Unnötig für diese Ziele.',
        'h2_5': '840.000 neue Arbeitsplätze in Europa — das ist keine Sparerzählung',
        'p_jobs1': 'Das Auffällige an diesem Klimaplan ist, dass er keine Sparerzählung ist und keinem europäischen Bürger ein Opfer abverlangt. Es ist eine industrielle Expansion in einem Maßstab, den Europa seit dem Wiederaufbau nach dem Krieg nicht mehr gesehen hat. Die Maschinen — 6 Meter breit, 1000 Meter pro Stunde, 300 Liter Kraftstoff pro Stunde, mit KI-Zustandsüberwachung und Satellitenverifikation — werden in Deutschland, den Niederlanden, Italien und Frankreich gebaut. Die Elektronik und KI-Module kommen von Schweizer und schwedischen Zulieferern. Die Bauteile kommen von zehntausenden europäischen KMU.',
        'p_jobs2': 'Etwa 98.000 Maschinen weltweit benötigt bei physischem Maximum, mit fünfjährigem Ersatzzyklus — das bedeutet 20.000 Maschinen pro Jahr in kontinuierlicher Produktion. Jede Maschine kostet etwa €875.000 an CAPEX plus €25.000 an KI-Modulen. Etwa 40% davon fließen in Arbeitsstunden: Design, Montage, Elektronik, Test, Service. Bei einem europäischen Durchschnittslohnkostenniveau von €70.000 pro FTE pro Jahr liefert das <strong>840.000 neue Arbeitsplätze</strong>.',
        'fig5_cap': 'Die Verteilung der 840.000 neuen europäischen Arbeitsplätze auf Maschinenbau, Elektronik, Zulieferer, Wartung, F&E, Logistik und Einsatzteams in Afrika.',
        'fte_labels': [('280.000', 'Maschinenbau — Deutschland, Niederlande, Italien — Chassis, Motoren, Hydraulik'),
                      ('180.000', 'Bauteile und KMU-Zulieferer verteilt über die EU'),
                      ('120.000', 'Elektronik und KI-Module — Sensoren, Satellitenverbindung, Verifikation'),
                      ('90.000', 'Wartung und Serviceflotten, die zwischen Europa und den Korridoren reisen'),
                      ('70.000', 'Design, F&E und Biotech-Labore für Pflanzenverbesserung'),
                      ('100.000', 'Logistik, Büro und Einsatzteams in Afrika (plus hunderttausende lokale Jobs)')],
        'p_jobs3': 'Diese 840.000 Arbeitsplätze sind strukturell, nicht zyklisch. Sie bestehen solange das Klimaprogramm besteht — mindestens 30 Jahre. Sie sind regional über alle EU-Mitgliedstaaten mit industrieller Kapazität verteilt. Und sie erfordern keine Umschulung von Menschen, die heute schon in der Automobil-, Stahl- oder Fertigungsindustrie arbeiten.',
        'h2_6': 'Asylsuchende als Partner — eine Zukunftsperspektive, die unsere Demokratie nicht bieten kann',
        'p_asyl1': 'Die größte politische Wahrheit, die dieser Klimaplan aufdeckt, ist eine, die Europa lieber nicht ausspricht: unsere "Demokratie" bietet hunderttausenden Asylsuchenden keine Zukunftsperspektive. Sie kommen in Zelten und Containern an, warten jahrelang auf Verfahren, dürfen nicht arbeiten, und wenn sie einen Status erhalten, ist die erste Generation chancenlos auf dem Arbeitsmarkt und die zweite entfremdet von beiden Kulturen. Das ist kein Versagen der Absichten — das ist ein strukturelles Versagen der europäischen Gesellschaft wie sie heute funktioniert.',
        'p_asyl2': 'Der Welt-Gürtel bietet etwas wesentlich anderes. In Mauretanien, Mali, Niger, Tschad, Sudan, Äthiopien, Kolumbien, Peru und Bolivien entstehen in den kommenden 25 Jahren hunderttausende Arbeitsplätze — Maschinisten, Techniker, Satellitenanalysten, Verifikateure, Koordinatoren, Pflanzenbiologen, Wassermanager. Die Jobs sind neu, hochwertig, ökologisch sinnvoll und werden auf Weltmarkt-Niveau bezahlt, mit einem anständigen Aufschlag über den lokalen Löhnen. Sie sind genau das, was der Migrant der ersten Generation sucht und in Europa selten findet: <strong>Arbeit mit Bedeutung, in der eigenen Region, in der eigenen Sprache, mit Aussicht auf Karriere und Familie.</strong>',
        'quote_2': 'Wer in Mauretanien einen guten Job beim Klimaprogramm hat, muss nicht nach Deutschland. Wer in Mali einen technischen Beruf mit Karrierepfad lernt, braucht keinen Berliner Container. Wer in Kolumbien beim CO₂-Programm arbeitet, braucht kein Madrid.',
        'p_asyl3': 'Das ist kein Anti-Migrations-Argument. Es ist ein Pro-Zukunfts-Argument. Für Menschen, die heute als Asylsuchende in Europa festsitzen — oft gezwungen durch Umstände, die sie nicht selbst gewählt haben — bietet der Welt-Gürtel das, was unser Arbeitsmarkt und unsere Bürokratie ihnen strukturell verweigern: <strong>eine Zukunft.</strong> Rückkehr wird dann keine Abschiebung, sondern eine Anstellung. Wer heute in Ter Apel oder Nauen sitzt, kann morgen technischer Spezialist in Nouakchott oder Djibouti bei einem europäisch geleiteten Programm sein.',
        'p_asyl4': 'Was hunderttausend europäische Sozialarbeiter und Dolmetscher nicht erreichen können, erreicht das Klimaprogramm von selbst. Nicht indem man Menschen "zurückschickt", sondern indem man ihnen einen Grund gibt, zurückkehren <em>zu wollen</em>: einen Job, eine Karriere, eine Familie, ein Land, das wieder eine Zukunft hat.',
        'h2_7': 'Was übrig bleibt — 135 rote Kreuze auf der Karte',
        'p_rest1': 'Die 135 Zonen, die selbst bei €80 pro Tonne unrentabel bleiben, verdienen ebenfalls ausdrückliche Erwähnung. Sie liegen konzentriert in den trockensten, am stärksten zersplitterten Gebieten: ägyptisches Landesinneres, syrisches und irakisches Hochland, jemenitisches Bergland, Rub-al-Khali. Physisch einfach zu trocken. Politisch zu instabil. Landschaftlich zu zersplittert. Auf der Weltkarte oben in diesem Artikel sind das die roten Kreuze. Sie werden übersprungen. Punkt.',
        'p_rest2': 'Auch Levante, Süd-Europa Mediterran, Iberisches Randland und Balkan-Steppenrand sind technisch möglich, aber wirtschaftlich marginal und klimapolitisch kaum notwendig. Für 2040-neutral und 2050 −50% sind sie nicht nötig. Sie sind nur eine Option, wenn sich Rückschläge in den Hauptkorridoren häufen.',
        'h2_8': 'Was das ist, und was es nicht ist',
        'p_conc1': 'Das ist keine Utopie und kein Techno-Fix. Es ist ein differenzierter, durchgerechneter Investitionsvorschlag für eine konkrete Klimaoperation auf 290 rentablen Zonen. Er ist technisch machbar mit vorhandener Technologie — Juncao und Moringa wachsen heute schon in den Zielgebieten, die Maschinen sind eine Skalierung vorhandener Agrartechnik, Satellitenverifikation existiert seit zehn Jahren. Er ist wirtschaftlich rentabel bei einem Marktpreis, der heute schon im EU ETS erreicht wird.',
        'p_conc2': 'Er ist politisch schwierig, weil er drei Tabus gleichzeitig bricht. Er sagt, dass Teile des Klimaeinsatzes in Europa (Süd-Europa Mediterran, Iberisch, Balkan) sinnlos sind und übersprungen werden müssen. Er positioniert Klimapolitik als <strong>Wachstumsindustrie</strong> statt als Verlustindustrie. Und er skizziert eine Rückkehrperspektive für Migranten, die ausdrücklich anerkennt, dass unsere Demokratie ihnen strukturell keine Zukunft bietet.',
        'p_conc3': 'Diese Zeitung findet es Zeit für diese drei Tabus. Die Rechnung steht. Die Maschinen können gebaut werden. Die Länder wollen. Was bleibt ist der politische Mut, <strong>Differenzierung</strong> über Konsens, <strong>Industrie</strong> über Sparen, und <strong>Ehrlichkeit über Migration</strong> über Selbsttäuschung zu wählen.',
        'bron': '<strong>Quellen.</strong> Berechnungen auf Basis von 425 Korridor-Segmenten (Geografie, Temperatur, Niederschlag, Tau, Biomasseertrag pro Hektar, Maschinen-CAPEX/OPEX, Feldgröße, länderspezifische Arbeitskosten). Für den breiteren Kontext siehe das vollständige Excel-Modell Verbreding_Strategie_v3.xlsx und den zugehörigen Bericht Plan_2040_2050. Für die Physik der CO₂-Bindung über Juncao und Moringa siehe die früheren Artikel <a href="../../nl/editie-5/artikel-05-plant-die-verhuist.html">Die Pflanze, die umzieht</a> und <a href="../../nl/editie-5/artikel-03-vergeten-orde.html">Die vergessene Ordnung</a>.',
    },

    'ru': {
        'lead': 'Климатическая проблема больше не нуждается в идеологическом решении. Ей нужен дифференцированный план строительства, построенный из гектаров, тонн CO₂ и евро за тонну. Эта газета провела такой расчёт для 425 сегментов коридоров по 100 км вокруг Сахары, вдоль Анд, через Северную Австралию, через Анатолию и вдоль русских и казахских степей. Из этого выкристаллизовывается стратегия, которая одновременно нарушает три табу: она объявляет, какие территории нерентабельны и должны быть пропущены, она не требует жертв, но предлагает 840 000 новых рабочих мест в Европе, и она даёт беженцам конкретную перспективу будущего в Африке, которую наша собственная демократия им не может предложить.',
        'kpi': [('290', 'рентабельных зон при €40/тCO₂ — из 425 рассчитанных'),
                ('21,1 Гт', 'связывание CO₂ в год при базовой ширине 100 км'),
                ('80,8 Гт', 'CO₂ при максимальном расширении — на 84% больше даже цели 2050'),
                ('840 000', 'новых рабочих мест в ЕС в машиностроении и электронике')],
        'h2_1': 'Вопрос не в том, "можем ли мы", а в том, "где и насколько широко"',
        'p_q1': 'Пятнадцать лет климатических дебатов удерживали дискуссию на одном вопросе — насколько нужно сокращать выбросы, как быстро и кто платит. Обратный вопрос редко поднимается: сколько CO₂ земля может поглотить обратно существующими промышленными средствами, и сколько это стоит за тонну? Эта газета сделала такой расчёт в 425 конкретных местах, каждое длиной 100 км, в участках шириной 100 км. Каждый сегмент был рассчитан по температуре, осадкам, росе, размеру поля и использованию машин.',
        'p_q2': '<strong>Результат обескураживающе прост.</strong> Из 425 зон только 290 оказываются действительно рентабельными при рыночной цене €40 за тонну CO₂. Остальные — 135 зон — имеют себестоимость выше €40. Они получают красный крест на карте. Все они находятся в слишком сухих или слишком фрагментированных районах: внутренний Египет, Левант, части Аравийского полуострова и самые фрагментированные части Южной Европы.',
        'quote_1': 'Расширение рентабельных зон даёт больший климатический эффект на вложенный евро, чем расширение в нерентабельные зоны. Это кажется очевидным. Но ни одна климатическая организация никогда не формулировала это так.',
        'fig1_cap': '12 коридоров сильно различаются по физическому пространству. Северная Австралия имеет 600 км, Южная Европа только 30. Применять одну и ту же ширину везде наивно.',
        'h2_2': 'Ответ дифференцированный — здесь 30 км, там 600 км',
        'p_diff': 'Климатические планы любят говорить одной цифрой. Это исследование не может. Физическая максимальная ширина каждого коридора варьируется в двадцать раз: от 30 км в Южной Европе (фрагментированной деревнями, оливковыми рощами, виноградниками и морем) до 600 км в австралийском Топ-Энде (пустом до горизонта, с сотрудничеством аборигенов). Каждый коридор получает ровно столько ширины, сколько позволяет его география.',
        'tabel1_cap_col': ['Коридор', 'Макс. ширина', 'Макс. CO₂ Гт/год', 'Себестоимость', 'Ограничивающий фактор'],
        'tabel1_data': [
            ('<strong>Северная Австралия</strong>', '600 км', '13,4', '€10,53', 'Топ-Энд пуст, Соглашения о землепользовании с аборигенами'),
            ('<strong>Сахара от берега до берега</strong>', '500 км', '24,9', '€14,49', 'Южная граница Сахары от Мавритании до Джибути'),
            ('<strong>Южная Америка Анды-Амазонка</strong>', '400 км', '29,1', '€7,50', 'Предгорья; не в тропическом лесу'),
            ('Южно-русские степи', '400 км', '5,1', '€17,68', 'Советское наследие крупных блоков'),
            ('Центрально-азиатские степи', '500 км', '2,8', '€26,44', 'Казахские степи, мало населения'),
            ('Анатолия-Кавказ-Иран', '200 км', '2,3', '€20,74', 'Фрагментация нагорий, население в долинах'),
            ('Аравийский полуостров', '400 км', '0,8', '€23,24', 'Вода — ограничивающий фактор'),
            ('Северная Сахара (Марокко-Египет)', '300 км', '0,8', '€32,62', 'Политическая фрагментация Ливии, Египта'),
            ('Балканская окраина степи', '80 км', '0,6', '€22,06', 'Маргинальные плато между сельским хозяйством'),
            ('Иберийские окраинные земли', '60 км', '0,5', '€29,83', 'Фрагментировано деревнями'),
            ('Левант', '50 км', '0,09', '€28,59', 'Политическая нестабильность, плотное население'),
            ('Средиземноморье Южной Европы', '30 км', '0,4', '€30,61', 'Сильно фрагментировано деревнями, морем'),
        ],
        'tabel1_totaal': ['ВСЕГО', 'варьируется', '80,8', 'взвеш. €14,91', 'Физический глобальный максимум'],
        'p_kost': 'Средняя себестоимость по всем 290 рентабельным зонам при базовой ширине 100 км составляет <strong>€14,91 за тонну CO₂</strong>. Южная Америка выходит лучше всего — €7,50; Южная Европа хуже всего — €30,61. Это не политический выбор, а физика: эффективность фотосинтеза = температура × свет × вода. В тропиках все три доступны круглый год, в Европе только 5-7 месяцев.',
        'h2_3': 'Цели 2040 и 2050 — с рыночными ценами, которые никому не нужно замалчивать',
        'p_targets': 'Если мировые выбросы CO₂ по реалистичной политике сокращения падают с 37,4 Гт в 2024 до 29,3 Гт в 2040 и 17,5 Гт в 2050, то наше связывание в 2040 должно как минимум компенсировать эти 29,3 Гт, чтобы быть углеродно-нейтральным. Для 2050 минимум −25% нужно возвращать 26,9 Гт в год; для −50% — 36,2 Гт в год.',
        'fig2_cap': 'Красная линия показывает business-as-usual с ростом +1%/год. Золотая линия — постепенное сокращение через климатическую политику. Тёмно-зелёная линия — наше связывание через Мировой Пояс — устойчиво нарастает с нуля в 2026 до 36 Гт/год в 2050.',
        'p_marktprijs': 'Рыночная цена удаления CO₂ сегодня стоит между €40 и €80 за тонну. Эта рыночная цена сохраняется в плане — никакого давления, никакого демпинга. При рыночной цене €40 чистая маржа по 290 зонам составляет €25,09 за тонну; при €80 это становится €65,09 за тонну. Оставшаяся прибыль значительна, но не запредельна: <strong>€529 миллиардов в год при €40, €1373 миллиарда при €80</strong>. Достаточно, чтобы построить все машины, проложить всю инфраструктуру и дать Африке структурную экономику — а принимающим странам их законную долю в мировой климатической операции.',
        'fig3_cap': 'Чистая прибыль по коридору в год. Южная Америка и Сахара вместе дают почти две трети мировой прибыли — как при €40, так и при €80 рыночной цене.',
        'tabel2_col': ['Рыночная цена', 'Маржа/тонну', 'Прибыль при базе 100 км', 'Прибыль при физ. макс.'],
        'tabel2_data': [
            ('<strong>€40/тCO₂</strong>', '€25,09', '€529 млрд/год', '€2027 млрд/год'),
            ('<strong>€60/тCO₂</strong>', '€45,09', '€951 млрд/год', '€3643 млрд/год'),
        ],
        'tabel2_totaal': ['€80/тCO₂', '€65,09', '€1373 млрд/год', '€5259 млрд/год'],
        'h2_4': 'Насколько широким должен стать каждый район?',
        'p_uitrol': 'Оптимальное развёртывание следует прибыли на шаг. Каждые 100 км расширения ранжируются по прибыли за гектар — и самое прибыльное идёт первым. Ответ не "175 км везде". Он такой: Южная Америка первой до полных 400 км, затем Северная Австралия до 400 км, затем Сахара от берега до берега до 500 км. Южная Европа получает только свои физические 30 км — или ноль, если не нужно.',
        'fig4_cap': 'При средней ширине 139 км по всем 290 рентабельным зонам достигается климатическая нейтральность 2040. При 172 км среднем виден 2050 −50% негативный.',
        'p_2040': '<strong>Развёртывание 2040:</strong> Южная Америка Анды-Амазонка на полных 400 км (29,1 Гт/год, €527 млрд прибыли @€80); Северная Австралия на 100 км (2,2 Гт/год, €155 млрд прибыли); Сахара от берега до берега в пилотной фазе 15 км для инфраструктуры и координации Великой Зелёной Стены. Все остальные коридоры: пока не активны.',
        'p_2050': '<strong>Развёртывание 2050 (−50% негативно):</strong> Южная Америка на полных 400 км; Северная Австралия расширена до 400 км (8,9 Гт/год); Сахара всё ещё в резерве. Все европейские коридоры: все ещё 0 км. Не нужны для этих целей.',
        'h2_5': '840 000 новых рабочих мест в Европе — это не история экономии',
        'p_jobs1': 'Что поразительно в этом климатическом плане, это то, что он не является историей экономии и не требует жертв от европейского гражданина. Это промышленная экспансия в масштабе, которого Европа не видела со времён послевоенного восстановления. Машины — 6 метров в ширину, 1000 метров в час, 300 литров топлива в час, с ИИ-мониторингом состояния и спутниковой верификацией — строятся в Германии, Нидерландах, Италии и Франции. Электроника и ИИ-модули поступают от швейцарских и шведских поставщиков. Компоненты поступают от десятков тысяч европейских МСП.',
        'p_jobs2': 'Около 98 000 машин потребуется в мире при физическом максимуме, с пятилетним циклом замены — это означает 20 000 машин в год в непрерывном производстве. Каждая машина стоит около €875 000 CAPEX плюс €25 000 в ИИ-модулях. Около 40% этого идёт на рабочие часы: проектирование, сборка, электроника, тестирование, обслуживание. При среднеевропейских трудозатратах €70 000 на FTE в год это даёт <strong>840 000 новых рабочих мест</strong>.',
        'fig5_cap': 'Распределение 840 000 новых европейских рабочих мест по машиностроению, электронике, поставщикам, обслуживанию, R&D, логистике и командам развёртывания в Африке.',
        'fte_labels': [('280 000', 'Машиностроение — Германия, Нидерланды, Италия — шасси, двигатели, гидравлика'),
                      ('180 000', 'Компоненты и МСП-поставщики по всему ЕС'),
                      ('120 000', 'Электроника и ИИ-модули — сенсоры, спутниковая связь, верификация'),
                      ('90 000', 'Обслуживание и сервисные флоты между Европой и коридорами'),
                      ('70 000', 'Проектирование, R&D и биотех-лаборатории'),
                      ('100 000', 'Логистика, офис и команды развёртывания в Африке (плюс сотни тысяч местных рабочих мест)')],
        'p_jobs3': 'Эти 840 000 рабочих мест структурны, не цикличны. Они существуют пока существует климатическая программа — минимум 30 лет. Они регионально распределены по всем странам-членам ЕС с промышленным потенциалом. И они не требуют переподготовки людей, которые сегодня уже работают в автомобильной, металлургической или производственной промышленности.',
        'h2_6': 'Беженцы как партнёры — перспектива будущего, которую наша демократия не может предложить',
        'p_asyl1': 'Самая большая политическая правда, которую раскрывает этот климатический план, — та, которую Европа предпочитает не произносить вслух: наша "демократия" не предлагает сотням тысяч беженцев никакой перспективы будущего. Они приезжают в палатки и контейнеры, годами ждут процедур, им не разрешают работать, а когда они получают статус, первое поколение бессильно на рынке труда, а второе отчуждено от обеих культур. Это не провал намерений — это структурный провал европейского общества, каким оно функционирует сегодня.',
        'p_asyl2': 'Мировой Пояс предлагает нечто существенно иное. В Мавритании, Мали, Нигере, Чаде, Судане, Эфиопии, Колумбии, Перу и Боливии в ближайшие 25 лет появятся сотни тысяч рабочих мест — машинисты, техники, спутниковые аналитики, верификаторы, координаторы, биологи растений, водохозяйственники. Работы новые, высокоценные, экологически осмысленные и оплачиваются по мировому уровню с достойной надбавкой над местными зарплатами. Они — это именно то, что ищет мигрант первого поколения и редко находит в Европе: <strong>работа со смыслом, в своей стране, на своём языке, с перспективой карьеры и семьи.</strong>',
        'quote_2': 'Тот, у кого хорошая работа в Мавритании при климатической программе, не должен ехать в Германию. Тот, кто в Мали учит технический профессию с карьерным путём, не нуждается в берлинском контейнере. Тот, кто работает в Колумбии в программе CO₂, не нуждается в Мадриде.',
        'p_asyl3': 'Это не антимиграционный аргумент. Это про-будущее аргумент. Для людей, которые сегодня застряли беженцами в Европе — часто вынужденных обстоятельствами, которые они сами не выбирали — Мировой Пояс предлагает то, в чём наш рынок труда и бюрократия им структурно отказывают: <strong>будущее.</strong> Возвращение тогда становится не депортацией, а назначением. Тот, кто сегодня сидит в Тер-Апеле или Науене, завтра может быть техническим специалистом в Нуакшоте или Джибути при европейской программе.',
        'p_asyl4': 'То, чего не могут добиться сто тысяч европейских соцработников и переводчиков, климатическая программа достигает сама по себе. Не "отправляя людей обратно", а давая им причину <em>хотеть</em> вернуться: работу, карьеру, семью, страну с будущим.',
        'h2_7': 'Что остаётся — 135 красных крестов на карте',
        'p_rest1': '135 зон, которые остаются нерентабельными даже при €80 за тонну, также заслуживают явного упоминания. Они сконцентрированы в самых сухих, самых фрагментированных районах: внутренний Египет, сирийское и иракское нагорья, йеменские горы, Руб-эль-Хали. Физически просто слишком сухо. Политически слишком нестабильно. Ландшафтно слишком фрагментировано. На карте мира вверху этой статьи это красные кресты. Их пропускают. Точка.',
        'p_rest2': 'Также Левант, Средиземноморье Южной Европы, Иберийские окраинные земли и Балканская окраина степи технически возможны, но экономически маргинальны и климатически едва ли необходимы. Для 2040-нейтральной и 2050 −50% они не нужны. Они лишь опция, если неудачи в главных коридорах накапливаются.',
        'h2_8': 'Что это такое и чем оно не является',
        'p_conc1': 'Это не утопия и не технологическое решение. Это дифференцированное, просчитанное инвестиционное предложение для конкретной климатической операции на 290 рентабельных зонах. Технически осуществимо с существующей технологией — Джункао и Моринга уже растут в целевых районах, машины — масштабирование существующей сельхозтехники, спутниковая верификация существует десять лет. Экономически рентабельно при рыночной цене, уже достигаемой в EU ETS.',
        'p_conc2': 'Политически трудно, потому что нарушает три табу одновременно. Оно говорит, что части климатических усилий в Европе (Средиземноморье, Иберия, Балканы) бессмысленны и должны быть пропущены. Оно позиционирует климатическую политику как <strong>индустрию роста</strong>, а не индустрию потерь. И оно набрасывает перспективу возвращения для мигрантов, которая явно признаёт: наша демократия структурно не даёт им будущего.',
        'p_conc3': 'Эта газета считает, что настало время для этих трёх табу. Расчёт есть. Машины могут быть построены. Страны хотят. Что осталось — политическая смелость выбрать <strong>дифференциацию</strong> над консенсусом, <strong>индустрию</strong> над экономией, и <strong>честность о миграции</strong> над самообманом.',
        'bron': '<strong>Источники.</strong> Расчёты на основе 425 сегментов коридоров (география, температура, осадки, роса, урожайность биомассы на гектар, CAPEX/OPEX машин, размер поля, страновые трудозатраты). Для более широкого контекста см. полную Excel-модель Verbreding_Strategie_v3.xlsx и сопутствующий отчёт Plan_2040_2050. О физике связывания CO₂ через Джункао и Морингу см. <a href="../../nl/editie-5/artikel-05-plant-die-verhuist.html">Растение, которое переезжает</a> и <a href="../../nl/editie-5/artikel-03-vergeten-orde.html">Забытый порядок</a>.',
    },

    'fr': {
        'lead': "Le problème climatique n'a plus besoin d'une solution idéologique. Il a besoin d'un plan de construction différencié, bâti à partir d'hectares, de tonnes de CO₂ et d'euros par tonne. Ce journal a fait ce calcul pour 425 segments de corridor de 100 km autour du Sahara, le long des Andes, à travers l'Australie du Nord, à travers l'Anatolie et le long des steppes russes et kazakhes. Ce qui en ressort est une stratégie qui brise trois tabous à la fois : elle déclare quels territoires sont non rentables et doivent donc être écartés, elle ne demande aucun sacrifice mais offre 840 000 nouveaux emplois en Europe, et elle donne aux demandeurs d'asile une perspective d'avenir concrète en Afrique que notre propre démocratie ne peut leur offrir.",
        'kpi': [('290', "zones rentables à €40/tCO₂ — sur 425 calculées"),
                ('21,1 Gt', "séquestration de CO₂ par an à largeur de base 100 km"),
                ('80,8 Gt', "CO₂ à l'expansion maximale — 84% de plus que même l'objectif 2050"),
                ('840 000', "nouveaux emplois européens dans la construction de machines et l'électronique")],
        'h2_1': "La question n'est pas \"pouvons-nous le faire\", mais \"où et à quelle largeur\"",
        'p_q1': "Quinze ans de débat climatique ont maintenu la discussion sur la même question — de combien devons-nous réduire, à quelle vitesse, et qui paie les coûts. La question inverse est rarement soulevée : combien de CO₂ la terre peut-elle réabsorber avec les moyens industriels existants, et combien cela coûte-t-il par tonne ? Ce journal a fait ce calcul à 425 endroits concrets, chacun long de 100 km, en sections de 100 km de large. Chaque segment a été calculé en fonction de la température, des précipitations, de la rosée, de la taille du champ et du déploiement des machines.",
        'p_q2': "<strong>Le résultat est d'une simplicité déconcertante.</strong> Sur les 425 zones, seules 290 s'avèrent véritablement rentables à un prix de marché de €40 par tonne de CO₂. Le reste — 135 zones — a un coût supérieur à €40. Elles reçoivent une croix rouge sur la carte. Elles se trouvent toutes dans des régions trop sèches ou trop fragmentées : l'intérieur égyptien, le Levant, des parties de la péninsule arabique, et les parties les plus fragmentées de l'Europe du Sud.",
        'quote_1': "Élargir les zones rentables offre un impact climatique plus important par euro investi que l'expansion vers des zones non rentables. Cela semble évident. Pourtant, aucune organisation climatique ne l'a jamais formulé de cette façon.",
        'fig1_cap': "Les 12 corridors diffèrent énormément par leur espace physique. L'Australie du Nord dispose de 600 km, l'Europe du Sud seulement de 30. Appliquer la même largeur partout est naïf.",
        'h2_2': "La réponse est différenciée — 30 km ici, 600 km là-bas",
        'p_diff': "Les plans climatiques aiment parler avec un seul chiffre. Cette étude ne le peut pas. La largeur maximale physique par corridor varie d'un facteur vingt : de 30 km en Europe du Sud (fragmentée par les villages, oliveraies, vignobles et mer) à 600 km dans le Top End australien (vide jusqu'à l'horizon, avec la coopération aborigène). Chaque corridor reçoit exactement autant de largeur que sa géographie le permet.",
        'tabel1_cap_col': ['Corridor', 'Largeur max', 'CO₂ max Gt/an', 'Coût', 'Facteur limitant'],
        'tabel1_data': [
            ('<strong>Australie du Nord</strong>', '600 km', '13,4', '€10,53', "Top End vide, Accords d'utilisation des terres aborigènes"),
            ('<strong>Sahara Côte-à-Côte</strong>', '500 km', '24,9', '€14,49', "Bord sud du Sahara de la Mauritanie à Djibouti"),
            ('<strong>Amérique du Sud Andes-Amazone</strong>', '400 km', '29,1', '€7,50', "Contreforts ; pas dans la forêt tropicale"),
            ('Steppes de Russie du Sud', '400 km', '5,1', '€17,68', "Héritage soviétique de grands blocs"),
            ("Steppes d'Asie centrale", '500 km', '2,8', '€26,44', "Steppes kazakhes, peu de population"),
            ('Anatolie-Caucase-Iran', '200 km', '2,3', '€20,74', "Fragmentation des hauts plateaux"),
            ('Péninsule arabique', '400 km', '0,8', '€23,24', "L'eau est le facteur limitant"),
            ('Sahara Nord (Maroc-Égypte)', '300 km', '0,8', '€32,62', "Fragmentation politique Libye, Égypte"),
            ('Bord des steppes balkaniques', '80 km', '0,6', '€22,06', "Plateaux marginaux entre agriculture"),
            ('Terres marginales ibériques', '60 km', '0,5', '€29,83', "Fragmentées par les villages"),
            ('Levant', '50 km', '0,09', '€28,59', "Instabilité politique, population dense"),
            ('Europe du Sud méditerranéenne', '30 km', '0,4', '€30,61', "Fortement fragmentée par villages, mer"),
        ],
        'tabel1_totaal': ['TOTAL', 'variable', '80,8', 'pond. €14,91', "Maximum physique mondial"],
        'p_kost': "Le coût moyen pour toutes les 290 zones rentables à largeur de base 100 km est de <strong>€14,91 par tonne de CO₂</strong>. L'Amérique du Sud sort la meilleure à €7,50 ; l'Europe du Sud la pire à €30,61. Ce n'est pas un choix politique mais de la physique : l'efficacité de la photosynthèse = température × lumière × eau. Sous les tropiques, les trois sont présents toute l'année, en Europe seulement 5 à 7 mois.",
        'h2_3': "Les objectifs 2040 et 2050 — avec des prix de marché que personne n'a besoin de minimiser",
        'p_targets': "Si les émissions mondiales de CO₂ sous une politique de réduction réaliste passent de 37,4 Gt en 2024 à 29,3 Gt en 2040 et 17,5 Gt en 2050, notre séquestration en 2040 doit au moins compenser ces 29,3 Gt pour être climatiquement neutre. Pour 2050 au moins 25% négatif, il faut éliminer 26,9 Gt par an ; pour 50% négatif 36,2 Gt par an.",
        'fig2_cap': "La ligne rouge montre le business-as-usual avec une croissance de +1%/an. La ligne dorée montre une réduction progressive via la politique climatique. La ligne vert foncé notre séquestration via la Ceinture-Mondiale — construite régulièrement de zéro en 2026 à 36 Gt/an en 2050.",
        'p_marktprijs': "Le prix de marché de l'élimination du CO₂ se situe aujourd'hui entre €40 et €80 par tonne. Ce prix de marché est maintenu dans le plan — pas de pression sur les prix, pas de dumping. À un prix de marché de €40, la marge nette sur les 290 zones est de €25,09 par tonne ; à €80 cela devient €65,09 par tonne. Ce qui reste comme bénéfice est substantiel mais pas extatique : <strong>€529 milliards par an à €40, €1373 milliards à €80</strong>. Suffisant pour construire toutes les machines, installer toute l'infrastructure et donner à l'Afrique une économie structurelle — et donner aux pays d'accueil leur juste part dans l'opération climatique mondiale.",
        'fig3_cap': "Bénéfice net par corridor par an. L'Amérique du Sud et le Sahara fournissent ensemble près des deux tiers du bénéfice mondial — à la fois au prix de marché de €40 et de €80.",
        'tabel2_col': ['Prix de marché', 'Marge/tonne', 'Bénéfice base 100 km', 'Bénéfice max physique'],
        'tabel2_data': [
            ('<strong>€40/tCO₂</strong>', '€25,09', '€529 Mrd./an', '€2027 Mrd./an'),
            ('<strong>€60/tCO₂</strong>', '€45,09', '€951 Mrd./an', '€3643 Mrd./an'),
        ],
        'tabel2_totaal': ['€80/tCO₂', '€65,09', '€1373 Mrd./an', '€5259 Mrd./an'],
        'h2_4': "Quelle doit être la largeur de chaque région ?",
        'p_uitrol': "Le déploiement optimal suit le retour par étape. Chaque 100 km d'élargissement est classé selon le bénéfice par hectare — et le plus rentable vient en premier. La réponse n'est pas \"175 km partout\". C'est : d'abord l'Amérique du Sud à 400 km pleins, puis l'Australie du Nord à 400 km, puis le Sahara Côte-à-Côte à 500 km. L'Europe du Sud ne reçoit que ses 30 km physiques — ou zéro, si ce n'est pas nécessaire.",
        'fig4_cap': "À une largeur moyenne de 139 km sur les 290 zones rentables, la neutralité climatique 2040 est atteignable. À 172 km en moyenne, 2050 −50% négatif est en vue.",
        'p_2040': "<strong>Déploiement 2040 :</strong> Amérique du Sud Andes-Amazone à 400 km pleins (29,1 Gt/an, €527 Mrd. de bénéfice @€80) ; Australie du Nord à 100 km (2,2 Gt/an, €155 Mrd. de bénéfice) ; Sahara Côte-à-Côte en phase pilote 15 km pour infrastructure et coordination de la Grande Muraille Verte. Tous les autres corridors : pas encore actifs.",
        'p_2050': "<strong>Déploiement 2050 (−50% négatif) :</strong> Amérique du Sud à 400 km pleins ; Australie du Nord étendue à 400 km (8,9 Gt/an) ; Sahara toujours en réserve. Tous les corridors européens : toujours 0 km. Inutiles pour ces objectifs.",
        'h2_5': "840 000 nouveaux emplois en Europe — ce n'est pas un récit d'austérité",
        'p_jobs1': "Ce qui est frappant dans ce plan climatique, c'est qu'il n'est pas un récit d'austérité et ne demande aucun sacrifice au citoyen européen. C'est une expansion industrielle à une échelle que l'Europe n'a pas connue depuis la reconstruction d'après-guerre. Les machines — 6 mètres de large, 1000 mètres par heure, 300 litres de carburant par heure, avec surveillance de l'état par IA et vérification satellite — sont construites en Allemagne, aux Pays-Bas, en Italie et en France. L'électronique et les modules IA proviennent de fournisseurs suisses et suédois. Les composants proviennent de dizaines de milliers de PME européennes.",
        'p_jobs2': "Environ 98 000 machines sont nécessaires dans le monde au maximum physique, avec un cycle de remplacement de cinq ans — ce qui signifie 20 000 machines par an en production continue. Chaque machine coûte environ €875 000 en CAPEX plus €25 000 en modules IA. Environ 40% de cela va aux heures de travail : conception, assemblage, électronique, test, service. À un coût moyen européen du travail de €70 000 par ETP par an, cela livre <strong>840 000 nouveaux emplois</strong>.",
        'fig5_cap': "Répartition des 840 000 nouveaux emplois européens entre construction de machines, électronique, fournisseurs, maintenance, R&D, logistique et équipes de déploiement en Afrique.",
        'fte_labels': [('280 000', "Construction de machines — Allemagne, Pays-Bas, Italie — châssis, moteurs, hydraulique"),
                      ('180 000', "Composants et fournisseurs PME répartis dans toute l'UE"),
                      ('120 000', "Électronique et modules IA — capteurs, liaison satellite, vérification"),
                      ('90 000', "Maintenance et flottes de service entre Europe et corridors"),
                      ('70 000', "Conception, R&D et laboratoires biotech pour amélioration des plantes"),
                      ('100 000', "Logistique, bureau et équipes de déploiement en Afrique")],
        'p_jobs3': "Ces 840 000 emplois sont structurels, pas cycliques. Ils existent aussi longtemps que le programme climatique existe — au moins 30 ans. Ils sont répartis régionalement dans tous les États membres de l'UE ayant une capacité industrielle. Et ils ne nécessitent aucune reconversion des personnes qui travaillent aujourd'hui déjà dans l'automobile, la sidérurgie ou la fabrication.",
        'h2_6': "Les demandeurs d'asile comme partenaires — une perspective d'avenir que notre démocratie ne peut offrir",
        'p_asyl1': "La plus grande vérité politique que ce plan climatique révèle est celle que l'Europe préfère ne pas dire à haute voix : notre \"démocratie\" n'offre à des centaines de milliers de demandeurs d'asile aucune perspective d'avenir. Ils arrivent dans des tentes et des conteneurs, attendent des années les procédures, ne sont pas autorisés à travailler, et une fois qu'ils obtiennent un statut, la première génération est impuissante sur le marché du travail et la seconde aliénée aux deux cultures. Ce n'est pas un échec des intentions — c'est un échec structurel de la société européenne telle qu'elle fonctionne aujourd'hui.",
        'p_asyl2': "La Ceinture-Mondiale offre quelque chose d'essentiellement différent. En Mauritanie, au Mali, au Niger, au Tchad, au Soudan, en Éthiopie, en Colombie, au Pérou et en Bolivie, des centaines de milliers d'emplois vont émerger dans les 25 prochaines années — machinistes, techniciens, analystes satellites, vérificateurs, coordinateurs, biologistes végétaux, gestionnaires de l'eau. Les emplois sont nouveaux, de haute valeur, écologiquement significatifs et payés au niveau du marché mondial avec une majoration décente au-dessus des salaires locaux. Ils sont exactement ce que le migrant de première génération cherche et trouve rarement en Europe : <strong>un travail avec du sens, dans sa propre région, dans sa propre langue, avec la perspective d'une carrière et d'une famille.</strong>",
        'quote_2': "Celui qui a un bon travail en Mauritanie au programme climatique n'a pas besoin d'aller en Allemagne. Celui qui apprend un métier technique au Mali avec un parcours de carrière n'a pas besoin d'un conteneur berlinois. Celui qui travaille en Colombie au programme CO₂ n'a pas besoin de Madrid.",
        'p_asyl3': "Ce n'est pas un argument anti-migration. C'est un argument pro-avenir. Pour les personnes aujourd'hui coincées comme demandeurs d'asile en Europe — souvent forcées par des circonstances qu'elles n'ont pas choisies — la Ceinture-Mondiale offre ce que notre marché du travail et notre bureaucratie leur refusent structurellement : <strong>un avenir.</strong> Le retour devient alors non pas une déportation, mais une nomination. Ceux qui sont aujourd'hui à Ter Apel ou Nauen peuvent demain être spécialistes techniques à Nouakchott ou Djibouti dans un programme dirigé par les Européens.",
        'p_asyl4': "Ce que cent mille travailleurs sociaux et interprètes européens ne peuvent pas atteindre, le programme climatique l'atteint tout seul. Pas en \"renvoyant les gens\", mais en leur donnant une raison de <em>vouloir</em> retourner : un emploi, une carrière, une famille, un pays qui a à nouveau un avenir.",
        'h2_7': "Ce qui reste — 135 croix rouges sur la carte",
        'p_rest1': "Les 135 zones qui restent non rentables même à €80 par tonne méritent également une mention explicite. Elles sont concentrées dans les régions les plus sèches, les plus fragmentées : intérieur égyptien, hauts plateaux syriens et irakiens, montagnes yéménites, Rub-al-Khali. Physiquement simplement trop sèches. Politiquement trop instables. Paysagèrement trop fragmentées. Sur la carte du monde en haut de cet article, ce sont les croix rouges. Elles sont écartées. Point.",
        'p_rest2': "Levant, Europe du Sud méditerranéenne, Terres marginales ibériques et Bord des steppes balkaniques sont techniquement possibles mais économiquement marginaux et climatiquement guère nécessaires. Pour 2040-neutre et 2050 −50% ils ne sont pas nécessaires. Ils ne sont qu'une option si les revers dans les corridors principaux s'accumulent.",
        'h2_8': "Ce que c'est, et ce que ce n'est pas",
        'p_conc1': "Ce n'est pas une utopie et pas une solution technique miracle. C'est une proposition d'investissement différenciée et calculée pour une opération climatique concrète sur 290 zones rentables. Techniquement réalisable avec la technologie existante — Juncao et Moringa poussent déjà dans les zones cibles, les machines sont un passage à l'échelle de la technologie agricole existante, la vérification satellite existe depuis dix ans. Économiquement rentable à un prix de marché déjà atteint dans l'EU ETS.",
        'p_conc2': "Politiquement difficile car il brise trois tabous à la fois. Il dit que des parties de l'effort climatique en Europe (Méditerranée, Ibérie, Balkans) sont sans intérêt et doivent être écartées. Il positionne la politique climatique comme une <strong>industrie de croissance</strong> au lieu d'une industrie de perte. Et il esquisse une perspective de retour pour les migrants qui reconnaît explicitement : notre démocratie ne leur offre structurellement pas d'avenir.",
        'p_conc3': "Ce journal estime qu'il est temps pour ces trois tabous. Le calcul est établi. Les machines peuvent être construites. Les pays le veulent. Ce qui reste est le courage politique de choisir la <strong>différenciation</strong> sur le consensus, l'<strong>industrie</strong> sur l'austérité, et l'<strong>honnêteté sur la migration</strong> sur l'auto-illusion.",
        'bron': "<strong>Sources.</strong> Calculs basés sur 425 segments de corridor (géographie, température, précipitations, rosée, rendement de biomasse par hectare, CAPEX/OPEX machines, taille de champ, coûts du travail spécifiques au pays). Pour un contexte plus large, voir le modèle Excel complet Verbreding_Strategie_v3.xlsx et le rapport correspondant Plan_2040_2050. Pour la physique de la séquestration du CO₂ via Juncao et Moringa, voir <a href=\"../../nl/editie-5/artikel-05-plant-die-verhuist.html\">La plante qui déménage</a> et <a href=\"../../nl/editie-5/artikel-03-vergeten-orde.html\">L'ordre oublié</a>.",
    },

    'es': {
        'lead': "El problema climático ya no necesita una solución ideológica. Necesita un plan de construcción diferenciado, construido a partir de hectáreas, toneladas de CO₂ y euros por tonelada. Este periódico realizó ese cálculo para 425 segmentos de corredor de 100 km alrededor del Sahara, a lo largo de los Andes, a través del norte de Australia, a través de Anatolia y a lo largo de las estepas rusas y kazajas. Lo que surge es una estrategia que rompe tres tabúes a la vez: declara qué áreas son no rentables y por tanto deben omitirse, no requiere sacrificio sino que ofrece 840.000 nuevos empleos en Europa, y da a los solicitantes de asilo una perspectiva de futuro concreta en África que nuestra propia democracia no puede ofrecerles.",
        'kpi': [('290', 'zonas rentables a €40/tCO₂ — de 425 calculadas'),
                ('21,1 Gt', 'secuestro de CO₂ por año a ancho base 100 km'),
                ('80,8 Gt', 'CO₂ en expansión máxima — 84% más que incluso el objetivo 2050'),
                ('840.000', 'nuevos empleos en la UE en construcción de máquinas y electrónica')],
        'h2_1': 'La pregunta no es "¿podemos hacerlo?", sino "¿dónde y cuán ancho?"',
        'p_q1': "Quince años de debate climático han mantenido la discusión sobre la misma pregunta — cuánto debemos reducir, qué tan rápido, y quién paga los costos. La pregunta inversa rara vez se plantea: ¿cuánto CO₂ puede la tierra reabsorber con los medios industriales existentes, y cuánto cuesta eso por tonelada? Este periódico hizo ese cálculo en 425 lugares concretos, cada uno de 100 km de largo, en secciones de 100 km de ancho. Cada segmento se calculó según temperatura, precipitación, rocío, tamaño del campo y despliegue de máquinas.",
        'p_q2': "<strong>El resultado es desconcertantemente simple.</strong> De las 425 zonas, solo 290 resultan verdaderamente rentables a un precio de mercado de €40 por tonelada de CO₂. El resto — 135 zonas — tiene un costo superior a €40. Estas reciben una cruz roja en el mapa. Todas están en áreas demasiado secas o demasiado fragmentadas: el interior egipcio, el Levante, partes de la Península Arábiga, y las partes más fragmentadas del sur de Europa.",
        'quote_1': "Ampliar las zonas rentables ofrece más impacto climático por euro invertido que expandirse hacia zonas no rentables. Eso parece obvio. Sin embargo, ninguna organización climática lo ha formulado nunca así.",
        'fig1_cap': "Los 12 corredores difieren enormemente en espacio físico. El norte de Australia tiene 600 km disponibles, el sur de Europa solo 30. Aplicar el mismo ancho en todas partes es ingenuo.",
        'h2_2': 'La respuesta es diferenciada — 30 km aquí, 600 km allí',
        'p_diff': "Los planes climáticos gustan hablar con un solo número. Este estudio no puede. El ancho máximo físico por corredor varía en un factor de veinte: de 30 km en el sur de Europa (fragmentado por pueblos, olivares, viñedos y mar) a 600 km en el Top End australiano (vacío hasta el horizonte, con cooperación aborigen). Cada corredor recibe exactamente tanto ancho como permite su geografía.",
        'tabel1_cap_col': ['Corredor', 'Ancho máx', 'Máx CO₂ Gt/año', 'Costo', 'Factor limitante'],
        'tabel1_data': [
            ('<strong>Norte de Australia</strong>', '600 km', '13,4', '€10,53', 'Top End vacío, Acuerdos de Uso de Tierras Aborígenes'),
            ('<strong>Sahara Costa-a-Costa</strong>', '500 km', '24,9', '€14,49', 'Borde sur del Sahara de Mauritania a Yibuti'),
            ('<strong>Sudamérica Andes-Amazonas</strong>', '400 km', '29,1', '€7,50', 'Piedemonte; no en selva'),
            ('Estepas del sur de Rusia', '400 km', '5,1', '€17,68', 'Legado soviético de grandes bloques'),
            ('Estepas de Asia Central', '500 km', '2,8', '€26,44', 'Estepas kazajas, poca población'),
            ('Anatolia-Cáucaso-Irán', '200 km', '2,3', '€20,74', 'Fragmentación de altiplanos'),
            ('Península Arábiga', '400 km', '0,8', '€23,24', 'El agua es factor limitante'),
            ('Sahara Norte (Marruecos-Egipto)', '300 km', '0,8', '€32,62', 'Fragmentación política Libia, Egipto'),
            ('Borde de estepa balcánica', '80 km', '0,6', '€22,06', 'Mesetas marginales entre agricultura'),
            ('Tierras marginales ibéricas', '60 km', '0,5', '€29,83', 'Fragmentado por pueblos'),
            ('Levante', '50 km', '0,09', '€28,59', 'Inestabilidad política, población densa'),
            ('Sur de Europa mediterráneo', '30 km', '0,4', '€30,61', 'Fuertemente fragmentado por pueblos, mar'),
        ],
        'tabel1_totaal': ['TOTAL', 'varía', '80,8', 'pond. €14,91', 'Máximo físico global'],
        'p_kost': "El costo promedio sobre todas las 290 zonas rentables a ancho base 100 km es de <strong>€14,91 por tonelada de CO₂</strong>. Sudamérica sale mejor con €7,50; el sur de Europa peor con €30,61. No es una elección política sino física: eficiencia de fotosíntesis = temperatura × luz × agua. En los trópicos los tres están presentes todo el año, en Europa solo 5 a 7 meses.",
        'h2_3': 'Los objetivos 2040 y 2050 — con precios de mercado que nadie necesita minimizar',
        'p_targets': "Si las emisiones mundiales de CO₂ bajo una política de reducción realista caen de 37,4 Gt en 2024 a 29,3 Gt en 2040 y 17,5 Gt en 2050, entonces nuestro secuestro en 2040 debe al menos compensar esas 29,3 Gt para ser climáticamente neutral. Para 2050 al menos 25% negativo, hay que retirar 26,9 Gt por año; para 50% negativo 36,2 Gt por año.",
        'fig2_cap': "La línea roja muestra business-as-usual con crecimiento +1%/año. La línea dorada muestra reducción gradual mediante política climática. La línea verde oscuro nuestro secuestro mediante el Cinturón-Mundial — construyendo constantemente de cero en 2026 a 36 Gt/año en 2050.",
        'p_marktprijs': "El precio de mercado para la eliminación de CO₂ está hoy entre €40 y €80 por tonelada. Este precio de mercado se mantiene en el plan — sin presión de precios, sin dumping. A un precio de mercado de €40 el margen neto sobre las 290 zonas es de €25,09 por tonelada; a €80 se convierte en €65,09 por tonelada. Lo que queda como beneficio es sustancial pero no extático: <strong>€529 mil millones por año a €40, €1.373 mil millones a €80</strong>. Suficiente para construir todas las máquinas, tender toda la infraestructura y dar a África una economía estructural — y dar a los países anfitriones su parte justa en la operación climática mundial.",
        'fig3_cap': "Beneficio neto por corredor por año. Sudamérica y Sahara juntos entregan casi dos tercios del beneficio global — tanto a precio de mercado €40 como €80.",
        'tabel2_col': ['Precio de mercado', 'Margen/tonelada', 'Beneficio base 100 km', 'Beneficio máx físico'],
        'tabel2_data': [
            ('<strong>€40/tCO₂</strong>', '€25,09', '€529 Mrd./año', '€2.027 Mrd./año'),
            ('<strong>€60/tCO₂</strong>', '€45,09', '€951 Mrd./año', '€3.643 Mrd./año'),
        ],
        'tabel2_totaal': ['€80/tCO₂', '€65,09', '€1.373 Mrd./año', '€5.259 Mrd./año'],
        'h2_4': '¿Qué ancho debe tener cada área?',
        'p_uitrol': "El despliegue óptimo sigue el rendimiento por paso. Cada 100 km de ampliación se clasifica por beneficio por hectárea — y el más rentable viene primero. La respuesta no es \"175 km en todas partes\". Es: primero Sudamérica a los 400 km completos, luego norte de Australia a 400 km, luego Sahara Costa-a-Costa a 500 km. El sur de Europa solo recibe sus 30 km físicos — o cero, si no es necesario.",
        'fig4_cap': "A un ancho promedio de 139 km sobre las 290 zonas rentables, 2040 climáticamente neutral es alcanzable. A 172 km promedio, 2050 −50% negativo está a la vista.",
        'p_2040': "<strong>Despliegue 2040:</strong> Sudamérica Andes-Amazonas a 400 km completos (29,1 Gt/año, €527 Mrd. de beneficio @€80); norte de Australia a 100 km (2,2 Gt/año, €155 Mrd. de beneficio); Sahara Costa-a-Costa en fase piloto 15 km para infraestructura y coordinación de la Gran Muralla Verde. Todos los demás corredores: aún no activos.",
        'p_2050': "<strong>Despliegue 2050 (−50% negativo):</strong> Sudamérica a 400 km completos; norte de Australia expandido a 400 km (8,9 Gt/año); Sahara aún como reserva. Todos los corredores europeos: todavía 0 km. Innecesarios para estos objetivos.",
        'h2_5': '840.000 nuevos empleos en Europa — esto no es un relato de austeridad',
        'p_jobs1': "Lo llamativo de este plan climático es que no es un relato de austeridad y no pide sacrificio al ciudadano europeo. Es una expansión industrial a una escala que Europa no ha visto desde la reconstrucción de posguerra. Las máquinas — 6 metros de ancho, 1000 metros por hora, 300 litros de combustible por hora, con monitoreo de condición por IA y verificación satelital — se construyen en Alemania, Países Bajos, Italia y Francia. La electrónica y los módulos de IA provienen de proveedores suizos y suecos. Los componentes vienen de decenas de miles de pymes europeas.",
        'p_jobs2': "Aproximadamente 98.000 máquinas necesarias en todo el mundo al máximo físico, con ciclo de reemplazo de cinco años — significa 20.000 máquinas por año en producción continua. Cada máquina cuesta aproximadamente €875.000 en CAPEX más €25.000 en módulos de IA. Aproximadamente el 40% de esto va a horas de trabajo: diseño, ensamblaje, electrónica, prueba, servicio. A un costo laboral europeo promedio de €70.000 por FTE por año, eso entrega <strong>840.000 nuevos empleos</strong>.",
        'fig5_cap': "Distribución de los 840.000 nuevos empleos europeos entre construcción de máquinas, electrónica, proveedores, mantenimiento, I+D, logística y equipos de despliegue en África.",
        'fte_labels': [('280.000', 'Construcción de máquinas — Alemania, Países Bajos, Italia — chasis, motores, hidráulica'),
                      ('180.000', 'Componentes y proveedores pymes distribuidos en la UE'),
                      ('120.000', 'Electrónica y módulos de IA — sensores, enlace satelital, verificación'),
                      ('90.000', 'Mantenimiento y flotas de servicio entre Europa y corredores'),
                      ('70.000', 'Diseño, I+D y laboratorios biotecnológicos para mejora de plantas'),
                      ('100.000', 'Logística, oficina y equipos de despliegue en África (más cientos de miles de empleos locales)')],
        'p_jobs3': "Estos 840.000 empleos son estructurales, no cíclicos. Existen mientras exista el programa climático — al menos 30 años. Están distribuidos regionalmente en todos los Estados miembros de la UE con capacidad industrial. Y no requieren recualificación de personas que hoy ya trabajan en la industria automotriz, siderúrgica o manufacturera.",
        'h2_6': 'Los solicitantes de asilo como socios — una perspectiva de futuro que nuestra democracia no puede ofrecer',
        'p_asyl1': "La mayor verdad política que este plan climático expone es una que Europa prefiere no decir en voz alta: nuestra \"democracia\" no ofrece a cientos de miles de solicitantes de asilo ninguna perspectiva de futuro. Llegan en tiendas y contenedores, esperan años los procedimientos, no se les permite trabajar, y cuando reciben estatus, la primera generación queda impotente en el mercado laboral y la segunda alienada de ambas culturas. Esto no es un fracaso de intenciones — es un fracaso estructural de la sociedad europea tal como funciona hoy.",
        'p_asyl2': "El Cinturón-Mundial ofrece algo esencialmente diferente. En Mauritania, Malí, Níger, Chad, Sudán, Etiopía, Colombia, Perú y Bolivia surgirán cientos de miles de empleos en los próximos 25 años — maquinistas, técnicos, analistas satelitales, verificadores, coordinadores, biólogos de plantas, gestores de agua. Los empleos son nuevos, de alto valor, ecológicamente significativos y pagados a nivel de mercado mundial con un decente margen sobre los salarios locales. Son exactamente lo que el migrante de primera generación busca y raramente encuentra en Europa: <strong>trabajo con significado, en su propia región, en su propia lengua, con perspectiva de una carrera y una familia.</strong>",
        'quote_2': "Quien tiene un buen trabajo en Mauritania en el programa climático no necesita ir a Alemania. Quien aprende una profesión técnica en Malí con una trayectoria profesional no necesita un contenedor berlinés. Quien trabaja en Colombia en el programa CO₂ no necesita Madrid.",
        'p_asyl3': "Este no es un argumento anti-migración. Es un argumento pro-futuro. Para las personas que hoy están atrapadas como solicitantes de asilo en Europa — a menudo forzadas por circunstancias que no eligieron — el Cinturón-Mundial ofrece lo que nuestro mercado laboral y burocracia les niegan estructuralmente: <strong>un futuro.</strong> El retorno se convierte entonces no en una deportación, sino en un nombramiento. Quienes hoy están en Ter Apel o Nauen pueden mañana ser especialistas técnicos en Nuakchot o Yibuti en un programa dirigido por europeos.",
        'p_asyl4': "Lo que cien mil trabajadores sociales e intérpretes europeos no pueden lograr, el programa climático lo logra por sí solo. No \"devolviendo personas\", sino dándoles una razón para <em>querer</em> regresar: un empleo, una carrera, una familia, un país con futuro nuevamente.",
        'h2_7': 'Lo que queda — 135 cruces rojas en el mapa',
        'p_rest1': "Las 135 zonas que permanecen no rentables incluso a €80 por tonelada también merecen mención explícita. Se concentran en las áreas más secas, más fragmentadas: interior egipcio, altiplanos sirios e iraquíes, montañas yemeníes, Rub-al-Khali. Físicamente demasiado secas. Políticamente demasiado inestables. Paisajísticamente demasiado fragmentadas. En el mapa mundial en la parte superior de este artículo, estas son las cruces rojas. Se omiten. Punto.",
        'p_rest2': "También Levante, Sur de Europa mediterráneo, Tierras marginales ibéricas y Borde de estepa balcánica son técnicamente posibles pero económicamente marginales y climático-políticamente apenas necesarios. Para 2040-neutral y 2050 −50% no son necesarios. Son solo una opción si los contratiempos en los corredores principales se acumulan.",
        'h2_8': 'Lo que esto es, y lo que no es',
        'p_conc1': "Esto no es una utopía ni una solución técnica milagrosa. Es una propuesta de inversión diferenciada y calculada para una operación climática concreta en 290 zonas rentables. Es técnicamente factible con tecnología existente — Juncao y Moringa ya crecen hoy en las áreas objetivo, las máquinas son una ampliación de escala de tecnología agrícola existente, la verificación satelital existe desde hace diez años. Es económicamente rentable a un precio de mercado ya alcanzado en el EU ETS.",
        'p_conc2': "Es políticamente difícil porque rompe tres tabúes a la vez. Dice que partes del esfuerzo climático en Europa (mediterráneo, ibérico, balcánico) son inútiles y deben omitirse. Posiciona la política climática como una <strong>industria de crecimiento</strong> en lugar de industria de pérdidas. Y esboza una perspectiva de retorno para migrantes que reconoce explícitamente: nuestra democracia no les ofrece estructuralmente futuro.",
        'p_conc3': "Este periódico piensa que es hora de esos tres tabúes. El cálculo está. Las máquinas pueden construirse. Los países quieren. Lo que queda es el coraje político de elegir <strong>diferenciación</strong> sobre consenso, <strong>industria</strong> sobre austeridad, y <strong>honestidad sobre migración</strong> sobre autoengaño.",
        'bron': "<strong>Fuentes.</strong> Cálculos basados en 425 segmentos de corredor (geografía, temperatura, precipitación, rocío, rendimiento de biomasa por hectárea, CAPEX/OPEX máquinas, tamaño de campo, costos laborales por país). Para contexto más amplio ver el modelo Excel completo Verbreding_Strategie_v3.xlsx y el informe adjunto Plan_2040_2050. Para la física del secuestro de CO₂ vía Juncao y Moringa ver <a href=\"../../nl/editie-5/artikel-05-plant-die-verhuist.html\">La planta que se muda</a> y <a href=\"../../nl/editie-5/artikel-03-vergeten-orde.html\">El orden olvidado</a>.",
    },

    'it': {
        'lead': "Il problema climatico non ha più bisogno di una soluzione ideologica. Ha bisogno di un piano di costruzione differenziato, costruito da ettari, tonnellate di CO₂ ed euro per tonnellata. Questo giornale ha fatto quel calcolo per 425 segmenti di corridoio di 100 km intorno al Sahara, lungo le Ande, attraverso l'Australia settentrionale, attraverso l'Anatolia e lungo le steppe russe e kazake. Ciò che emerge è una strategia che rompe tre tabù contemporaneamente: dichiara quali aree sono non redditizie e quindi devono essere saltate, non richiede sacrifici ma offre 840.000 nuovi posti di lavoro in Europa, e dà ai richiedenti asilo una concreta prospettiva di futuro in Africa che la nostra stessa democrazia non può offrire loro.",
        'kpi': [('290', 'zone redditizie a €40/tCO₂ — su 425 calcolate'),
                ('21,1 Gt', 'sequestro CO₂ all\'anno a larghezza base 100 km'),
                ('80,8 Gt', 'CO₂ alla massima espansione — 84% in più dell\'obiettivo 2050'),
                ('840.000', 'nuovi posti di lavoro UE in costruzione macchine ed elettronica')],
        'h2_1': 'La domanda non è "possiamo farlo", ma "dove e quanto largo"',
        'p_q1': "Quindici anni di dibattito climatico hanno mantenuto la discussione sulla stessa domanda — quanto dobbiamo ridurre, quanto velocemente, e chi paga i costi. La domanda inversa raramente viene sollevata: quanto CO₂ può la terra riassorbire con mezzi industriali esistenti, e quanto costa per tonnellata? Questo giornale ha fatto quel calcolo in 425 luoghi concreti, ciascuno lungo 100 km, in sezioni larghe 100 km. Ogni segmento è stato calcolato secondo temperatura, precipitazioni, rugiada, dimensione del campo e impiego di macchine.",
        'p_q2': "<strong>Il risultato è di sconcertante semplicità.</strong> Delle 425 zone, solo 290 risultano veramente redditizie a un prezzo di mercato di €40 per tonnellata di CO₂. Il resto — 135 zone — ha un costo superiore a €40. Queste ricevono una croce rossa sulla mappa. Sono tutte in aree troppo secche o troppo frammentate: l'interno egiziano, il Levante, parti della Penisola Arabica, e le parti più frammentate dell'Europa meridionale.",
        'quote_1': "Ampliare le zone redditizie offre più impatto climatico per euro investito rispetto all'espansione in zone non redditizie. Sembra ovvio. Eppure nessuna organizzazione climatica lo ha mai formulato così.",
        'fig1_cap': "I 12 corridoi differiscono enormemente per spazio fisico. L'Australia settentrionale ha 600 km disponibili, l'Europa meridionale solo 30. Applicare la stessa larghezza ovunque è ingenuo.",
        'h2_2': "La risposta è differenziata — 30 km qui, 600 km là",
        'p_diff': "I piani climatici amano parlare con un singolo numero. Questo studio non può. La larghezza massima fisica per corridoio varia di un fattore venti: da 30 km nell'Europa meridionale (frammentata da villaggi, oliveti, vigneti e mare) a 600 km nel Top End australiano (vuoto fino all'orizzonte, con cooperazione aborigena). Ogni corridoio riceve esattamente tanta larghezza quanto la sua geografia permette.",
        'tabel1_cap_col': ['Corridoio', 'Larghezza max', 'CO₂ max Gt/anno', 'Costo', 'Fattore limitante'],
        'tabel1_data': [
            ('<strong>Australia settentrionale</strong>', '600 km', '13,4', '€10,53', "Top End vuoto, Accordi d'uso del territorio aborigeni"),
            ('<strong>Sahara Costa-a-Costa</strong>', '500 km', '24,9', '€14,49', "Bordo sud del Sahara dalla Mauritania a Gibuti"),
            ('<strong>Sud America Ande-Amazzonia</strong>', '400 km', '29,1', '€7,50', "Pedemontano; non in foresta pluviale"),
            ('Steppe della Russia meridionale', '400 km', '5,1', '€17,68', "Eredità sovietica di grandi blocchi"),
            ('Steppe centroasiatiche', '500 km', '2,8', '€26,44', "Steppe kazake, poca popolazione"),
            ('Anatolia-Caucaso-Iran', '200 km', '2,3', '€20,74', "Frammentazione degli altipiani"),
            ('Penisola Arabica', '400 km', '0,8', '€23,24', "L'acqua è fattore limitante"),
            ('Nord Sahara (Marocco-Egitto)', '300 km', '0,8', '€32,62', "Frammentazione politica Libia, Egitto"),
            ('Bordo delle steppe balcaniche', '80 km', '0,6', '€22,06', "Altipiani marginali tra agricoltura"),
            ('Terre marginali iberiche', '60 km', '0,5', '€29,83', "Frammentate dai villaggi"),
            ('Levante', '50 km', '0,09', '€28,59', "Instabilità politica, popolazione densa"),
            ('Sud Europa mediterraneo', '30 km', '0,4', '€30,61', "Fortemente frammentato da villaggi, mare"),
        ],
        'tabel1_totaal': ['TOTALE', 'variabile', '80,8', 'pond. €14,91', "Massimo fisico globale"],
        'p_kost': "Il costo medio sulle 290 zone redditizie a larghezza base 100 km è di <strong>€14,91 per tonnellata di CO₂</strong>. Il Sud America esce meglio a €7,50; l'Europa meridionale peggio a €30,61. Non è una scelta politica ma fisica: efficienza della fotosintesi = temperatura × luce × acqua. Nei tropici tutti e tre sono presenti tutto l'anno, in Europa solo 5-7 mesi.",
        'h2_3': "Gli obiettivi 2040 e 2050 — con prezzi di mercato che nessuno deve minimizzare",
        'p_targets': "Se le emissioni globali di CO₂ sotto una politica di riduzione realistica scendono da 37,4 Gt nel 2024 a 29,3 Gt nel 2040 e 17,5 Gt nel 2050, il nostro sequestro nel 2040 deve almeno compensare quei 29,3 Gt per essere climaticamente neutrale. Per 2050 almeno 25% negativo, bisogna rimuovere 26,9 Gt all'anno; per 50% negativo 36,2 Gt all'anno.",
        'fig2_cap': "La linea rossa mostra il business-as-usual con crescita +1%/anno. La linea dorata mostra riduzione graduale tramite politica climatica. La linea verde scuro il nostro sequestro tramite la Cintura-Mondiale — costruendo costantemente da zero nel 2026 a 36 Gt/anno nel 2050.",
        'p_marktprijs': "Il prezzo di mercato per la rimozione di CO₂ si trova oggi tra €40 e €80 per tonnellata. Questo prezzo di mercato è mantenuto nel piano — senza pressione sui prezzi, senza dumping. A un prezzo di mercato di €40 il margine netto sulle 290 zone è €25,09 per tonnellata; a €80 diventa €65,09 per tonnellata. Ciò che rimane come profitto è sostanziale ma non estatico: <strong>€529 miliardi all'anno a €40, €1.373 miliardi a €80</strong>. Sufficienti a costruire tutte le macchine, posare tutta l'infrastruttura e dare all'Africa un'economia strutturale — e dare ai paesi ospitanti la loro giusta quota nell'operazione climatica mondiale.",
        'fig3_cap': "Profitto netto per corridoio all'anno. Sud America e Sahara insieme forniscono quasi due terzi del profitto globale — sia a €40 che €80 di prezzo di mercato.",
        'tabel2_col': ['Prezzo di mercato', 'Margine/tonnellata', 'Profitto base 100 km', 'Profitto max fisico'],
        'tabel2_data': [
            ('<strong>€40/tCO₂</strong>', '€25,09', '€529 Mrd./anno', '€2.027 Mrd./anno'),
            ('<strong>€60/tCO₂</strong>', '€45,09', '€951 Mrd./anno', '€3.643 Mrd./anno'),
        ],
        'tabel2_totaal': ['€80/tCO₂', '€65,09', '€1.373 Mrd./anno', '€5.259 Mrd./anno'],
        'h2_4': "Quanto larga deve diventare ogni area?",
        'p_uitrol': "Il rollout ottimale segue il rendimento per passo. Ogni 100 km di ampliamento è classificato per profitto per ettaro — e il più redditizio viene per primo. La risposta non è \"175 km ovunque\". È: prima Sud America ai pieni 400 km, poi Australia settentrionale a 400 km, poi Sahara Costa-a-Costa a 500 km. L'Europa meridionale riceve solo i suoi 30 km fisici — o zero, se non necessari.",
        'fig4_cap': "A una larghezza media di 139 km sulle 290 zone redditizie, 2040 climaticamente neutrale è raggiungibile. A 172 km medi, 2050 −50% negativo è in vista.",
        'p_2040': "<strong>Rollout 2040:</strong> Sud America Ande-Amazzonia ai pieni 400 km (29,1 Gt/anno, €527 Mrd. di profitto @€80); Australia settentrionale a 100 km (2,2 Gt/anno, €155 Mrd. di profitto); Sahara Costa-a-Costa in fase pilota 15 km per infrastruttura e coordinamento della Grande Muraglia Verde. Tutti gli altri corridoi: non ancora attivi.",
        'p_2050': "<strong>Rollout 2050 (−50% negativo):</strong> Sud America ai pieni 400 km; Australia settentrionale espansa a 400 km (8,9 Gt/anno); Sahara ancora come riserva. Tutti i corridoi europei: ancora 0 km. Non necessari per questi obiettivi.",
        'h2_5': "840.000 nuovi posti di lavoro in Europa — questa non è una storia di austerità",
        'p_jobs1': "Ciò che è notevole in questo piano climatico è che non è una storia di austerità e non chiede sacrifici al cittadino europeo. È un'espansione industriale su una scala che l'Europa non ha visto dalla ricostruzione post-bellica. Le macchine — 6 metri di larghezza, 1000 metri all'ora, 300 litri di carburante all'ora, con monitoraggio delle condizioni tramite IA e verifica satellitare — sono costruite in Germania, Paesi Bassi, Italia e Francia. L'elettronica e i moduli IA provengono da fornitori svizzeri e svedesi. I componenti provengono da decine di migliaia di PMI europee.",
        'p_jobs2': "Circa 98.000 macchine necessarie in tutto il mondo al massimo fisico, con ciclo di sostituzione di cinque anni — significa 20.000 macchine all'anno in produzione continua. Ogni macchina costa circa €875.000 di CAPEX più €25.000 in moduli IA. Circa il 40% di questo va alle ore di lavoro: progettazione, assemblaggio, elettronica, test, servizio. A un costo del lavoro europeo medio di €70.000 per FTE all'anno, ciò fornisce <strong>840.000 nuovi posti di lavoro</strong>.",
        'fig5_cap': "Distribuzione degli 840.000 nuovi posti di lavoro europei tra costruzione di macchine, elettronica, fornitori, manutenzione, R&S, logistica e squadre di dispiegamento in Africa.",
        'fte_labels': [('280.000', "Costruzione di macchine — Germania, Paesi Bassi, Italia — telai, motori, idraulica"),
                      ('180.000', "Componenti e fornitori PMI distribuiti nell'UE"),
                      ('120.000', "Elettronica e moduli IA — sensori, collegamento satellitare, verifica"),
                      ('90.000', "Manutenzione e flotte di servizio tra Europa e corridoi"),
                      ('70.000', "Progettazione, R&S e laboratori biotech per miglioramento piante"),
                      ('100.000', "Logistica, ufficio e squadre di dispiegamento in Africa")],
        'p_jobs3': "Questi 840.000 posti di lavoro sono strutturali, non ciclici. Esistono finché esiste il programma climatico — almeno 30 anni. Sono distribuiti regionalmente in tutti gli Stati membri UE con capacità industriale. E non richiedono riqualificazione di persone che oggi lavorano già nell'industria automobilistica, siderurgica o manifatturiera.",
        'h2_6': "I richiedenti asilo come partner — una prospettiva di futuro che la nostra democrazia non può offrire",
        'p_asyl1': "La più grande verità politica che questo piano climatico rivela è una che l'Europa preferisce non pronunciare ad alta voce: la nostra \"democrazia\" non offre a centinaia di migliaia di richiedenti asilo alcuna prospettiva di futuro. Arrivano in tende e container, aspettano anni le procedure, non hanno il permesso di lavorare, e una volta ricevuto lo status, la prima generazione è impotente sul mercato del lavoro e la seconda alienata da entrambe le culture. Questo non è un fallimento delle intenzioni — è un fallimento strutturale della società europea come funziona oggi.",
        'p_asyl2': "La Cintura-Mondiale offre qualcosa di essenzialmente diverso. In Mauritania, Mali, Niger, Ciad, Sudan, Etiopia, Colombia, Perù e Bolivia emergeranno centinaia di migliaia di posti di lavoro nei prossimi 25 anni — macchinisti, tecnici, analisti satellitari, verificatori, coordinatori, biologi vegetali, gestori dell'acqua. I posti di lavoro sono nuovi, di alto valore, ecologicamente significativi e pagati a livello di mercato mondiale con un decente aumento sopra i salari locali. Sono esattamente quello che il migrante di prima generazione cerca e raramente trova in Europa: <strong>lavoro con significato, nella propria regione, nella propria lingua, con prospettiva di una carriera e una famiglia.</strong>",
        'quote_2': "Chi ha un buon lavoro in Mauritania al programma climatico non deve andare in Germania. Chi impara una professione tecnica in Mali con un percorso di carriera non ha bisogno di un container berlinese. Chi lavora in Colombia al programma CO₂ non ha bisogno di Madrid.",
        'p_asyl3': "Questo non è un argomento anti-migrazione. È un argomento pro-futuro. Per le persone oggi bloccate come richiedenti asilo in Europa — spesso costrette da circostanze che non hanno scelto — la Cintura-Mondiale offre ciò che il nostro mercato del lavoro e la burocrazia strutturalmente rifiutano loro: <strong>un futuro.</strong> Il ritorno diventa allora non una deportazione, ma un incarico. Chi oggi è a Ter Apel o Nauen può domani essere specialista tecnico a Nouakchott o Gibuti in un programma diretto dagli europei.",
        'p_asyl4': "Ciò che centomila assistenti sociali e interpreti europei non possono raggiungere, il programma climatico raggiunge da solo. Non \"rimandando le persone indietro\", ma dando loro una ragione per <em>volere</em> tornare: un lavoro, una carriera, una famiglia, un paese che ha di nuovo un futuro.",
        'h2_7': "Ciò che rimane — 135 croci rosse sulla mappa",
        'p_rest1': "Le 135 zone che rimangono non redditizie anche a €80 per tonnellata meritano anche menzione esplicita. Sono concentrate nelle aree più secche, più frammentate: interno egiziano, altipiani siriani e iracheni, montagne yemenite, Rub-al-Khali. Fisicamente semplicemente troppo secche. Politicamente troppo instabili. Paesaggisticamente troppo frammentate. Sulla mappa del mondo in cima a questo articolo, queste sono le croci rosse. Vengono saltate. Punto.",
        'p_rest2': "Anche Levante, Sud Europa mediterraneo, Terre marginali iberiche e Bordo delle steppe balcaniche sono tecnicamente possibili ma economicamente marginali e climatico-politicamente appena necessari. Per 2040-neutrale e 2050 −50% non sono necessari. Sono solo un'opzione se i rovesci nei corridoi principali si accumulano.",
        'h2_8': "Cos'è questo, e cosa non è",
        'p_conc1': "Questa non è un'utopia e non una techno-fix. È una proposta di investimento differenziata e calcolata per un'operazione climatica concreta su 290 zone redditizie. È tecnicamente fattibile con tecnologia esistente — Juncao e Moringa già crescono oggi nelle aree obiettivo, le macchine sono un ridimensionamento della tecnologia agricola esistente, la verifica satellitare esiste da dieci anni. È economicamente redditizio a un prezzo di mercato già raggiunto oggi nel EU ETS.",
        'p_conc2': "È politicamente difficile perché rompe tre tabù contemporaneamente. Dice che parti dello sforzo climatico in Europa (mediterraneo, iberico, balcanico) sono inutili e devono essere saltate. Posiziona la politica climatica come <strong>industria di crescita</strong> invece che industria di perdita. E disegna una prospettiva di ritorno per i migranti che riconosce esplicitamente: la nostra democrazia non offre loro strutturalmente futuro.",
        'p_conc3': "Questo giornale pensa che sia tempo per questi tre tabù. Il calcolo è pronto. Le macchine possono essere costruite. I paesi vogliono. Ciò che rimane è il coraggio politico di scegliere la <strong>differenziazione</strong> sul consenso, l'<strong>industria</strong> sull'austerità, e l'<strong>onestà sulla migrazione</strong> sull'autoinganno.",
        'bron': "<strong>Fonti.</strong> Calcoli basati su 425 segmenti di corridoio (geografia, temperatura, precipitazioni, rugiada, resa in biomassa per ettaro, CAPEX/OPEX macchine, dimensione del campo, costi del lavoro specifici per paese). Per un contesto più ampio vedi il modello Excel completo Verbreding_Strategie_v3.xlsx e il rapporto correlato Plan_2040_2050. Per la fisica del sequestro di CO₂ tramite Juncao e Moringa vedi <a href=\"../../nl/editie-5/artikel-05-plant-die-verhuist.html\">La pianta che si trasferisce</a> e <a href=\"../../nl/editie-5/artikel-03-vergeten-orde.html\">L'ordine dimenticato</a>.",
    },

    'pt': {
        'lead': "O problema climático já não precisa de uma solução ideológica. Precisa de um plano de construção diferenciado, construído a partir de hectares, toneladas de CO₂ e euros por tonelada. Este jornal fez esse cálculo para 425 segmentos de corredor de 100 km à volta do Saara, ao longo dos Andes, através do norte da Austrália, através da Anatólia e ao longo das estepes russas e cazaques. O que emerge é uma estratégia que quebra três tabus ao mesmo tempo: declara que áreas são não rentáveis e portanto devem ser omitidas, não exige sacrifício mas oferece 840.000 novos empregos na Europa, e dá aos requerentes de asilo uma perspetiva de futuro concreta em África que a nossa própria democracia não lhes pode oferecer.",
        'kpi': [('290', 'zonas rentáveis a €40/tCO₂ — de 425 calculadas'),
                ('21,1 Gt', 'sequestro de CO₂ por ano a largura base 100 km'),
                ('80,8 Gt', 'CO₂ à expansão máxima — 84% mais que mesmo o objetivo 2050'),
                ('840.000', 'novos empregos na UE em construção de máquinas e eletrónica')],
        'h2_1': 'A questão não é "conseguimos", mas "onde e com que largura"',
        'p_q1': "Quinze anos de debate climático mantiveram a discussão na mesma questão — quanto devemos reduzir, quão depressa, e quem paga os custos. A questão inversa raramente é levantada: quanto CO₂ pode a terra reabsorver com meios industriais existentes, e quanto custa por tonelada? Este jornal fez esse cálculo em 425 lugares concretos, cada um com 100 km de comprimento, em secções de 100 km de largura. Cada segmento foi calculado segundo temperatura, precipitação, orvalho, tamanho do campo e utilização de máquinas.",
        'p_q2': "<strong>O resultado é de simplicidade desconcertante.</strong> Das 425 zonas, apenas 290 revelam-se verdadeiramente rentáveis a um preço de mercado de €40 por tonelada de CO₂. O resto — 135 zonas — tem um custo superior a €40. Estas recebem uma cruz vermelha no mapa. Estão todas em áreas demasiado secas ou demasiado fragmentadas: o interior egípcio, o Levante, partes da Península Arábica, e as partes mais fragmentadas do sul da Europa.",
        'quote_1': "Alargar as zonas rentáveis oferece mais impacto climático por euro investido do que expandir para zonas não rentáveis. Parece óbvio. No entanto, nenhuma organização climática o formulou nunca desta forma.",
        'fig1_cap': "Os 12 corredores diferem enormemente em espaço físico. O norte da Austrália tem 600 km disponíveis, o sul da Europa apenas 30. Aplicar a mesma largura em todo o lado é ingénuo.",
        'h2_2': 'A resposta é diferenciada — 30 km aqui, 600 km ali',
        'p_diff': "Os planos climáticos gostam de falar com um único número. Este estudo não pode. A largura máxima física por corredor varia por um fator de vinte: de 30 km no sul da Europa (fragmentada por aldeias, olivais, vinhas e mar) a 600 km no Top End australiano (vazio até ao horizonte, com cooperação aborígene). Cada corredor recebe exatamente tanta largura quanto a sua geografia permite.",
        'tabel1_cap_col': ['Corredor', 'Largura máx', 'CO₂ máx Gt/ano', 'Custo', 'Fator limitante'],
        'tabel1_data': [
            ('<strong>Norte da Austrália</strong>', '600 km', '13,4', '€10,53', 'Top End vazio, Acordos de Utilização de Terras Aborígenes'),
            ('<strong>Saara Costa-a-Costa</strong>', '500 km', '24,9', '€14,49', 'Borda sul do Saara da Mauritânia ao Djibuti'),
            ('<strong>América do Sul Andes-Amazónia</strong>', '400 km', '29,1', '€7,50', 'Sopé; não em floresta pluvial'),
            ('Estepes do Sul da Rússia', '400 km', '5,1', '€17,68', 'Legado soviético de grandes blocos'),
            ('Estepes da Ásia Central', '500 km', '2,8', '€26,44', 'Estepes cazaques, pouca população'),
            ('Anatólia-Cáucaso-Irão', '200 km', '2,3', '€20,74', 'Fragmentação de planaltos'),
            ('Península Arábica', '400 km', '0,8', '€23,24', 'A água é fator limitante'),
            ('Norte do Saara (Marrocos-Egito)', '300 km', '0,8', '€32,62', 'Fragmentação política Líbia, Egito'),
            ('Borda das estepes balcânicas', '80 km', '0,6', '€22,06', 'Planaltos marginais entre agricultura'),
            ('Terras marginais ibéricas', '60 km', '0,5', '€29,83', 'Fragmentadas pelas aldeias'),
            ('Levante', '50 km', '0,09', '€28,59', 'Instabilidade política, população densa'),
            ('Sul da Europa mediterrânico', '30 km', '0,4', '€30,61', 'Fortemente fragmentado por aldeias, mar'),
        ],
        'tabel1_totaal': ['TOTAL', 'varia', '80,8', 'pond. €14,91', 'Máximo físico global'],
        'p_kost': "O custo médio sobre todas as 290 zonas rentáveis a largura base 100 km é <strong>€14,91 por tonelada de CO₂</strong>. A América do Sul sai melhor a €7,50; o sul da Europa pior a €30,61. Não é uma escolha política mas física: eficiência da fotossíntese = temperatura × luz × água. Nos trópicos os três estão presentes durante todo o ano, na Europa apenas 5 a 7 meses.",
        'h2_3': 'Os objetivos 2040 e 2050 — com preços de mercado que ninguém precisa minimizar',
        'p_targets': "Se as emissões mundiais de CO₂ sob uma política de redução realista caem de 37,4 Gt em 2024 para 29,3 Gt em 2040 e 17,5 Gt em 2050, então o nosso sequestro em 2040 deve pelo menos compensar essas 29,3 Gt para ser climaticamente neutro. Para 2050 pelo menos 25% negativo, é preciso remover 26,9 Gt por ano; para 50% negativo 36,2 Gt por ano.",
        'fig2_cap': "A linha vermelha mostra business-as-usual com crescimento +1%/ano. A linha dourada mostra redução gradual através da política climática. A linha verde-escura o nosso sequestro através do Cinturão-Mundial — construindo constantemente desde zero em 2026 até 36 Gt/ano em 2050.",
        'p_marktprijs': "O preço de mercado para a remoção de CO₂ situa-se hoje entre €40 e €80 por tonelada. Este preço de mercado é mantido no plano — sem pressão sobre preços, sem dumping. A um preço de mercado de €40 a margem líquida sobre as 290 zonas é €25,09 por tonelada; a €80 torna-se €65,09 por tonelada. O que resta como lucro é substancial mas não extático: <strong>€529 mil milhões por ano a €40, €1.373 mil milhões a €80</strong>. Suficiente para construir todas as máquinas, instalar toda a infraestrutura e dar a África uma economia estrutural — e dar aos países anfitriões a sua parte justa na operação climática mundial.",
        'fig3_cap': "Lucro líquido por corredor por ano. América do Sul e Saara juntos entregam quase dois terços do lucro global — tanto a €40 como a €80 de preço de mercado.",
        'tabel2_col': ['Preço de mercado', 'Margem/tonelada', 'Lucro base 100 km', 'Lucro máx físico'],
        'tabel2_data': [
            ('<strong>€40/tCO₂</strong>', '€25,09', '€529 Mrd./ano', '€2.027 Mrd./ano'),
            ('<strong>€60/tCO₂</strong>', '€45,09', '€951 Mrd./ano', '€3.643 Mrd./ano'),
        ],
        'tabel2_totaal': ['€80/tCO₂', '€65,09', '€1.373 Mrd./ano', '€5.259 Mrd./ano'],
        'h2_4': 'Que largura deve ter cada área?',
        'p_uitrol': "O rollout ótimo segue o retorno por passo. Cada 100 km de ampliação é classificado por lucro por hectare — e o mais rentável vem primeiro. A resposta não é \"175 km em todo o lado\". É: primeiro América do Sul aos 400 km completos, depois norte da Austrália a 400 km, depois Saara Costa-a-Costa a 500 km. O sul da Europa apenas recebe os seus 30 km físicos — ou zero, se não for necessário.",
        'fig4_cap': "A uma largura média de 139 km sobre as 290 zonas rentáveis, 2040 climaticamente neutro é atingível. A 172 km médios, 2050 −50% negativo está à vista.",
        'p_2040': "<strong>Rollout 2040:</strong> América do Sul Andes-Amazónia aos 400 km completos (29,1 Gt/ano, €527 Mrd. de lucro @€80); norte da Austrália a 100 km (2,2 Gt/ano, €155 Mrd. de lucro); Saara Costa-a-Costa em fase piloto 15 km para infraestrutura e coordenação da Grande Muralha Verde. Todos os outros corredores: ainda não ativos.",
        'p_2050': "<strong>Rollout 2050 (−50% negativo):</strong> América do Sul aos 400 km completos; norte da Austrália expandido para 400 km (8,9 Gt/ano); Saara ainda como reserva. Todos os corredores europeus: ainda 0 km. Desnecessários para estes objetivos.",
        'h2_5': '840.000 novos empregos na Europa — isto não é uma narrativa de austeridade',
        'p_jobs1': "O que é notável neste plano climático é que não é uma narrativa de austeridade e não pede sacrifício ao cidadão europeu. É uma expansão industrial numa escala que a Europa não vê desde a reconstrução do pós-guerra. As máquinas — 6 metros de largura, 1000 metros por hora, 300 litros de combustível por hora, com monitorização de condição por IA e verificação por satélite — são construídas na Alemanha, Países Baixos, Itália e França. A eletrónica e módulos IA vêm de fornecedores suíços e suecos. Os componentes vêm de dezenas de milhares de PMEs europeias.",
        'p_jobs2': "Cerca de 98.000 máquinas necessárias em todo o mundo no máximo físico, com ciclo de substituição de cinco anos — significa 20.000 máquinas por ano em produção contínua. Cada máquina custa aproximadamente €875.000 em CAPEX mais €25.000 em módulos IA. Cerca de 40% disto vai para horas de trabalho: design, montagem, eletrónica, teste, serviço. A um custo laboral europeu médio de €70.000 por FTE por ano, isto entrega <strong>840.000 novos empregos</strong>.",
        'fig5_cap': "Distribuição dos 840.000 novos empregos europeus entre construção de máquinas, eletrónica, fornecedores, manutenção, I&D, logística e equipas de destacamento em África.",
        'fte_labels': [('280.000', 'Construção de máquinas — Alemanha, Países Baixos, Itália — chassis, motores, hidráulica'),
                      ('180.000', 'Componentes e fornecedores PMEs distribuídos na UE'),
                      ('120.000', 'Eletrónica e módulos IA — sensores, ligação satélite, verificação'),
                      ('90.000', 'Manutenção e frotas de serviço entre Europa e corredores'),
                      ('70.000', 'Design, I&D e laboratórios biotecnológicos para melhoria de plantas'),
                      ('100.000', 'Logística, escritório e equipas de destacamento em África')],
        'p_jobs3': "Estes 840.000 empregos são estruturais, não cíclicos. Existem enquanto o programa climático existir — pelo menos 30 anos. Estão distribuídos regionalmente por todos os Estados-membros da UE com capacidade industrial. E não exigem requalificação de pessoas que hoje já trabalham na indústria automóvel, siderúrgica ou de manufactura.",
        'h2_6': 'Os requerentes de asilo como parceiros — uma perspetiva de futuro que a nossa democracia não pode oferecer',
        'p_asyl1': "A maior verdade política que este plano climático revela é uma que a Europa prefere não dizer em voz alta: a nossa \"democracia\" não oferece a centenas de milhares de requerentes de asilo qualquer perspetiva de futuro. Chegam em tendas e contentores, esperam anos pelos procedimentos, não têm permissão para trabalhar, e uma vez recebido o estatuto, a primeira geração é impotente no mercado de trabalho e a segunda alienada de ambas as culturas. Isto não é um fracasso de intenções — é um fracasso estrutural da sociedade europeia como funciona hoje.",
        'p_asyl2': "O Cinturão-Mundial oferece algo essencialmente diferente. Na Mauritânia, Mali, Níger, Chade, Sudão, Etiópia, Colômbia, Peru e Bolívia surgirão centenas de milhares de empregos nos próximos 25 anos — maquinistas, técnicos, analistas de satélite, verificadores, coordenadores, biólogos de plantas, gestores de água. Os empregos são novos, de alto valor, ecologicamente significativos e pagos a nível de mercado mundial com um decente adicional sobre os salários locais. São exatamente o que o migrante de primeira geração procura e raramente encontra na Europa: <strong>trabalho com significado, na sua própria região, na sua própria língua, com perspetiva de uma carreira e uma família.</strong>",
        'quote_2': "Quem tem um bom emprego na Mauritânia no programa climático não precisa ir para a Alemanha. Quem aprende uma profissão técnica no Mali com um percurso de carreira não precisa de um contentor berlinense. Quem trabalha na Colômbia no programa CO₂ não precisa de Madrid.",
        'p_asyl3': "Este não é um argumento anti-migração. É um argumento pró-futuro. Para as pessoas hoje presas como requerentes de asilo na Europa — muitas vezes forçadas por circunstâncias que não escolheram — o Cinturão-Mundial oferece o que o nosso mercado de trabalho e burocracia lhes recusam estruturalmente: <strong>um futuro.</strong> O regresso torna-se então não uma deportação, mas uma nomeação. Quem hoje está em Ter Apel ou Nauen pode amanhã ser especialista técnico em Nuaquechote ou Djibuti num programa dirigido pelos europeus.",
        'p_asyl4': "O que cem mil assistentes sociais e intérpretes europeus não conseguem alcançar, o programa climático alcança por si só. Não \"mandando pessoas de volta\", mas dando-lhes uma razão para <em>quererem</em> voltar: um emprego, uma carreira, uma família, um país que tem novamente um futuro.",
        'h2_7': 'O que resta — 135 cruzes vermelhas no mapa',
        'p_rest1': "As 135 zonas que permanecem não rentáveis mesmo a €80 por tonelada também merecem menção explícita. Estão concentradas nas áreas mais secas, mais fragmentadas: interior egípcio, planaltos sírios e iraquianos, montanhas iemenitas, Rub-al-Khali. Fisicamente simplesmente demasiado secas. Politicamente demasiado instáveis. Paisagisticamente demasiado fragmentadas. No mapa mundial no topo deste artigo, estas são as cruzes vermelhas. São omitidas. Ponto.",
        'p_rest2': "Também Levante, Sul da Europa mediterrânico, Terras marginais ibéricas e Borda das estepes balcânicas são tecnicamente possíveis mas economicamente marginais e climático-politicamente pouco necessários. Para 2040-neutro e 2050 −50% não são necessários. São apenas uma opção se os contratempos nos corredores principais se acumularem.",
        'h2_8': 'O que isto é, e o que não é',
        'p_conc1': "Isto não é uma utopia e não uma techno-fix. É uma proposta de investimento diferenciada e calculada para uma operação climática concreta em 290 zonas rentáveis. É tecnicamente viável com tecnologia existente — Juncao e Moringa já crescem hoje nas áreas alvo, as máquinas são um escalar de tecnologia agrícola existente, a verificação por satélite existe há dez anos. É economicamente rentável a um preço de mercado já atingido hoje no EU ETS.",
        'p_conc2': "É politicamente difícil porque quebra três tabus ao mesmo tempo. Diz que partes do esforço climático na Europa (mediterrânico, ibérico, balcânico) são inúteis e devem ser omitidas. Posiciona a política climática como uma <strong>indústria de crescimento</strong> em vez de indústria de perda. E esboça uma perspetiva de regresso para migrantes que reconhece explicitamente: a nossa democracia não lhes oferece estruturalmente futuro.",
        'p_conc3': "Este jornal acha que é altura para estes três tabus. O cálculo está feito. As máquinas podem ser construídas. Os países querem. O que resta é a coragem política de escolher <strong>diferenciação</strong> sobre consenso, <strong>indústria</strong> sobre austeridade, e <strong>honestidade sobre migração</strong> sobre autoilusão.",
        'bron': "<strong>Fontes.</strong> Cálculos baseados em 425 segmentos de corredor (geografia, temperatura, precipitação, orvalho, produtividade de biomassa por hectare, CAPEX/OPEX máquinas, tamanho do campo, custos laborais específicos por país). Para contexto mais amplo ver o modelo Excel completo Verbreding_Strategie_v3.xlsx e o relatório correspondente Plan_2040_2050. Para a física do sequestro de CO₂ via Juncao e Moringa ver <a href=\"../../nl/editie-5/artikel-05-plant-die-verhuist.html\">A planta que se muda</a> e <a href=\"../../nl/editie-5/artikel-03-vergeten-orde.html\">A ordem esquecida</a>.",
    },
}


def build_html(taal, cfg, inhoud):
    nav_html = '\n'.join(f'      <li><a href="{href}">{label}</a></li>' for href, label in cfg['nav_links'])

    kpis = ''.join(f'''
      <div class="cijferblok__cel">
        <div class="cijferblok__cijfer">{v}</div>
        <div class="cijferblok__label">{lbl}</div>
      </div>''' for v, lbl in inhoud['kpi'])

    fte = ''.join(f'''
      <div class="cijferblok__cel">
        <div class="cijferblok__cijfer">{v}</div>
        <div class="cijferblok__label">{lbl}</div>
      </div>''' for v, lbl in inhoud['fte_labels'])

    t1_col = inhoud['tabel1_cap_col']
    t1_rows = ''.join(
        f'          <tr><td>{n}</td><td class="getal">{w}</td><td class="getal">{c}</td><td class="getal">{k}</td><td>{f}</td></tr>\n'
        for n, w, c, k, f in inhoud['tabel1_data']
    )
    t1_totaal_row = inhoud['tabel1_totaal']
    t1_totaal = (f'          <tr class="totaal"><td>{t1_totaal_row[0]}</td>'
                 f'<td class="getal">{t1_totaal_row[1]}</td>'
                 f'<td class="getal">{t1_totaal_row[2]}</td>'
                 f'<td class="getal">{t1_totaal_row[3]}</td>'
                 f'<td>{t1_totaal_row[4]}</td></tr>\n')

    t2_col = inhoud['tabel2_col']
    t2_rows = ''.join(
        f'          <tr><td>{a}</td><td class="getal">{b}</td><td class="getal">{c}</td><td class="getal">{d}</td></tr>\n'
        for a, b, c, d in inhoud['tabel2_data']
    )
    t2_totaal_row = inhoud['tabel2_totaal']
    t2_totaal = (f'          <tr class="totaal"><td>{t2_totaal_row[0]}</td>'
                 f'<td class="getal">{t2_totaal_row[1]}</td>'
                 f'<td class="getal">{t2_totaal_row[2]}</td>'
                 f'<td class="getal">{t2_totaal_row[3]}</td></tr>\n')

    return f'''<!DOCTYPE html>
<html lang="{cfg['lang_attr']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cfg['titel']} · Het Open Vizier</title>
  <meta name="description" content="{cfg['ondertitel']}">
  <link rel="stylesheet" href="../../assets/style.css">
  <link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://openvizier.org/{taal}/{cfg['wo_map']}/{cfg['slug']}.html">
  <meta property="og:title" content="{cfg['titel']}">
  <meta property="og:description" content="{cfg['ondertitel']}">
  <meta property="og:image" content="https://openvizier.org/assets/wat-opkomt/H_wereldgordel.jpg">
  <meta property="og:site_name" content="Het Open Vizier">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{cfg['titel']}">
  <meta name="twitter:image" content="https://openvizier.org/assets/wat-opkomt/H_wereldgordel.jpg">
  <style>
    .wo-artikel {{ max-width: 780px; margin: 2rem auto 1rem auto; padding: 0 1.25rem; }}
    .wo-artikel__meta {{ text-align: center; color: #6b7280; font-size: 0.85rem; letter-spacing: 0.05em; text-transform: uppercase; margin: 2rem 0 1rem 0; }}
    .wo-artikel__titel {{ font-family: var(--font-serif, Georgia, serif); font-size: clamp(2rem, 5.5vw, 3rem); line-height: 1.2; text-align: center; margin: 0.5rem 0 0.5rem 0; color: #1a1a1a; }}
    .wo-artikel__subtitle {{ text-align: center; color: #4a5263; font-style: italic; font-family: var(--font-serif, Georgia, serif); font-size: clamp(1.05rem, 2.3vw, 1.2rem); margin: 0.5rem auto 2rem auto; max-width: 640px; }}
    .wo-artikel__auteur {{ text-align: center; color: #6b7280; font-size: 0.95rem; margin: 0 0 3rem 0; }}
    .wo-artikel__streep {{ width: 60px; height: 4px; background: #1c5760; margin: 2.5rem auto; }}
    .wo-artikel__hero {{ max-width: 1280px; margin: 0 auto 2rem auto; padding: 0 1.25rem; }}
    .wo-artikel__hero img {{ display: block; width: 100%; max-width: 780px; height: auto; margin: 0 auto; border: 1px solid #d4d1ca; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .wo-artikel__inhoud {{ font-family: var(--font-serif, Georgia, serif); font-size: clamp(1.05rem, 2.3vw, 1.15rem); line-height: 1.75; color: #2a2a2a; }}
    .wo-artikel__inhoud p {{ margin: 0 0 1.5rem 0; }}
    .wo-artikel__inhoud h2 {{ font-family: var(--font-serif, Georgia, serif); font-size: clamp(1.5rem, 3.5vw, 1.9rem); line-height: 1.3; margin: 3rem 0 1rem 0; color: #1a1a1a; }}
    .wo-artikel__inhoud blockquote {{ margin: 1.8rem 0; padding: 0.4rem 1.25rem; border-left: 4px solid #1c5760; background: #faf5ea; font-style: italic; color: #2b2b2b; }}
    .wo-artikel__inhoud .cijferblok {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; margin: 2rem 0; }}
    .wo-artikel__inhoud .cijferblok__cel {{ background: #f5f3ee; border-left: 3px solid #1c5760; padding: 0.9rem 1rem; }}
    .wo-artikel__inhoud .cijferblok__cijfer {{ font-family: var(--font-serif, Georgia, serif); font-size: 1.6rem; font-weight: 700; color: #1c5760; line-height: 1.1; margin: 0 0 0.3rem 0; }}
    .wo-artikel__inhoud .cijferblok__label {{ font-size: 0.85rem; color: #4a5263; line-height: 1.35; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    .wo-artikel__inhoud .bronblok {{ margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid #d4d1ca; font-size: 0.9rem; color: #4a5263; }}
    .wo-artikel__inhoud .grafiek {{ margin: 2.5rem 0; }}
    .wo-artikel__inhoud .grafiek img {{ display: block; width: 100%; height: auto; border: 1px solid #d4d1ca; }}
    .wo-artikel__inhoud .grafiek figcaption {{ font-size: 0.88rem; color: #6b7280; font-style: italic; text-align: center; padding-top: 0.5rem; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    .wo-artikel__inhoud .tabel {{ margin: 2rem 0; overflow-x: auto; }}
    .wo-artikel__inhoud .tabel table {{ width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 0.92rem; }}
    .wo-artikel__inhoud .tabel th {{ background: #1c5760; color: #f5f0e6; padding: 0.6rem 0.7rem; text-align: left; font-weight: 700; font-size: 0.85rem; }}
    .wo-artikel__inhoud .tabel td {{ padding: 0.5rem 0.7rem; border-bottom: 1px solid #d4d1ca; vertical-align: top; }}
    .wo-artikel__inhoud .tabel tr:last-child td {{ border-bottom: none; }}
    .wo-artikel__inhoud .tabel tr.totaal {{ background: #f5f3ee; font-weight: 700; }}
    .wo-artikel__inhoud .tabel td.getal {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .wo-artikel__terug {{ text-align: center; margin: 3rem 0 1rem 0; }}
    .wo-artikel__terug a {{ color: #1c5760; text-decoration: none; font-size: 0.95rem; }}
  </style>
</head>
<body>

<header class="masthead" style="position:relative;">
  <a href="/" class="masthead__taal">
    <span class="masthead__taal__huis" aria-hidden="true">⌂</span>
    <span class="masthead__taal__label">Lang</span>
    <span class="masthead__taal__cur">· {cfg['nav_lang']}</span>
  </a>
  <div class="masthead__date">{cfg['masthead_date']}</div>
  <h1 class="masthead__title"><a href="../" style="color:inherit;text-decoration:none">Het Open Vizier</a></h1>
  <p class="masthead__tagline">{cfg['masthead_tagline']}</p>
</header>

<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
{nav_html}
    </ul>
  </div>
</nav>

<div class="wo-artikel__hero">
  <img src="../../assets/wat-opkomt/H_wereldgordel.jpg" alt="{cfg['titel']}" loading="eager">
</div>

<article class="wo-artikel">
  <p class="wo-artikel__meta">{cfg['meta_line']}</p>
  <h1 class="wo-artikel__titel">{cfg['titel']}</h1>
  <p class="wo-artikel__subtitle">{cfg['ondertitel']}</p>
  <p class="wo-artikel__auteur">{cfg['author_line']}</p>

  <div class="wo-artikel__streep"></div>

  <div class="wo-artikel__inhoud">

    <p>{inhoud['lead']}</p>

    <div class="cijferblok">{kpis}
    </div>

    <h2>{inhoud['h2_1']}</h2>
    <p>{inhoud['p_q1']}</p>
    <p>{inhoud['p_q2']}</p>
    <blockquote>{inhoud['quote_1']}</blockquote>

    <figure class="grafiek">
      <img src="../../assets/wat-opkomt/graf_klimaat_3_max_breedte.jpg" alt="">
      <figcaption>{inhoud['fig1_cap']}</figcaption>
    </figure>

    <h2>{inhoud['h2_2']}</h2>
    <p>{inhoud['p_diff']}</p>

    <div class="tabel">
      <table>
        <thead><tr><th>{t1_col[0]}</th><th>{t1_col[1]}</th><th>{t1_col[2]}</th><th>{t1_col[3]}</th><th>{t1_col[4]}</th></tr></thead>
        <tbody>
{t1_rows}{t1_totaal}        </tbody>
      </table>
    </div>

    <p>{inhoud['p_kost']}</p>

    <h2>{inhoud['h2_3']}</h2>
    <p>{inhoud['p_targets']}</p>

    <figure class="grafiek">
      <img src="../../assets/wat-opkomt/graf_klimaat_1_tijdlijn.jpg" alt="">
      <figcaption>{inhoud['fig2_cap']}</figcaption>
    </figure>

    <p>{inhoud['p_marktprijs']}</p>

    <figure class="grafiek">
      <img src="../../assets/wat-opkomt/graf_klimaat_2_winst_corridor.jpg" alt="">
      <figcaption>{inhoud['fig3_cap']}</figcaption>
    </figure>

    <div class="tabel">
      <table>
        <thead><tr><th>{t2_col[0]}</th><th>{t2_col[1]}</th><th>{t2_col[2]}</th><th>{t2_col[3]}</th></tr></thead>
        <tbody>
{t2_rows}{t2_totaal}        </tbody>
      </table>
    </div>

    <h2>{inhoud['h2_4']}</h2>
    <p>{inhoud['p_uitrol']}</p>

    <figure class="grafiek">
      <img src="../../assets/wat-opkomt/graf_klimaat_4_verbreding.jpg" alt="">
      <figcaption>{inhoud['fig4_cap']}</figcaption>
    </figure>

    <p>{inhoud['p_2040']}</p>
    <p>{inhoud['p_2050']}</p>

    <h2>{inhoud['h2_5']}</h2>
    <p>{inhoud['p_jobs1']}</p>
    <p>{inhoud['p_jobs2']}</p>

    <figure class="grafiek">
      <img src="../../assets/wat-opkomt/graf_klimaat_5_fte.jpg" alt="">
      <figcaption>{inhoud['fig5_cap']}</figcaption>
    </figure>

    <div class="cijferblok">{fte}
    </div>

    <p>{inhoud['p_jobs3']}</p>

    <h2>{inhoud['h2_6']}</h2>
    <p>{inhoud['p_asyl1']}</p>
    <p>{inhoud['p_asyl2']}</p>
    <blockquote>{inhoud['quote_2']}</blockquote>
    <p>{inhoud['p_asyl3']}</p>
    <p>{inhoud['p_asyl4']}</p>

    <h2>{inhoud['h2_7']}</h2>
    <p>{inhoud['p_rest1']}</p>
    <p>{inhoud['p_rest2']}</p>

    <h2>{inhoud['h2_8']}</h2>
    <p>{inhoud['p_conc1']}</p>
    <p>{inhoud['p_conc2']}</p>
    <p>{inhoud['p_conc3']}</p>

    <div class="bronblok">{inhoud['bron']}</div>
  </div>

  <div class="wo-artikel__terug"><a href="./">{cfg['back_link']}</a></div>
</article>

<footer style="background:#1c5760; color:#f5f0e6; padding:2rem 1.5rem; text-align:center; margin-top:2rem;">
  <div><strong>Het Open Vizier</strong></div>
  <div style="margin-top:.4rem;"><a href="https://openvizier.org" style="color:#ffd700;">openvizier.org</a></div>
</footer>

</body>
</html>
'''


print("=== Volledige body-vertalingen schrijven voor DE/RU/FR/ES/IT/PT ===\n")
for taal, cfg in TALEN.items():
    inhoud = INHOUD[taal]
    html = build_html(taal, cfg, inhoud)
    output_dir = REPO / taal / cfg['wo_map']
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{cfg['slug']}.html"
    output_file.write_text(html, encoding='utf-8')
    print(f"  ✓ {taal}/{cfg['wo_map']}/{cfg['slug']}.html  ({len(html):,} bytes)")

print("\n=== Klaar ===")
