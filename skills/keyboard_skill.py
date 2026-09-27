import pyautogui


def run(command):

    text = command.lower().strip()

    # Type text
    if text.startswith("type "):
        value = command[5:].strip()

        if value:
            pyautogui.write(value, interval=0.03)
            return "Typed it Boss."

    # Press Enter
    if "press enter" in text or text == "enter":
        pyautogui.press("enter")
        return "Enter pressed Boss."

    # Press Escape
    if "press escape" in text or text == "escape":
        pyautogui.press("esc")
        return "Escape pressed Boss."

    # Copy
    if text == "copy":
        pyautogui.hotkey("ctrl", "c")
        return "Copied Boss."

    # Paste
    if text == "paste":
        pyautogui.hotkey("ctrl", "v")
        return "Pasted Boss."

    # Select all
    if "select all" in text:
        pyautogui.hotkey("ctrl", "a")
        return "Selected all Boss."

    return None