"""BeautifulSoup: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track3_automation/more_beautifulsoup.py
Needs:  pip install beautifulsoup4

The examples parse HTML held in strings, so they work offline and give the
same result every time. To scrape a real page, fetch the HTML first:
    html = requests.get(url, timeout=10).text
and then parse it exactly the same way. Check a site's terms and robots.txt
before scraping, and keep your request rate low.
"""

import csv
import io
import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


PAGE = """
<html>
 <head><title>Cluster Status</title>
  <script>var tracking = 1;</script><style>.x{color:red}</style></head>
 <body>
  <h1 id="title">Cluster <em>Status</em></h1>
  <p class="note">Updated <b>today</b> by <a href="/people/ana">Ana</a>.</p>
  <p class="note warning">Two nodes need attention.</p>
  <table id="nodes">
   <tr><th>Node</th><th>CPU</th><th>State</th></tr>
   <tr><td>node-1</td><td>35</td><td class="ok">up</td></tr>
   <tr><td>node-2</td><td>91</td><td class="ok">up</td></tr>
   <tr><td>node-3</td><td>0</td><td class="bad">down</td></tr>
  </table>
  <ul class="links">
   <li><a href="/docs/install">Install</a></li>
   <li><a href="https://example.com/help" target="_blank">Help</a></li>
   <li><a href="/docs/install">Install (again)</a></li>
   <li><a>No link here</a></li>
  </ul>
  <img src="/img/logo.png" alt="Logo"><img src="chart.png">
 </body>
</html>
"""

# ---------------------------------------------------------------
show(1, "Parse HTML and read basic parts")
# WHAT: turn text into a searchable tree.
# HOW : BeautifulSoup(html, "html.parser"). soup.title and soup.h1 jump to the
#       first such tag; .text / .string / .get_text() read the words.
# WHY : the starting point of every scraper.
soup = BeautifulSoup(PAGE, "html.parser")
print(soup.title.string)
print(soup.h1.text)
print(soup.h1.name, "| id =", soup.h1["id"])

# ---------------------------------------------------------------
show(2, "find and find_all")
# WHAT: locate elements by tag, class or id.
# HOW : find returns the first match (or None); find_all returns a list.
#       class_ has an underscore because class is a Python keyword.
# WHY : the basic search tools.
print(soup.find("p").text)
print(soup.find("p", class_="warning").text)
print(soup.find(id="title").name)
print(len(soup.find_all("a")), "links;", len(soup.find_all("td")), "cells")
print(soup.find("nothing"))

# ---------------------------------------------------------------
show(3, "Attributes: href, src, class")
# WHAT: read values stored in tags.
# HOW : tag["attr"] raises KeyError if absent; tag.get("attr") returns None.
#       class is returned as a LIST.
# WHY : links and images live in attributes.
for a in soup.find_all("a"):
    print(repr(a.get_text()), "->", a.get("href"))
print(soup.find("p", class_="warning")["class"])

# ---------------------------------------------------------------
show(4, "CSS selectors with select()")
# WHAT: the most flexible way to find things.
# HOW : the same selectors as CSS: tag, .class, #id, parent child,
#       parent > child, [attr], :nth-of-type().
# WHY : you can copy a selector from the browser's inspector.
print([li.text for li in soup.select("ul.links li")])
print(soup.select_one("table#nodes td.bad").text)
print([a["href"] for a in soup.select("a[href^='/docs']")])
print(soup.select("tr:nth-of-type(2) td")[0].text)
print(len(soup.select("p.note")), len(soup.select("p.warning")))

# ---------------------------------------------------------------
show(5, "Navigate the tree: parent, children, siblings")
# WHAT: move around from an element you found.
# HOW : .parent, .children, .find_next_sibling, .find_parent.
# WHY : "the value next to the label" is a very common scraping pattern.
bad = soup.select_one("td.bad")
print("row:", [td.text for td in bad.parent.find_all("td")])
print("previous cell:", bad.find_previous_sibling("td").text)
print("table id:", bad.find_parent("table")["id"])
print("children of ul:", len(list(soup.find("ul").find_all("li", recursive=False))))

# ---------------------------------------------------------------
show(6, "Scrape a table into a list of dictionaries")
# WHAT: HTML table -> Python data.
# HOW : read headers from <th>; zip them with each row's <td> values.
# WHY : the shape from Days 13, 20 and 27: ready for CSV, JSON or Pandas.
table = soup.find("table", id="nodes")
headers = [th.text.lower() for th in table.find_all("th")]
rows = []
for tr in table.find_all("tr")[1:]:
    values = [td.text for td in tr.find_all("td")]
    row = dict(zip(headers, values))
    row["cpu"] = int(row["cpu"])
    rows.append(row)
print(rows)
print("down:", [r["node"] for r in rows if r["state"] == "down"])

# ---------------------------------------------------------------
show(7, "Clean text: get_text and whitespace")
# WHAT: extract readable text without the markup.
# HOW : get_text(" ", strip=True) joins the pieces with a separator and
#       trims whitespace.
# WHY : messy HTML has odd spacing and nested tags.
messy = BeautifulSoup("<div>  Hello\n   <b>big</b>  <i>world</i> </div>", "html.parser")
print(repr(messy.div.text))
print(repr(messy.div.get_text(" ", strip=True)))
print(repr(" ".join(messy.div.get_text().split())))

# ---------------------------------------------------------------
show(8, "Remove noise and edit the tree")
# WHAT: strip scripts and styles; change content.
# HOW : decompose() deletes a tag; assign to .string; attribute assignment
#       edits attributes.
# WHY : cleaning a page before extracting its text.
page2 = BeautifulSoup(PAGE, "html.parser")
for tag in page2(["script", "style"]):
    tag.decompose()
print("script tags left:", len(page2.find_all("script")))
page2.h1.string = "Renamed"
page2.find("a")["href"] = "/people/ana-2"
print(page2.h1, page2.find("a"))
print(page2.body.get_text(" ", strip=True)[:60], "...")

# ---------------------------------------------------------------
show(9, "Links and images: relative -> absolute, unique")
# WHAT: collect every link and image with full URLs.
# HOW : urljoin(base, href); skip tags without the attribute; use a set to
#       remove duplicates.
# WHY : crawling and link checking.
BASE = "https://docs.example.com/guide/"
links = {urljoin(BASE, a["href"]) for a in soup.find_all("a", href=True)}
images = [urljoin(BASE, img["src"]) for img in soup.find_all("img", src=True)]
print(sorted(links))
print(images)

# ---------------------------------------------------------------
show(10, "Mini program: scrape a product listing robustly")
# WHAT: extract name, price, rating and stock, coping with missing fields.
# HOW : select each card; helper functions return None instead of crashing;
#       clean the price; write JSON and CSV.
# WHY : real pages are inconsistent; defensive code survives them.
LISTING = """
<div class="grid">
 <div class="product"><h2>Pen</h2><span class="price">$1.50</span>
   <span class="stars" data-rating="4.5"></span><span class="stock in">In stock</span></div>
 <div class="product"><h2>Notebook</h2><span class="price">$4.00</span>
   <span class="stock out">Sold out</span></div>
 <div class="product"><h2>Bag</h2><span class="price">$25</span>
   <span class="stars" data-rating="3"></span></div>
 <div class="product"><span class="price">$9.99</span></div>
</div>
"""


def text_of(parent, selector):
    tag = parent.select_one(selector)
    return tag.get_text(strip=True) if tag else None


def parse_price(text):
    try:
        return float(text.replace("$", "").replace(",", ""))
    except (AttributeError, ValueError):
        return None


products, skipped = [], 0
for card in BeautifulSoup(LISTING, "html.parser").select("div.product"):
    name = text_of(card, "h2")
    if not name:
        skipped += 1
        continue
    stars = card.select_one("span.stars")
    products.append({
        "name": name,
        "price": parse_price(text_of(card, "span.price")),
        "rating": float(stars["data-rating"]) if stars else None,
        "in_stock": "in" in (card.select_one("span.stock") or {"class": []}).get("class", []),
    })
print(json.dumps(products, indent=1))
print("skipped cards without a name:", skipped)
out = io.StringIO()
writer = csv.DictWriter(out, fieldnames=products[0].keys())
writer.writeheader()
writer.writerows(products)
print(out.getvalue())
print("average price:", round(sum(p["price"] for p in products) / len(products), 2))
