"""
Genereer cascade-grafieken voor de Stille Analyse, met BiCRS/Ethanol-lijn als extra scenario.

Output: PNG-bestanden in assets/wat-opkomt/gevolgenkaart/ met -bicrs-suffix
(blijven naast bestaande huidige-beleid versies).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa - registers projection
import numpy as np
from pathlib import Path

# ============================================================
# STIJL & PALET
# ============================================================
BG = "#ffffff"
TEXT = "#1a1a1a"
GREY = "#6b7280"
GREY_LIGHT = "#d4d1ca"
PLANE = "#cfe1f0"

# Kwadrant-titel kleuren
COL_PLUNDERAARS = "#b81e3a"   # rood
COL_MEELOPERS   = "#d97a1f"   # oranje
COL_WIJZENDEN   = "#1c5760"   # teal
COL_VERDEDIGERS = "#0e3d2e"   # donkergroen

# Partij-kleuren (per partij consistent)
PARTIJ_KLEUREN = {
    "GroenLinks-PvdA": "#b81e3a",
    "D66": "#16a085",
    "CDA": "#8a8a85",
    "ChristenUnie": "#5d7799",
    "VVD": "#1e88e5",
    "BBB": "#d2b04c",
    "NSC": "#c0392b",
    "SGP": "#5d4037",
    "PVV": "#1e6091",
    "FvD": "#7d3c98",
    "JA21": "#16537e",
    "Nova Democratia": "#0e3d2e",
}

# Kleur van BiCRS-overlay
COL_BICRS = "#2ea043"  # helderder groen voor zichtbaarheid op alle kwadranten
COL_BICRS_FILL = "#a8d5b9"

JAREN = [2027, 2028, 2029, 2030]

# ============================================================
# PROFIEL-DATA
# Per profiel: voor elke partij een eindwaarde 2030 (€/jr).
# Lijnen lopen van €0 in 2027 lineair naar eindwaarde 2030.
# ============================================================

# DGA 58 jaar — €/jr verlies of winst (eindwaarde 2030)
# Gebaseerd op cascade-dga.jpg + tabel (% × inkomen 1e benadering)
DGA = {
    "scenario_naam": "DGA 58 jaar — Jacobus",
    "scenario_beschrijving": [
        "Jacobus, 58 jaar, getrouwd",
        "Eigen woning: €850.000",
        "Spaargeld: €280.000",
        "BV: €120.000 vermogen",
        "Bedrijfsopvolging in 2033",
        "Pensioenpot: €145.000",
    ],
    "partijen": {
        # Plunderaars-zone
        "GroenLinks-PvdA": -19000,
        # Meelopers-zone
        "D66": -111,
        "CDA": -5706,
        "NSC": -4305,
        "VVD": -2603,
        # Wijzenden-zone
        "PVV": -1402,
        "BBB": -352,
        "JA21": -101,
        "FvD": 550,
        # Verdedigers-zone
        "Nova Democratia": 3000,
    },
    # Mapping naar kwadrant: "P"=Plunderaars, "M"=Meelopers, "W"=Wijzenden, "V"=Verdedigers
    "kwadrant": {
        "GroenLinks-PvdA": "P",
        "D66": "M",
        "CDA": "M",
        "NSC": "M",
        "VVD": "M",
        "PVV": "W",
        "BBB": "W",
        "JA21": "W",
        "FvD": "W",
        "Nova Democratia": "V",
    },
    # BiCRS-overlay: alle partijen krijgen positieve uitkomst onder BiCRS
    # Gebaseerd op tabel-percentages × €100k inkomen ordegrootte voor DGA
    "bicrs_per_partij": {
        "GroenLinks-PvdA": 4000,   # +2 tot +6%
        "D66": 5000,                # +3 tot +7%
        "CDA": 6500,                # +4 tot +9%
        "NSC": 6000,                # +4 tot +8%
        "VVD": 7500,                # +5 tot +10%
        "PVV": 8500,                # +6 tot +11%
        "BBB": 9000,                # +6 tot +12%
        "JA21": 11000,              # +8 tot +14%
        "FvD": 11000,
        "Nova Democratia": 14000,   # +10 tot +18%
    },
    "y_min": -20000,
    "y_max": 20000,
    "y_step": 10000,
    "y_format": lambda v: f"€{int(v/1000):+d}k" if v != 0 else "€0",
    "ylabel_unit": "€/jr",
}

# Gepensioneerde 70 jaar — vergelijkbare structuur, kleinere bedragen
GEPENSIONEERDE = {
    "scenario_naam": "Gepensioneerde 70 jaar — Marie",
    "scenario_beschrijving": [
        "Marie, 70 jaar, weduwe",
        "Eigen woning: €420.000",
        "Spaargeld: €68.000",
        "AOW + pensioen: €28.500/jr",
        "Pensioenpot opgegeten",
        "Zorgkosten stijgend",
    ],
    "partijen": {
        "GroenLinks-PvdA": -4200,
        "D66": -3800,
        "CDA": -2600,
        "NSC": -2100,
        "VVD": -1400,
        "PVV": -800,
        "BBB": -350,
        "JA21": -200,
        "FvD": 180,
        "Nova Democratia": 1100,
    },
    "kwadrant": {
        "GroenLinks-PvdA": "P",
        "D66": "M",
        "CDA": "M",
        "NSC": "M",
        "VVD": "M",
        "PVV": "W",
        "BBB": "W",
        "JA21": "W",
        "FvD": "W",
        "Nova Democratia": "V",
    },
    "bicrs_per_partij": {
        "GroenLinks-PvdA": 800,
        "D66": 1000,
        "CDA": 1300,
        "NSC": 1200,
        "VVD": 1500,
        "PVV": 1800,
        "BBB": 2000,
        "JA21": 2400,
        "FvD": 2400,
        "Nova Democratia": 3500,
    },
    "y_min": -5000,
    "y_max": 5000,
    "y_step": 2500,
    "y_format": lambda v: f"€{int(v):+d}" if v != 0 else "€0",
    "ylabel_unit": "€/jr",
}

# Modale Ouders — vergelijkbaar
MODALE_OUDERS = {
    "scenario_naam": "Modaal gezin met kinderen — Lisa & Tom",
    "scenario_beschrijving": [
        "Lisa & Tom, 38/40 jaar",
        "Twee kinderen (5, 8)",
        "Gezamenlijk inkomen €78k",
        "Hypotheek: €310.000",
        "Spaargeld: €18.000",
        "Geen pensioen-buffer",
    ],
    "partijen": {
        "GroenLinks-PvdA": -7800,
        "D66": -6200,
        "CDA": -4100,
        "NSC": -3400,
        "VVD": -2200,
        "PVV": -1100,
        "BBB": -550,
        "JA21": -180,
        "FvD": 320,
        "Nova Democratia": 1800,
    },
    "kwadrant": {
        "GroenLinks-PvdA": "P",
        "D66": "M",
        "CDA": "M",
        "NSC": "M",
        "VVD": "M",
        "PVV": "W",
        "BBB": "W",
        "JA21": "W",
        "FvD": "W",
        "Nova Democratia": "V",
    },
    "bicrs_per_partij": {
        "GroenLinks-PvdA": 1500,
        "D66": 1800,
        "CDA": 2400,
        "NSC": 2200,
        "VVD": 2800,
        "PVV": 3400,
        "BBB": 3700,
        "JA21": 4500,
        "FvD": 4500,
        "Nova Democratia": 6800,
    },
    "y_min": -8000,
    "y_max": 8000,
    "y_step": 4000,
    "y_format": lambda v: f"€{int(v):+d}" if v != 0 else "€0",
    "ylabel_unit": "€/jr",
}


# ============================================================
# VERTALINGEN
# ============================================================
T = {
    "nl": {
        "title_template": "Wat uw stem u oplevert — {scenario}",
        "subtitle_template": "Tien posities, vier jaren vooruit — volledige cascade (Zuid-Afrika-pad)",
        "orde": "3e ORDE — + emigratie + generatie-effect + voorzieningenkrimp (Zuid-Afrika-pad)",
        "plunderaars": "PLUNDERAARS",
        "meelopers": "MEELOPERS",
        "wijzenden": "WIJZENDEN",
        "verdedigers": "VERDEDIGERS",
        "plunderaars_sub": "wat zij willen — vermogen herverdelen",
        "meelopers_sub": "wat zij doen — meegaan met de plundering",
        "wijzenden_sub": "wel benoemen — geen alternatief",
        "verdedigers_sub": "productiviteit en welvaartsopbouw",
        "dit_scenario": "DIT SCENARIO",
        "eindwaarde": "EINDWAARDE 2030",
        "huidig_beleid": "Huidig beleid (Green Deal + CBAM)",
        "met_bicrs": "MET BiCRS / ETHANOL — alternatief scenario",
        "hoe_lezen_kop": "HOE LEZEN",
        "hoe_lezen": "Vier zones, één schaal. Blauw vlak = €0. Lijn boven: u ontvangt. Lijn eronder: u levert in.",
        "verdedigers_leeg": "VERDEDIGERS-zone in Nederland is leeg — alleen Nova Democratia / VMP vult die positie.",
        "macro_anker": "Macro-anker: Statistics SA Q1 2026 (32,7% werkloosheid), Argentinië 2024 (pensioen-erosie 50%, bbp −3,5%), CPB-elasticiteiten.",
        "footer_left": "Het Open Vizier — gevolgenkaart.nl",
        "bicrs_label": "BiCRS-scenario — herstel via biomass-to-ethanol",
    },
    "en": {
        "title_template": "What your vote delivers — {scenario}",
        "subtitle_template": "Ten positions, four years ahead — full cascade (South Africa path)",
        "orde": "3rd ORDER — + emigration + generation effect + service erosion (South Africa path)",
        "plunderaars": "PLUNDERERS",
        "meelopers": "FOLLOWERS",
        "wijzenden": "POINTERS",
        "verdedigers": "DEFENDERS",
        "plunderaars_sub": "what they want — redistribute wealth",
        "meelopers_sub": "what they do — going along with the plunder",
        "wijzenden_sub": "naming — no alternative",
        "verdedigers_sub": "productivity and wealth building",
        "dit_scenario": "THIS SCENARIO",
        "eindwaarde": "END VALUE 2030",
        "huidig_beleid": "Current policy (Green Deal + CBAM)",
        "met_bicrs": "WITH BiCRS / ETHANOL — alternative scenario",
        "hoe_lezen_kop": "HOW TO READ",
        "hoe_lezen": "Four zones, one scale. Blue plane = €0. Line above: you receive. Line below: you pay.",
        "verdedigers_leeg": "DEFENDERS zone in the Netherlands is empty — only Nova Democratia / VMP fills that position.",
        "macro_anker": "Macro anchor: Statistics SA Q1 2026 (32.7% unemployment), Argentina 2024 (pension erosion 50%, GDP −3.5%), CPB elasticities.",
        "footer_left": "Het Open Vizier — gevolgenkaart.nl",
        "bicrs_label": "BiCRS scenario — recovery via biomass-to-ethanol",
    },
    "de": {
        "title_template": "Was Ihre Stimme bringt — {scenario}",
        "subtitle_template": "Zehn Positionen, vier Jahre voraus — vollständige Kaskade (Südafrika-Pfad)",
        "orde": "3. ORDNUNG — + Emigration + Generationeneffekt + Versorgungseinbruch (Südafrika-Pfad)",
        "plunderaars": "PLÜNDERER",
        "meelopers": "MITLÄUFER",
        "wijzenden": "ZEIGER",
        "verdedigers": "VERTEIDIGER",
        "plunderaars_sub": "was sie wollen — Vermögen umverteilen",
        "meelopers_sub": "was sie tun — bei der Plünderung mitmachen",
        "wijzenden_sub": "benennen — keine Alternative",
        "verdedigers_sub": "Produktivität und Wohlstandsaufbau",
        "dit_scenario": "DIESES SZENARIO",
        "eindwaarde": "ENDWERT 2030",
        "huidig_beleid": "Aktuelle Politik (Green Deal + CBAM)",
        "met_bicrs": "MIT BiCRS / ETHANOL — Alternativszenario",
        "hoe_lezen_kop": "WIE LESEN",
        "hoe_lezen": "Vier Zonen, eine Skala. Blaue Ebene = €0. Linie darüber: Sie erhalten. Linie darunter: Sie zahlen.",
        "verdedigers_leeg": "VERTEIDIGER-Zone in den Niederlanden ist leer — nur Nova Democratia / VMP füllt diese Position.",
        "macro_anker": "Makroanker: Statistics SA Q1 2026 (32,7% Arbeitslosigkeit), Argentinien 2024 (Renten­erosion 50%, BIP −3,5%), CPB-Elastizitäten.",
        "footer_left": "Het Open Vizier — gevolgenkaart.nl",
        "bicrs_label": "BiCRS-Szenario — Erholung über Biomass-to-Ethanol",
    },
    "ru": {
        "title_template": "Что приносит ваш голос — {scenario}",
        "subtitle_template": "Десять позиций, четыре года вперёд — полный каскад (южноафриканский путь)",
        "orde": "3-Й ПОРЯДОК — + эмиграция + поколенческий эффект + сокращение услуг (южноафриканский путь)",
        "plunderaars": "ГРАБИТЕЛИ",
        "meelopers": "ПОПУТЧИКИ",
        "wijzenden": "УКАЗАТЕЛИ",
        "verdedigers": "ЗАЩИТНИКИ",
        "plunderaars_sub": "чего они хотят — перераспределить богатство",
        "meelopers_sub": "что они делают — идут на ограбление",
        "wijzenden_sub": "называют — без альтернативы",
        "verdedigers_sub": "производительность и накопление богатства",
        "dit_scenario": "ЭТОТ СЦЕНАРИЙ",
        "eindwaarde": "ИТОГ 2030",
        "huidig_beleid": "Текущая политика (Green Deal + CBAM)",
        "met_bicrs": "С BiCRS / ЭТАНОЛОМ — альтернативный сценарий",
        "hoe_lezen_kop": "КАК ЧИТАТЬ",
        "hoe_lezen": "Четыре зоны, одна шкала. Голубая плоскость = €0. Линия выше: вы получаете. Ниже: вы платите.",
        "verdedigers_leeg": "Зона ЗАЩИТНИКОВ в Нидерландах пуста — только Nova Democratia / VMP занимает эту позицию.",
        "macro_anker": "Макро-якорь: Statistics SA Q1 2026 (32,7% безработицы), Аргентина 2024 (эрозия пенсий 50%, ВВП −3,5%), эластичности CPB.",
        "footer_left": "Het Open Vizier — gevolgenkaart.nl",
        "bicrs_label": "Сценарий BiCRS — восстановление через биомассу-в-этанол",
    },
}


# ============================================================
# RENDER-FUNCTIE
# ============================================================
def render_cascade(profile, lang_dict, scenario_naam_vert, out_path):
    """Render één cascade-grafiek met BiCRS-overlay voor een profiel in een taal."""
    fig = plt.figure(figsize=(21.25, 13.03), dpi=100, facecolor=BG)

    # Titel
    fig.text(0.018, 0.965, lang_dict["title_template"].format(scenario=scenario_naam_vert),
             fontsize=22, fontweight="bold", color=TEXT, family="serif")
    fig.text(0.018, 0.943, lang_dict["subtitle_template"],
             fontsize=13, color=GREY, family="serif", fontstyle="italic")
    fig.text(0.018, 0.923, lang_dict["orde"],
             fontsize=11, color="#0e3d2e", family="serif", fontweight="bold")

    # Vier kwadranten (4 axes)
    # Layout: 2 kolommen × 2 rijen, met ruimte rechts voor info-panel
    quadranten = [
        ("plunderaars",  COL_PLUNDERAARS,  "P", 0.04, 0.51),
        ("meelopers",    COL_MEELOPERS,    "M", 0.34, 0.51),
        ("wijzenden",    COL_WIJZENDEN,    "W", 0.04, 0.07),
        ("verdedigers",  COL_VERDEDIGERS,  "V", 0.34, 0.07),
    ]

    # Verzamel partijen per kwadrant
    partijen_per_kw = {"P": [], "M": [], "W": [], "V": []}
    for p, kw in profile["kwadrant"].items():
        partijen_per_kw[kw].append(p)

    y_min, y_max = profile["y_min"], profile["y_max"]
    y_ticks = list(range(int(y_min), int(y_max) + 1, int(profile["y_step"])))

    for kw_key, col, kw_kort, left, bottom in quadranten:
        ax = fig.add_axes([left, bottom, 0.30, 0.36], projection="3d", facecolor=BG)
        ax.set_proj_type("persp")

        # Plot het €0-vlak
        partijen = partijen_per_kw[kw_kort]
        n_partijen = max(len(partijen), 1)
        xs = np.arange(n_partijen + 1)
        ys = np.array([JAREN[0] - 0.3, JAREN[-1] + 0.3])
        X, Y = np.meshgrid(xs, ys)
        Z = np.zeros_like(X, dtype=float)
        ax.plot_surface(Y, X, Z, color=PLANE, alpha=0.18, edgecolor="none")

        # Plot per partij in deze kwadrant (huidig beleid)
        for i, partij in enumerate(partijen):
            kleur = PARTIJ_KLEUREN.get(partij, "#444")
            eindwaarde = profile["partijen"][partij]
            # Lijn van 0 (2027) naar eindwaarde (2030), licht gecurved
            jrs = np.array(JAREN, dtype=float)
            vals = np.linspace(0, eindwaarde, len(JAREN))
            # Klein deuk in midden voor realisme
            vals[1] *= 0.6
            vals[2] *= 0.85
            x_part = np.full_like(jrs, i + 0.5)
            ax.plot(jrs, x_part, vals, color=kleur, marker="o",
                    markersize=8, linewidth=2.4, zorder=5)
            # Eindwaarde-label
            label_kleur = "#0e3d2e" if eindwaarde > 0 else "#b81e3a" if eindwaarde < -500 else "#8b6800"
            ax.text(jrs[-1] + 0.15, i + 0.5, eindwaarde + (300 if eindwaarde >= 0 else -300),
                    profile["y_format"](eindwaarde),
                    color=label_kleur, fontsize=10, fontweight="bold")

            # Partij-naam onder de x-as
            ax.text(jrs[0] - 0.6, i + 0.5, y_min * 0.05, partij,
                    fontsize=9, color=TEXT, ha="right")

            # ===== BiCRS-overlay =====
            bicrs_eind = profile["bicrs_per_partij"].get(partij, 0)
            bicrs_vals = np.linspace(0, bicrs_eind, len(JAREN))
            bicrs_vals[1] *= 0.5
            bicrs_vals[2] *= 0.8
            ax.plot(jrs, x_part, bicrs_vals, color=COL_BICRS,
                    marker="^", markersize=7, linewidth=2.2,
                    linestyle="--", zorder=6, alpha=0.95)

        # Vlak-titel boven de subplot — losse fig.text voor betere control
        # left+0.15 is horizontale midden van de 0.30 brede subplot
        title_x = left + 0.15
        title_y = bottom + 0.39
        fig.text(title_x, title_y, lang_dict[kw_key], fontsize=14, color=col,
                 fontweight="bold", family="serif", ha="center")
        fig.text(title_x, title_y - 0.018, lang_dict[kw_key + "_sub"], fontsize=10,
                 color=TEXT, family="serif", ha="center", style="italic")

        # Assen
        ax.set_xlim(JAREN[0] - 0.5, JAREN[-1] + 1.2)
        ax.set_ylim(-0.5, max(n_partijen, 4) + 0.5)
        ax.set_zlim(y_min, y_max)

        ax.set_xticks(JAREN)
        ax.set_xticklabels([str(j) for j in JAREN], fontsize=8, color=GREY)
        ax.set_yticks([])
        ax.set_zticks(y_ticks)
        ax.set_zticklabels([profile["y_format"](v) for v in y_ticks], fontsize=8, color=GREY)

        # Witmaken
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor("none")
        ax.yaxis.pane.set_edgecolor("none")
        ax.zaxis.pane.set_edgecolor("none")
        ax.grid(True, color="#e8e8e3", linewidth=0.6)

        ax.view_init(elev=22, azim=-70)

    # ============================================
    # INFO-PANEEL RECHTS
    # ============================================
    info_left = 0.70
    fig.text(info_left, 0.90, lang_dict["dit_scenario"],
             fontsize=11, color=TEXT, fontweight="bold", family="serif")
    for i, lijn in enumerate(profile["scenario_beschrijving"]):
        fig.text(info_left, 0.875 - i*0.022, lijn,
                 fontsize=10, color=TEXT, family="serif")

    # Eindwaarde-tabel
    fig.text(info_left, 0.65, lang_dict["eindwaarde"],
             fontsize=11, color=TEXT, fontweight="bold", family="serif")
    fig.text(info_left, 0.63, lang_dict["huidig_beleid"],
             fontsize=9, color=GREY, fontstyle="italic", family="serif")

    # Sorteer partijen op eindwaarde (hoog naar laag)
    sorted_partijen = sorted(profile["partijen"].items(),
                              key=lambda x: x[1], reverse=True)
    for i, (p, v) in enumerate(sorted_partijen):
        y_pos = 0.605 - i*0.022
        kleur = "#0e3d2e" if v > 0 else "#b81e3a" if v < -500 else "#8b6800"
        fig.text(info_left, y_pos, p, fontsize=10, color=TEXT, family="serif")
        fig.text(info_left + 0.20, y_pos,
                 profile["y_format"](v) + "/jr",
                 fontsize=10, color=kleur, family="serif",
                 fontweight="bold")

    # BiCRS-legenda
    fig.text(info_left, 0.36, lang_dict["met_bicrs"],
             fontsize=11, color=COL_BICRS, fontweight="bold", family="serif")
    # Sample line + samples
    ax_leg = fig.add_axes([info_left, 0.32, 0.07, 0.025])
    ax_leg.axis("off")
    ax_leg.plot([0, 1], [0.5, 0.5], color=COL_BICRS, linestyle="--",
                marker="^", markersize=7, linewidth=2.2)
    ax_leg.set_xlim(0, 1); ax_leg.set_ylim(0, 1)
    fig.text(info_left + 0.08, 0.33, lang_dict["bicrs_label"],
             fontsize=9, color="#2ea043", fontstyle="italic", family="serif")

    fig.text(info_left, 0.295, "Nova Democratia (BiCRS-doel)",
             fontsize=9.5, color=TEXT, family="serif")
    bicrs_nova = profile["bicrs_per_partij"].get("Nova Democratia", 0)
    fig.text(info_left + 0.20, 0.295,
             profile["y_format"](bicrs_nova) + "/jr",
             fontsize=10, color=COL_BICRS, family="serif",
             fontweight="bold")

    # ============================================
    # HOE LEZEN (links onder)
    # ============================================
    fig.text(0.018, 0.04, lang_dict["hoe_lezen_kop"],
             fontsize=10, color=TEXT, fontweight="bold", family="serif")
    fig.text(0.018, 0.025, lang_dict["hoe_lezen"],
             fontsize=9, color=TEXT, family="serif")
    fig.text(0.018, 0.012, lang_dict["verdedigers_leeg"],
             fontsize=8.5, color=COL_VERDEDIGERS, family="serif",
             fontweight="bold", fontstyle="italic")
    fig.text(0.018, 0.002, lang_dict["macro_anker"],
             fontsize=7.5, color=GREY, family="serif", fontstyle="italic")

    fig.text(0.99, 0.012, lang_dict["footer_left"],
             fontsize=8.5, color=GREY, family="serif",
             fontstyle="italic", ha="right")

    fig.savefig(out_path, dpi=100, facecolor=BG, bbox_inches=None)
    plt.close(fig)
    print(f"  ✓ {out_path}")


# ============================================================
# RUN
# ============================================================
# Vertaalde scenario-namen + beschrijvingen per profiel × taal
SCENARIO_VERT = {
    "dga": {
        "nl": ("de DGA van 58 jaar", [
            "Jacobus, 58 jaar, getrouwd",
            "Eigen woning: €850.000",
            "Spaargeld: €280.000",
            "BV: €120.000 vermogen",
            "Bedrijfsopvolging in 2033",
            "Pensioenpot: €145.000",
        ]),
        "en": ("the 58-year-old owner-director", [
            "Jacobus, 58, married",
            "Own home: €850,000",
            "Savings: €280,000",
            "Holding: €120,000 equity",
            "Business succession in 2033",
            "Pension pot: €145,000",
        ]),
        "de": ("der GGF mit 58 Jahren", [
            "Jacobus, 58 Jahre, verheiratet",
            "Eigenheim: €850.000",
            "Ersparnisse: €280.000",
            "GmbH: €120.000 Vermögen",
            "Nachfolge im Jahr 2033",
            "Rententopf: €145.000",
        ]),
        "ru": ("директор-собственник 58 лет", [
            "Якобус, 58 лет, женат",
            "Собств. жильё: €850.000",
            "Сбережения: €280.000",
            "Компания: €120.000",
            "Преемство в 2033",
            "Пенсия: €145.000",
        ]),
    },
    "gepensioneerde": {
        "nl": ("de gepensioneerde van 70 jaar", [
            "Marie, 70 jaar, weduwe",
            "Eigen woning: €420.000",
            "Spaargeld: €68.000",
            "AOW + pensioen: €28.500/jr",
            "Pensioenpot opgegeten",
            "Zorgkosten stijgend",
        ]),
        "en": ("the 70-year-old pensioner", [
            "Marie, 70, widow",
            "Own home: €420,000",
            "Savings: €68,000",
            "State + pension: €28,500/yr",
            "Pension pot depleted",
            "Care costs rising",
        ]),
        "de": ("die Rentnerin mit 70 Jahren", [
            "Marie, 70 Jahre, verwitwet",
            "Eigenheim: €420.000",
            "Ersparnisse: €68.000",
            "AOW + Rente: €28.500/J.",
            "Rententopf aufgebraucht",
            "Pflegekosten steigen",
        ]),
        "ru": ("пенсионерка 70 лет", [
            "Мари, 70 лет, вдова",
            "Собств. жильё: €420.000",
            "Сбережения: €68.000",
            "Пенсия: €28.500/год",
            "Пенсионный фонд исчерпан",
            "Растут расходы на уход",
        ]),
    },
    "modale_ouders": {
        "nl": ("het modale gezin met kinderen", None),  # Gebruik origineel
        "en": ("the modal family with children", None),
        "de": ("die durchschnittliche Familie mit Kindern", None),
        "ru": ("средняя семья с детьми", None),
    },
}


def main():
    out_dir = Path("/tmp/gh-repo/assets/wat-opkomt/gevolgenkaart")
    out_dir.mkdir(parents=True, exist_ok=True)

    profielen = [
        ("dga", DGA),
        ("gepensioneerde", GEPENSIONEERDE),
        ("modale-ouders", MODALE_OUDERS),
    ]
    # Map naar SCENARIO_VERT keys (underscore variant)
    profiel_key_map = {
        "dga": "dga",
        "gepensioneerde": "gepensioneerde",
        "modale-ouders": "modale_ouders",
    }
    talen = ["nl", "en", "de", "ru"]

    print("=== Cascade-grafieken met BiCRS-overlay genereren ===")
    for profiel_naam, profiel in profielen:
        for taal in talen:
            suffix = "" if taal == "nl" else f"-{taal}"
            out_path = out_dir / f"cascade-{profiel_naam}-bicrs{suffix}.jpg"
            # Bepaal scenario-naam voor deze taal
            scenario_naam_vert, beschrijving_vert = SCENARIO_VERT[profiel_key_map[profiel_naam]][taal]
            # Patch profiel met vertaalde beschrijving (of laat origineel)
            if beschrijving_vert is not None:
                profiel_lokaal = dict(profiel)
                profiel_lokaal["scenario_beschrijving"] = beschrijving_vert
            else:
                profiel_lokaal = profiel
            render_cascade(profiel_lokaal, T[taal], scenario_naam_vert, out_path)


if __name__ == "__main__":
    main()
