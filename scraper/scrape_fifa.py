from playwright.sync_api import sync_playwright

URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    page = browser.new_page(
        viewport={"width": 1600, "height": 900}
    )

    print("Opening FIFA website...")

    page.goto(URL, wait_until="domcontentloaded")

    # Wait for page to load
    page.wait_for_timeout(2000)

    # Accept cookies
    page.get_by_role("button", name="I'm OK with that").click()

    print("Cookies accepted!")

    page.wait_for_timeout(1500)

    # Click Attacking tab
    page.get_by_role("button", name="Attacking").click()

    print("Attacking clicked!")

    page.wait_for_timeout(3000)

    # Locate all rows
    rows = page.locator("tbody tr")

    print(f"Rows Found: {rows.count()}")

    # Get first row
    first_row = rows.nth(0)

    # Read every cell as text
    cells = first_row.locator("td").all_inner_texts()

    print("\n========== FIRST ROW ==========\n")

    for index, cell in enumerate(cells):
        print(f"Cell {index}:")
        print(repr(cell))
        print("-" * 40)

    print("\nDone!")

    # Keep browser open
    page.pause()

    browser.close()