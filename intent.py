def detect_intent(text):

    text = text.lower().strip()

    # =================================================
    # MEMORY
    # =================================================

    memory_patterns = [
        "remember ",
        "remember this",
        "yaad rakho",
        "yaad rakhna",
        "yaad kar lo",
        "don't forget",
        "mat bhoolna",
        "bhoolna mat",

        # Name / personal information
        "my name is ",
        "mera naam ",
        "my name ",
        "i am ",
        "i'm ",
        "mai ",
        "main ",
    ]

    if any(pattern in text for pattern in memory_patterns):
        return "memory"

    # =================================================
    # SYSTEM
    # =================================================

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
        "volume badhao",
        "volume badhao karo",
        "volume kam karo",
        "mute",
        "avaj band karo",
        "restart",
        "shutdown",
    ]

    if any(word in text for word in system_words):
        return "system"

    # =================================================
    # APP
    # =================================================

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

    # =================================================
    # BROWSER
    # =================================================

    browser_words = [
        "search",
        "google",
        "search for",
        "search karo",
        "google par",
        "google me",
        "chrome me search",
        "youtube search",
        "youtube par search",
        "youtube me search",
    ]

    if any(word in text for word in browser_words):
        return "browser"

    # =================================================
    # CAMERA
    # =================================================

    camera_words = [
        "open camera",
        "camera kholo",
        "camera open",
        "take photo",
        "photo lo",
        "camera band",
        "close camera",
    ]

    if any(word in text for word in camera_words):
        return "camera"

    # =================================================
    # VISION
    # =================================================

    vision_words = [
        "what do you see",
        "tum kya dekh rahe ho",
        "kya dekh rahe ho",
        "look at this",
        "analyze image",
        "image analyze",
        "photo analyze",
        "screen dekho",
    ]

    if any(word in text for word in vision_words):
        return "vision"

    # =================================================
    # MOUSE
    # =================================================

    mouse_words = [
        "move mouse",
        "mouse move",
        "click mouse",
        "left click",
        "right click",
        "double click",
        "mouse click",
    ]

    if any(word in text for word in mouse_words):
        return "mouse"

    # =================================================
    # KEYBOARD
    # =================================================

    keyboard_words = [
        "type ",
        "type this",
        "write this",
        "press key",
        "press enter",
        "press escape",
        "press tab",
        "press space",
        "keyboard",
    ]

    if any(word in text for word in keyboard_words):
        return "keyboard"

    # =================================================
    # CONTROL
    # =================================================

    control_words = [
        "control computer",
        "control pc",
        "computer control",
        "pc control",
        "click on",
        "open file",
        "close window",
        "minimize window",
        "maximize window",
    ]

    if any(word in text for word in control_words):
        return "control"

    # =================================================
    # INFORMATION
    # =================================================

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
        "batao",
        "meaning",
        "matlab",
        "explain",
    ]

    if any(word in text for word in information_words):
        return "information"

    return "conversation"