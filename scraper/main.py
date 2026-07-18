from playwright.sync_api import sync_playwright
from constants import URL
from fifa_scraper import scrape_current_page
import pandas as pd
from fifa_scraper import scrape_category, scrape_current_page, load_all_players
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

    page.goto(URL, wait_until="domcontentloaded",timeout=60000)

    page.wait_for_timeout(2000)

    page.get_by_role(
        "button",
        name="I'm OK with that"
    ).click()

    

  

    page.wait_for_timeout(2000)

    categories = [
    
    "adidas Golden Boot",
   
]

    for category in categories:

        df = scrape_category(page, category)

        filename = category.lower().replace(" ", "_") + ".csv"

        df.to_csv(f"data/{filename}", index=False)

        print(f"Saved {filename}")