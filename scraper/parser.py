def parse_player(headers, cells):
    """
    Convert a table row into a player dictionary.
    """

    # Clean the player cell
    player_info = [
        x.strip()
        for x in cells[1].split("\n")
        if x.strip()
    ]

    player = {
        "Rank": cells[0],
        "Player": player_info[0],
        "Country": player_info[1],
        "Position": player_info[2]
    }

    # Add every statistic dynamically
    for i in range(2, len(headers)):
        player[headers[i]] = cells[i]

    return player