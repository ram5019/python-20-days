"""Selenium: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track3_automation/more_selenium.py
Needs:  pip install selenium      and Google Chrome installed.
        (Selenium 4.6+ downloads a matching chromedriver automatically on first use.)

NOTE ON TESTING: these examples were written against the Selenium 4 API and
checked for syntax, but NOT run against a real browser when this course was
made. If one fails, read the error: it usually names the selector or the
wait that did not match. Selectors can need small adjustments per browser.

The examples drive a small web page that this script writes to a temporary
folder and opens with a file:// address, so no website is touched.
"""

import tempfile
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

TEST_PAGE = """<!doctype html>
<html><head><title>Demo Shop</title></head>
<body style="height:2000px">
  <h1 id="title" class="big">Demo Shop</h1>
  <p class="note">Welcome. <a href="#help" id="help-link">Help</a></p>

  <label>Name <input id="name" placeholder="your name"></label>
  <button id="greet" onclick="document.getElementById('out').textContent='Hello, '+document.getElementById('name').value+'!'">Greet</button>
  <p id="out"></p>

  <select id="color"><option value="r">Red</option><option value="g">Green</option><option value="b">Blue</option></select>
  <label><input type="checkbox" id="agree"> I agree</label>

  <table id="prices">
    <tr><th>Item</th><th>Price</th></tr>
    <tr><td>Pen</td><td>1.50</td></tr>
    <tr><td>Book</td><td>12.00</td></tr>
    <tr><td>Bag</td><td>25.00</td></tr>
  </table>

  <button id="load" onclick="setTimeout(function(){
      var ul=document.getElementById('list');
      ['alpha','beta','gamma'].forEach(function(t){var li=document.createElement('li');li.textContent=t;ul.appendChild(li);});
    }, 800)">Load items</button>
  <ul id="list"></ul>

  <button id="alert-btn" onclick="alert('Are you sure?')">Delete</button>
  <div id="hidden" style="display:none">secret</div>
  <iframe id="frame" srcdoc="<p id='inner'>inside the frame</p>" width="300" height="60"></iframe>

  <form id="signup" onsubmit="document.getElementById('result').textContent='Signed up: '+this.email.value;return false;">
    <input name="email" id="email" type="email">
    <input type="submit" id="submit" value="Sign up">
  </form>
  <p id="result"></p>
</body></html>
"""


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


def make_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1200,900")
    return webdriver.Chrome(options=options)


def example_1(driver, url):
    show(1, "Open a page and read basic information")
    # WHAT: load a page.  HOW: driver.get(url); driver.title; driver.current_url.
    # WHY : the first step of every automation.
    driver.get(url)
    print("title:", driver.title)
    print("url ends with:", driver.current_url.split("/")[-1])
    print("page source length > 500:", len(driver.page_source) > 500)


def example_2(driver, url):
    show(2, "Find elements: id, CSS, XPath, link text")
    # WHAT: locate things.  HOW: find_element (one) / find_elements (a list).
    #       find_element raises NoSuchElementException if nothing matches.
    # WHY : you must find an element before you can use it.
    print(driver.find_element(By.ID, "title").text)
    print(driver.find_element(By.CSS_SELECTOR, "p.note").text)
    print(driver.find_element(By.XPATH, "//table[@id='prices']//tr[2]/td[1]").text)
    print(driver.find_element(By.LINK_TEXT, "Help").get_attribute("href").split("#")[-1])
    print(len(driver.find_elements(By.TAG_NAME, "td")), "cells")
    try:
        driver.find_element(By.ID, "does-not-exist")
    except NoSuchElementException:
        print("NoSuchElementException for a missing id")


def example_3(driver, url):
    show(3, "Read text, attributes and visibility")
    # WHAT: inspect elements.  HOW: .text, get_attribute, is_displayed, tag_name.
    # WHY : check what the user would see.
    title = driver.find_element(By.ID, "title")
    print(title.tag_name, "|", title.text, "|", title.get_attribute("class"))
    print("placeholder:", driver.find_element(By.ID, "name").get_attribute("placeholder"))
    hidden = driver.find_element(By.ID, "hidden")
    print("hidden displayed?", hidden.is_displayed(), "| .text is:", repr(hidden.text))
    print("textContent still readable:", hidden.get_attribute("textContent"))


def example_4(driver, url):
    show(4, "Type into a field and click a button")
    # WHAT: act like a user.  HOW: send_keys types; click clicks.
    # WHY : forms, search boxes, buttons.
    box = driver.find_element(By.ID, "name")
    box.clear()
    box.send_keys("Sam")
    driver.find_element(By.ID, "greet").click()
    print(driver.find_element(By.ID, "out").text)
    box.send_keys(Keys.CONTROL, "a", Keys.BACKSPACE)
    print("field cleared:", repr(box.get_attribute("value")))


def example_5(driver, url):
    show(5, "Dropdowns and checkboxes")
    # WHAT: choose options.  HOW: the Select helper wraps <select>;
    #       checkboxes are clicked and checked with is_selected().
    # WHY : most forms contain them.
    select = Select(driver.find_element(By.ID, "color"))
    select.select_by_visible_text("Green")
    print("chosen:", select.first_selected_option.text)
    select.select_by_value("b")
    print("now:", select.first_selected_option.text, "| options:", [o.text for o in select.options])
    box = driver.find_element(By.ID, "agree")
    print("before:", box.is_selected())
    box.click()
    print("after :", box.is_selected())


def example_6(driver, url):
    show(6, "Explicit waits for content that appears later")
    # WHAT: wait for dynamic content.  HOW: WebDriverWait(driver, seconds)
    #       .until(condition). It polls until true or times out.
    # WHY : pages load content after the first paint; time.sleep is either
    #       too slow or too short.
    driver.find_element(By.ID, "load").click()
    print("immediately:", len(driver.find_elements(By.CSS_SELECTOR, "#list li")), "items")
    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#list li")))
    time.sleep(0.2)
    print("after waiting:", [li.text for li in driver.find_elements(By.CSS_SELECTOR, "#list li")])
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, "never")))
    except TimeoutException:
        print("TimeoutException: the condition never became true")


def example_7(driver, url):
    show(7, "Scrape a table into data")
    # WHAT: turn a table into dicts.  HOW: loop rows; read cell text.
    # WHY : same shape as the BeautifulSoup example; Selenium is needed only
    #       when the page requires JavaScript or interaction.
    rows = driver.find_elements(By.CSS_SELECTOR, "#prices tr")[1:]
    data = []
    for row in rows:
        item, price = [c.text for c in row.find_elements(By.TAG_NAME, "td")]
        data.append({"item": item, "price": float(price)})
    print(data)
    print("total:", sum(d["price"] for d in data))


def example_8(driver, url):
    show(8, "Alerts and iframes")
    # WHAT: handle pop-ups and embedded pages.
    # HOW : switch_to.alert to accept/dismiss; switch_to.frame to enter an
    #       iframe and default_content() to leave it.
    # WHY : elements inside an iframe cannot be found until you switch.
    driver.find_element(By.ID, "alert-btn").click()
    alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
    print("alert says:", alert.text)
    alert.dismiss()
    driver.switch_to.frame(driver.find_element(By.ID, "frame"))
    print("inside frame:", driver.find_element(By.ID, "inner").text)
    driver.switch_to.default_content()
    print("back on main page:", driver.find_element(By.ID, "title").text)


def example_9(driver, url):
    show(9, "JavaScript, scrolling and screenshots")
    # WHAT: run JS in the page; scroll; capture the screen.
    # HOW : execute_script returns values; save_screenshot writes a PNG.
    # WHY : scroll to lazy-loaded content; keep evidence when something fails.
    print("JS title:", driver.execute_script("return document.title"))
    print("page height > 1500:", driver.execute_script("return document.body.scrollHeight") > 1500)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    print("scrolled:", driver.execute_script("return window.scrollY") > 0)
    shot = Path(tempfile.gettempdir()) / "selenium_demo.png"
    driver.save_screenshot(str(shot))
    print("screenshot saved:", shot.exists(), shot.name)
    driver.execute_script("arguments[0].style.border='3px solid red'", driver.find_element(By.ID, "title"))


def example_10(driver, url):
    show(10, "Mini program: fill a form, verify the result, handle failure")
    # WHAT: a complete flow with checks.  HOW: a helper wraps waiting;
    #       try/except reports problems; the caller always quits the driver.
    # WHY : reliable automation = explicit waits + clear errors + cleanup.
    def wait_for_text(locator, text, seconds=3):
        return WebDriverWait(driver, seconds).until(EC.text_to_be_present_in_element(locator, text))

    driver.get(url)
    emails = ["ana@example.com", "li@example.com"]
    for email in emails:
        field = driver.find_element(By.ID, "email")
        field.clear()
        field.send_keys(email)
        driver.find_element(By.ID, "submit").click()
        try:
            wait_for_text((By.ID, "result"), email)
            print("confirmed:", driver.find_element(By.ID, "result").text)
        except TimeoutException:
            print("FAILED to confirm", email)
            driver.save_screenshot(str(Path(tempfile.gettempdir()) / "selenium_failure.png"))


def main():
    with tempfile.TemporaryDirectory() as folder:
        page = Path(folder) / "demo.html"
        page.write_text(TEST_PAGE)
        url = page.as_uri()
        try:
            driver = make_driver()
        except Exception as error:
            print("Could not start Chrome via Selenium:", error)
            print("Install Google Chrome and a recent selenium (pip install -U selenium).")
            return
        try:
            driver.get(url)
            for example in (example_1, example_2, example_3, example_4, example_5,
                            example_6, example_7, example_8, example_9, example_10):
                try:
                    example(driver, url)
                except Exception as error:
                    print(f"  !! {example.__name__} failed: {type(error).__name__}: {str(error)[:100]}")
        finally:
            driver.quit()                  # ALWAYS close the browser


if __name__ == "__main__":
    main()
