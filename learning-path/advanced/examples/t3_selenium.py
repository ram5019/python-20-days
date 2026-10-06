"""Track 3b example: Selenium, control a real browser.

Run:    python3 learning-path/advanced/examples/t3_selenium.py
Needs:  pip install selenium      and Google Chrome installed.
(Selenium 4.6+ downloads a matching chromedriver automatically the first time.)

Uses https://quotes.toscrape.com, a practice site built for learning scraping.
Use Selenium only when a page needs a real browser (JavaScript, clicking, logins).
For plain HTML pages, requests + BeautifulSoup is simpler and faster.
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# BLOCK 1: start a browser (headless = no visible window)
def make_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=options)


def main():
    driver = make_driver(headless=True)
    try:
        # BLOCK 2: open a page and read basic info
        driver.get("https://quotes.toscrape.com/")
        print("Title:", driver.title)

        # BLOCK 3: find elements (same CSS selectors as BeautifulSoup)
        quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
        print("Quotes on page 1:", len(quotes))
        first = quotes[0]
        print(first.find_element(By.CSS_SELECTOR, "span.text").text[:60])
        print("by", first.find_element(By.CSS_SELECTOR, "small.author").text)

        # BLOCK 4: click a link, then WAIT until the next page is ready
        driver.find_element(By.CSS_SELECTOR, "li.next a").click()
        WebDriverWait(driver, 10).until(EC.url_contains("/page/2"))
        print("Now on:", driver.current_url)

        # BLOCK 5: collect data across several pages
        authors = []
        for _ in range(3):
            for q in driver.find_elements(By.CSS_SELECTOR, "div.quote small.author"):
                authors.append(q.text)
            try:
                driver.find_element(By.CSS_SELECTOR, "li.next a").click()
                WebDriverWait(driver, 10).until(EC.staleness_of(q))   # old page gone
            except NoSuchElementException:
                break                                                  # last page
        print("Authors collected:", len(authors), "| unique:", len(set(authors)))

        # BLOCK 6: fill in a form and submit (login page of the practice site)
        driver.get("https://quotes.toscrape.com/login")
        driver.find_element(By.ID, "username").send_keys("demo")
        driver.find_element(By.ID, "password").send_keys("demo")       # practice site: any value works
        driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
        )
        print("Logged in to the practice site")

        # BLOCK 7: take a screenshot
        driver.save_screenshot("t3_selenium_screenshot.png")
        print("Saved t3_selenium_screenshot.png")

    except TimeoutException:
        print("Timed out waiting for the page. Selectors or network may have changed.")
    finally:
        driver.quit()                  # ALWAYS close, or Chrome processes pile up


if __name__ == "__main__":
    main()
