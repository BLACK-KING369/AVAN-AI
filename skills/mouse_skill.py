import pyautogui


def run(command):

    text = command.lower()


    # Left click
    if "click karo" in text or "click" in text:

        pyautogui.click()

        return "Click done Boss."


    # Double click
    if "double click" in text:

        pyautogui.doubleClick()

        return "Double click done Boss."


    # Right click
    if "right click" in text:

        pyautogui.rightClick()

        return "Right click done Boss."


    # Move mouse left
    if "mouse left" in text:

        x, y = pyautogui.position()

        pyautogui.moveTo(x-200, y)

        return "Moving mouse left Boss."


    # Move mouse right
    if "mouse right" in text:

        x, y = pyautogui.position()

        pyautogui.moveTo(x+200, y)

        return "Moving mouse right Boss."


    return None