from playwright.sync_api import Page

def clean_row(row):
    """
    Convert a table row into a clean list of values.
    """
    return [
        value.strip()
        for value in row.inner_text().split("\n")
        if value.strip()
    ]