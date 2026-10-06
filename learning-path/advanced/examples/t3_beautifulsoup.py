"""Track 3a example: BeautifulSoup, extract data from HTML.

Run:    python3 learning-path/advanced/examples/t3_beautifulsoup.py
Needs:  pip install beautifulsoup4 requests
Blocks 1-8 work offline. Block 9 fetches a practice site made for scraping.
"""

from bs4 import BeautifulSoup

HTML = """
<html>
  <body>
    <h1 id="title">Cluster Status</h1>
    <p class="note">Updated <b>today</b>.</p>
    <table id="nodes">
      <tr><th>Node</th><th>CPU</th><th>State</th></tr>
      <tr><td>node-1</td><td>35</td><td class="ok">up</td></tr>
      <tr><td>node-2</td><td>91</td><td class="ok">up</td></tr>
      <tr><td>node-3</td><td>0</td><td class="bad">down</td></tr>
    </table>
    <ul class="links">
      <li><a href="/docs/install">Install</a></li>
      <li><a href="https://example.com/help">Help</a></li>
    </ul>
  </body>
</html>
"""

# BLOCK 1: parse the HTML text into a navigable tree
soup = BeautifulSoup(HTML, "html.parser")

# BLOCK 2: find one element by tag, then read its text
print(soup.h1.text)                              # Cluster Status
print(soup.find("p", class_="note").get_text())  # Updated today.

# BLOCK 3: find by id and read attributes
title = soup.find(id="title")
print(title.name, title["id"])                   # h1 title

# BLOCK 4: find_all returns a list of matches
links = soup.find_all("a")
for a in links:
    print(a.text, "->", a["href"])

# BLOCK 5: CSS selectors (the most flexible way)
print([li.text for li in soup.select("ul.links li")])
print(soup.select_one("table#nodes td.bad").text)  # first matching element

# BLOCK 6: scrape a table into a list of dicts (Day 13 shape)
rows = soup.select("#nodes tr")[1:]              # skip header row
nodes = []
for row in rows:
    node, cpu, state = [td.text for td in row.find_all("td")]
    nodes.append({"node": node, "cpu": int(cpu), "state": state})
print(nodes)

# BLOCK 7: use the data (Day 21 comprehension)
down = [n["node"] for n in nodes if n["state"] == "down"]
print("Down:", down)

# BLOCK 8: fix relative links
from urllib.parse import urljoin
base = "https://docs.example.com/"
print([urljoin(base, a["href"]) for a in links])

# BLOCK 9: LIVE: scrape a practice site (needs network)
def scrape_quotes():
    import requests
    r = requests.get("https://quotes.toscrape.com/", timeout=10)
    r.raise_for_status()
    page = BeautifulSoup(r.text, "html.parser")
    results = []
    for q in page.select("div.quote")[:3]:
        results.append({
            "text": q.select_one("span.text").text,
            "author": q.select_one("small.author").text,
        })
    return results

if __name__ == "__main__":
    try:
        for item in scrape_quotes():
            print(item["author"], ":", item["text"][:50], "...")
    except Exception as e:                         # network off, site down, etc.
        print("Live scrape skipped:", e)
