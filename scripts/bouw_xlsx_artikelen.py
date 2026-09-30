#!/usr/bin/env python3
"""Build registered Dutch article pages from the Artikelinhoud sheet.

Article prose and publication metadata come only from vizier.xlsx.
Only marked front-page/list blocks and the registered article are written.
Existing text, articles, menus and banners are otherwise preserved.
"""
from pathlib import Path
from html import escape
from datetime import datetime
import re
import openpyxl
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
wb = openpyxl.load_workbook(REPO / "nl/_data/vizier.xlsx", data_only=True)
if "Artikelinhoud" not in wb.sheetnames:
    raise SystemExit(0)
matrix = list(wb["Knopen"].values)
headers = matrix[1]
rows = [{h: row[i] for i, h in enumerate(headers) if h} for row in matrix[2:]]
articles = {}
for row in wb["Artikelinhoud"].iter_rows(min_row=3, values_only=True):
    if row[1]:
        articles.setdefault(row[1], []).append((int(row[2]), row[3], row[4]))
template = (REPO / "scripts/templates/xlsx-artikel.html").read_text()

def replace_marked(path, key, markup, anchor):
    text = path.read_text()
    start, end = f"<!-- XLSX {key} START -->", f"<!-- XLSX {key} END -->"
    block = f"{start}\n{markup}\n{end}"
    if start in text:
        text = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, text, flags=re.S)
    else:
        assert anchor in text, f"Missing insertion anchor in {path}"
        text = text.replace(anchor, anchor + "\n" + block, 1)
    path.write_text(text)

for slug, blocks in articles.items():
    assert re.fullmatch(r"[a-z0-9-]+", slug), "Unsafe article slug"
    matching = [r for r in rows if r.get("Taal") == "nl" and r.get("URL") == f"wat-opkomt/{slug}.html"]
    assert matching, f"No matrix row for {slug}"
    record = matching[0]
    if record.get("Status") != "live" or record.get("Actief") is False:
        continue
    blocks.sort()
    first = {slot: html for _, slot, html in blocks if slot != "body"}
    raw_body = "\n".join(html for _, slot, html in blocks if slot == "body")
    body = BeautifulSoup(raw_body, "html.parser")
    toc = []
    for heading in body.find_all(["h1", "h2"]):
        if not heading.get_text(strip=True):
            heading.decompose()
            continue
        if heading.name == "h1":
            heading.name = "h2"
            toc.append(f'<a href="#{escape(heading["id"])}">{escape(heading.get_text(" ", strip=True))}</a>')
        else:
            heading.name = "h2" if heading.get("id") == "leeswijzer" else "h3"
    for table in body.find_all("table"):
        wrap = body.new_tag("div", attrs={"class": "table-scroll", "tabindex": "0", "role": "region",
            "aria-label": "Tabel; horizontaal verschuifbaar op smalle schermen"})
        table.wrap(wrap)
    in_sources = False
    for el in list(body.children):
        if not getattr(el, "name", None):
            continue
        if el.get("id") == "bronnen":
            in_sources = True
        if in_sources and el.name == "p":
            el["class"] = "source-entry"
            for text in list(el.find_all(string=True)):
                if text.parent.name == "a":
                    continue
                chunks = re.split(r"(https?://[^\s<>]+)", str(text))
                if len(chunks) < 2:
                    continue
                for chunk in chunks:
                    if chunk.startswith(("http://", "https://")):
                        a = body.new_tag("a", href=chunk, target="_blank", rel="noopener noreferrer")
                        a.string = chunk
                        text.insert_before(a)
                    else:
                        text.insert_before(chunk)
                text.extract()
    assert re.sub(r"\s+", "", BeautifulSoup(raw_body, "html.parser").get_text()) == re.sub(r"\s+", "", body.get_text())
    title = record["Naam"]
    subtitle = record.get("Ondertitel") or ""
    hero = str(record["Hero"]).replace("../", "/", 1)
    url = f"https://openvizier.org/nl/wat-opkomt/{slug}.html"
    values = {
        "TITLE": escape(title), "DESCRIPTION": escape(subtitle, quote=True), "CANONICAL": url,
        "HERO": hero, "HERO_ABSOLUTE": "https://openvizier.org" + hero,
        "SUBTITLE": first["subtitle"], "DATE": first["date"], "BODY": str(body),
        "TOC": "\n".join(toc), "PUBLICATION_DATE": str(record["Datum publicatie"]),
        "AUTHOR": escape(record.get("Auteur") or ""),
    }
    page = template
    for key, value in values.items():
        page = page.replace("{{" + key + "}}", value)
    assert "{{" not in page
    (REPO / "nl/wat-opkomt" / f"{slug}.html").write_text(page)
    day = datetime.strptime(str(record["Datum publicatie"]), "%Y-%m-%d")
    months = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
    label = f"{day.day} {months[day.month-1]} {day.year}"
    banner = f'''<a class="dgk-top" href="/nl/wat-opkomt/{slug}.html" style="background:#1a3347;border-left-color:#bf9b56;">
  <div class="dgk-top__grid">
    <div class="dgk-top__img"><img src="{hero}" alt="{escape(title)}" loading="eager" decoding="async"></div>
    <div class="dgk-top__txt">
      <p class="dgk-top__tag">NIEUW · VOORSPELLING · {label.upper()}</p>
      <h2 class="dgk-top__h">{escape(title)}</h2>
      <p class="dgk-top__l">{escape(subtitle)}</p>
      <span class="dgk-top__k">Lees de voorspelling →</span>
    </div>
  </div>
</a>'''
    replace_marked(REPO / "nl/index.html", slug, banner,
        '<script src="/assets/menu-loader.js" defer></script>')
    listing = f'''<article class="wo-item">
  <div class="wo-item__layout">
    <div class="wo-item__visual"><a href="{slug}.html"><img src="{hero}" alt="{escape(title)}" loading="eager"></a></div>
    <div class="wo-item__tekst">
      <p class="wo-item__datum">{label} · Voorspelling</p>
      <h2 class="wo-item__titel"><a href="{slug}.html">{escape(title)}</a></h2>
      <p class="wo-item__lead">{escape(subtitle)}</p>
    </div>
  </div>
</article>'''
    listing_path = REPO / "nl/wat-opkomt/index.html"
    match = re.search(r'<(?:section|div)\b[^>]*class=["\'][^"\']*\bwo-lijst\b[^"\']*["\'][^>]*>', listing_path.read_text())
    assert match, "Missing chronological article list"
    replace_marked(listing_path, slug, listing, match.group())
    print(f"Built {slug}: {len(blocks)} content blocks; front page and article list updated.")
