def detect_intent(text):
    text = text.lower().strip()

    # SYSTEM
    system_words = [
        "lock pc",
        "lock computer",
        "pc lock",
        "system lock",
        "band ho jao",
        "lock ho jao",
        "so jao avan",
        "show desktop", 
        "screenshot",
        "volume up", 
        "volume down", 
        "volume badhao karo",
        "volume kam karo",
        "mute",
        "avaj band karo",
        "restart", 
        "shutdown",
    ]

    if any(word in text for word in system_words):
        return "system"

    # APP
    app_words = [
        "open calculator",
        "calculator kholo",
        "open chrome",
        "chrome kholo",
        "open notepad",
        "notepad kholo",
        "open vs code",
        "vs code kholo",
        "open chatgpt",
        "chatgpt kholo",
        "open mail",
        "mail kholo",
        "open youtube",
        "youtube kholo",
        
    ]

    if any(word in text for word in app_words):
        return "app"

    # BROWSER SEARCH
    if (
        ("search" in text or "google" in text)
        and ("chrome" in text or "google" in text)
    ):
        return "browser"

    # YOUTUBE
    if "youtube" in text and "search" in text:
        return "browser"

    # MEMORY
    if (
        text.startswith("remember ")
        or "yaad rakho" in text
        or "remember this" in text
    ):
        return "memory"

    # INFORMATION
    information_words = [
        "what is",
        "who is",
        "why",
        "how",
        "when",
        "where",
        "tell me",
        "kya hai",
        "kaise",
        "kyun",
        "kab",
        "kahan",
        "batao"
    ]

    if any(word in text for word in information_words):
        return "information"

    # DEFAULT
    return "conversation"