import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
from .utils import random_delay, press_esc
from urllib.parse import parse_qs, urlparse, unquote


def scroll_to_load_all_jobs(driver, pause_time=2, max_scrolls=20):
    """Scroll page to load all jobs."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_job_cards(driver):
    return driver.find_elements(By.CSS_SELECTOR, "li div.base-search-card")


def extract_card_info(card):
    """Extract basic info from a job card."""
    try:
        title = card.find_element(
            By.CSS_SELECTOR, "h3.base-search-card__title").text.strip()
    except:
        title = ""
    try:
        company = card.find_element(
            By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
    except:
        company = ""
    try:
        location = card.find_element(
            By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
    except:
        location = ""
    try:
        link = card.find_element(
            By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")
    except:
        link = ""
    try:
        date = card.find_element(By.CSS_SELECTOR, "time").text.strip()
    except:
        date = ""
    return title, company, location, link, date


def get_job_link(driver, link):
    wait = WebDriverWait(driver, 10)

    # Open a new tab to get the real_url
    driver.execute_script("window.open(arguments[0], '_blank');", link)
    # time.sleep(5)

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Do your scraping in the new tab
    try:
        external_link_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "dd.font-sans a.link-no-visited-state"))

        )
        external_link = external_link_element.get_attribute('href')
    except:
        external_link = ""
    real_url = ""
    if external_link != "":
        parsed_url = urlparse(external_link)
        query_params = parse_qs(parsed_url.query)
        real_url = unquote(query_params.get("url", [None])[0])
    print('External_Link -> ', real_url)

    # Close the new tab
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])

    return real_url


def get_job_description(driver, link, wait_time=2):
    """Visit job page to extract description."""
    wait = WebDriverWait(driver, 10)
    driver.get(link)
    try:
        jd_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "section.description"))
        )

        jd = jd_element.text.strip()
    except:
        jd = ""

    try:
        temp_link_element = driver.find_element(
            By.CSS_SELECTOR, "h4.top-card-layout__second-subline a.topcard__org-name-link")
        temp_link = temp_link_element.get_attribute('href')
    except:
        temp_link = ""

    external_link = ""
    if temp_link != "":
        time.sleep(wait_time)
        external_link = get_job_link(driver, temp_link)

    time.sleep(wait_time)
    driver.back()
    time.sleep(wait_time)
    return jd, external_link


def scrape_jobs(driver, limit=None, delay_range=(2, 5)):
    """Scrape all jobs from page."""
    results = []
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ESCAPE)
    scroll_to_load_all_jobs(driver)

    cards = get_job_cards(driver)
    total = len(cards)
    if limit:
        total = min(total, limit)

    i = 0
    while i < total:
        cards = get_job_cards(driver)
        if i >= len(cards):
            print(f"Waiting for job card {i+1} to load...")
            time.sleep(2)
            continue

        card = cards[i]
        title, company, location, link, date = extract_card_info(card)
        print(f"Scraping {i+1}: {title} - {company}")

        jd, external_link = get_job_description(
            driver, link, wait_time=random.uniform(*delay_range))

        press_esc(driver)

        results.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Date": date,
            "Description": jd,
            "Link": link,
            "E_Link": external_link
        })

        random_delay(delay_range)
        i += 1

    return results
