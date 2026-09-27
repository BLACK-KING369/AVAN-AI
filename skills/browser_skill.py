from modules.browser import youtube_search, google_search


def run(command):

    text = command.lower().strip()

    # -------------------------
    # YOUTUBE SEARCH
    # -------------------------
    if "youtube" in text and "search" in text:

        query = text.replace("search", "")
        query = query.replace("on youtube", "")
        query = query.replace("youtube", "")
        query = query.strip()

        if query:
            return youtube_search(query)

        return "Boss, what should I search on YouTube?"

    # -------------------------
    # GOOGLE / CHROME SEARCH
    # -------------------------
    if "chrome" in text and "search" in text:

        query = text.replace("search", "")
        query = query.replace("on chrome", "")
        query = query.replace("chrome", "")
        query = query.strip()

        if query:
            return google_search(query)

        return "Boss, what should I search?"

    # -------------------------
    # GENERIC SEARCH
    # -------------------------
    if text.startswith("search "):

        query = text[7:].strip()

        if query:
            return google_search(query)

        return "Boss, what should I search?"

    return None