# Track 3: Automation, BeautifulSoup and Selenium

**Examples:** `examples/t3_beautifulsoup.py`, `examples/t3_selenium.py`
**Install:** `pip install beautifulsoup4 requests selenium` (Selenium also needs Google Chrome)
**Prerequisites:** Day 13 (dicts), Day 16 (errors), Day 21 (comprehensions), Day 26 (requests)

---

## 1. The big idea

**Automation** means letting Python do repetitive work on websites:

- **BeautifulSoup**: read a page's HTML and **pull out the data** you want (web scraping).
- **Selenium**: **control a real browser**: open pages, click, type, wait, take screenshots.

```
Is the data in the HTML that requests downloads?
   YES ─► requests + BeautifulSoup   (fast, light)
   NO  ─► (page builds itself with JavaScript, or needs login/clicks)
          ─► Selenium   (slower, but works like a person)
```

Before either, **check whether the site offers an API** (Day 26). An API gives clean JSON and is always better than scraping.

## 2. Why do these exist?

Websites are made for people, not programs. Copying a table of 500 rows by hand, checking a page every morning, or filling the same form 50 times is dull and error-prone. Scrapers and browser automation do it consistently. Typical uses: collecting data from internal dashboards with no API, monitoring a page for changes, downloading reports, testing a web app.

## 3. Simple way to understand

- **HTML** is a **family tree**: `html` contains `body`, which contains `table`, which contains `tr`, which contains `td`.
- **BeautifulSoup** is a **highlighter pen with a search tool**: "find every `td` with class `bad`".
- **Selenium** is a **robot sitting at your keyboard**: it moves the mouse, clicks and types in a real Chrome window. It must also **wait** for pages to finish loading, like a person would.

## 4. How it works: selectors

Both libraries find elements with the same **CSS selectors**:

| Selector | Matches |
|----------|---------|
| `h1` | every `<h1>` |
| `.note` | elements with `class="note"` |
| `#title` | the element with `id="title"` |
| `table#nodes td.bad` | `td` with class `bad` inside the table with id `nodes` |
| `ul.links li a` | links inside list items in `ul.links` |

Tip: in Chrome, right-click an element → **Inspect** to see its tag, class and id, then right-click it in the inspector → **Copy → Copy selector**.

---

## Part 1: BeautifulSoup (`t3_beautifulsoup.py`)

### Code walkthrough

| Block | Code | What it does |
|-------|------|--------------|
| setup | `HTML = """..."""` | a small page as a string, so you can learn **offline** |
| 1 | `BeautifulSoup(HTML, "html.parser")` | turns the text into a searchable tree |
| 2 | `soup.h1.text`, `soup.find("p", class_="note")` | first match by tag; `class_` has an underscore because `class` is a Python keyword |
| 3 | `soup.find(id="title")`, `title["id"]` | find by id; **attributes are read like dict keys** (Day 13) |
| 4 | `find_all("a")`, loop printing `a.text` and `a["href"]` | a **list** of every match |
| 5 | `soup.select("ul.links li")`, `select_one(...)` | CSS selectors: the most flexible and the one to prefer |
| 6 | skip the header row `[1:]`, unpack each row into a dict | turns an HTML table into a **list of dicts**, the shape from Days 13 and 20, ready for Pandas or JSON |
| 7 | list comprehension filtering `state == "down"` | the scraped data is now ordinary Python data |
| 8 | `urljoin(base, href)` | converts relative links like `/docs/install` into full URLs |
| 9 | `requests.get(...)` then parse | the real workflow: **download with requests, parse with BeautifulSoup**; wrapped in `try/except` (Day 16) |

**How the blocks connect:** parse (1) → locate (2 to 5) → extract into Python data (6) → use it (7, 8) → apply to a live page (9).

### The standard scraping recipe
```
1. requests.get(url, timeout=10)  → raise_for_status()
2. BeautifulSoup(response.text, "html.parser")
3. soup.select("css selector")    → list of elements
4. read .text / ["attribute"]     → build a list of dicts
5. save with csv or json (Days 19, 27) or load into Pandas (Track 1)
```

---

## Part 2: Selenium (`t3_selenium.py`)

> **Tested status:** I confirmed this file imports and parses correctly with Selenium 4.50, but I did **not** run it against a live browser. It uses Selenium 4's current API. Run it yourself and read any error message carefully.

### Code walkthrough

| Block | Code | What it does |
|-------|------|--------------|
| 1 | `webdriver.Chrome(options=...)`, `--headless=new` | starts Chrome; headless = no window; wrapped in a function (Day 14) |
| 2 | `driver.get(url)`, `driver.title` | opens a page |
| 3 | `find_elements(By.CSS_SELECTOR, ...)` | like `select`, but the results are **live browser elements** you can click and type into |
| 4 | `.click()` then `WebDriverWait(...).until(...)` | click, then **wait for a condition**, not a fixed time |
| 5 | loop over pages, `EC.staleness_of(q)`, `NoSuchElementException` | paginate: collect, click next, wait for the old page to disappear; stop when there is no "next" |
| 6 | `.send_keys(...)`, click submit, wait for the Logout link | fill and submit a form (the practice site accepts any login) |
| 7 | `save_screenshot(...)` | a picture of what the browser sees, great for debugging |
| `finally` | `driver.quit()` | **always** close the browser, even after errors (Day 16's `finally`) |

**Why waiting matters:** Python runs faster than a web page loads. If you look for an element before it exists, you get an error. **Explicit waits** (`WebDriverWait`) poll until the condition is true or time runs out. Avoid `time.sleep(5)`: it is either too long (slow) or too short (flaky).

### Which tool to choose

| Situation | Use |
|-----------|-----|
| Site has an API | **the API** (`requests`) |
| Static HTML page | requests + BeautifulSoup |
| Content appears only after JavaScript runs | Selenium |
| Need to click, log in, upload files | Selenium |
| Testing your own web app | Selenium |

---

## Be a good citizen

- Read the site's **terms of service** and `/robots.txt` before scraping.
- **Slow down**: add `time.sleep(1)` between requests; do not hammer servers.
- Do not scrape personal data you have no right to collect.
- Practise on sites built for it (`quotes.toscrape.com`, `books.toscrape.com`).
- **Never put real passwords in scripts.** Use environment variables.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| `find(...)` returns `None`, then `.text` | `AttributeError` | check for `None` first |
| Selector wrong after the site changes | empty results | re-inspect the page; scrapers need maintenance |
| Scraping a JavaScript-built page with `requests` | HTML is empty | use Selenium, or find the underlying API in browser DevTools → Network |
| `time.sleep` instead of waits | flaky scripts | `WebDriverWait` |
| Not calling `driver.quit()` | Chrome processes left running | use `try/finally` |
| Missing timeouts on `requests.get` | hangs | `timeout=10` |
| Forgetting that `.text` values are strings | maths fails | `int(...)` (as in Block 6) |
| Relative URLs saved as-is | broken links | `urljoin` |

## 8. Practice (in order)

1. **BS4:** change the HTML in the file to add a 4th node and confirm your code picks it up.
2. **BS4:** extract all `href`s that start with `http` into a list.
3. **BS4:** scrape `https://books.toscrape.com/` and print the title and price of the first 10 books.
4. **BS4 + Day 27:** save those 10 books to a CSV file.
5. **BS4 + Track 1:** load the CSV into Pandas and find the average price.
6. **Selenium:** open the practice site, click "Next" twice, and print each page's first author.
7. **Selenium:** run it with `headless=False` so you can watch the browser work.
8. **Mini-project:** a script that checks one page you care about and prints "changed" when its text differs from the last run (store the previous text in a file, Day 15).

## 9. Self-check

- When do you use BeautifulSoup and when Selenium?
- Why check for an API first?
- What does `soup.select("td.bad")` return?
- Why use explicit waits instead of `time.sleep`?
- Why does `driver.quit()` go in a `finally` block?
- What should you check before scraping a site?

**Next:** Track 4: AI/ML, where Python learns patterns from data.
