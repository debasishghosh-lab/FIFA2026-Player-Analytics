from playwright.sync_api import TimeoutError
from parser import parse_player
import pandas as pd


def load_all_players(page):

    while True:

        current_rows = page.locator("tbody tr").count()

        print(f"Rows loaded: {current_rows}")

        try:
            page.get_by_role(
                "button",
                name="Load more"
            ).click(timeout=5000)

            page.wait_for_function(
                f"document.querySelectorAll('tbody tr').length > {current_rows}",
                timeout=20000
            )

        except TimeoutError:
            print("Finished!")
            break

        except Exception as e:
            print(e)
            break

def scrape_current_page(page):
    """
    Scrape every visible player from the current page.
    """

    headers = page.locator("thead th").all_inner_texts()

    rows = page.locator("tbody tr")

    players = []
    print("Rows found:", rows.count())

    for i in range(rows.count()):

        row = rows.nth(i)

        cells = row.locator("td").all_inner_texts()

        player = parse_player(headers, cells)

        if player is not None:
            players.append(player)

    return players



def scrape_category(page, category):
    """
    Scrape one statistics category and return a DataFrame.
    """

    print(f"\n{'=' * 60}")
    print(f"Scraping: {category}")
    print(f"{'=' * 60}")

    # Click the category
    page.get_by_role("button", name=category).click()

    # Wait for the table to refresh
    page.wait_for_selector("tbody tr", timeout=30000)
    page.wait_for_timeout(2000)

    # Load all rows
    load_all_players(page)

    # Parse all rows
    players = scrape_current_page(page)

    df = pd.DataFrame(players)

    print(f"Collected {len(df)} players.")

    return df