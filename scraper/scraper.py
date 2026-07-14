from parser import parse_player


def scrape_current_page(page):
    """
    Scrape every visible player from the current page.
    """

    # Read table headers dynamically
    headers = page.locator("thead th").all_inner_texts()

    rows = page.locator("tbody tr")

    players = []

    for i in range(rows.count()):

        row = rows.nth(i)

        cells = row.locator("td").all_inner_texts()

        player = parse_player(headers, cells)

        players.append(player)

    return players