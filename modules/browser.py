try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:
    raise ImportError(
        "Playwright is not installed. Install it with: pip install playwright && playwright install chromium"
    ) from exc

# type: ignore


def youtube_search(query):

    p = sync_playwright().start()

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.youtube.com/results?search_query="
        + query.replace(" ", "+"),
        wait_until="domcontentloaded"
    )

    print(f"YouTube opened: {query}")

    # Browser ko alive rakho
    page.wait_for_timeout(1000000)

    return f"Searching YouTube for '{query}' Boss."


def google_search(query):

    p = sync_playwright().start()

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.google.com/search?q="
        + query.replace(" ", "+"),
        wait_until="domcontentloaded"
    )

    print(f"Google opened: {query}")

    # Browser ko alive rakho
    page.wait_for_timeout(1000000)

    return f"Searching Google for '{query}' Boss."