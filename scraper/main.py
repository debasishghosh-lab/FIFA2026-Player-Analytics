from playwright.sync_api import sync_playwright
from constants import URL
from scraper import scrape_current_page
import pandas as pd

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    page = browser.new_page(
        viewport={
            "width": 1600,
            "height": 900
        }
    )

    page.goto(URL, wait_until="domcontentloaded")

    page.wait_for_timeout(2000)

    page.get_by_role(
        "button",
        name="I'm OK with that"
    ).click()

    page.wait_for_timeout(2000)

    page.get_by_role(
        "button",
        name="Attacking"
    ).click()

    page.wait_for_timeout(3000)

    players = scrape_current_page(page)

df = pd.DataFrame(players)

df.to_csv(
    "data/attacking_page1.csv",
    index=False
)

print(df.head())