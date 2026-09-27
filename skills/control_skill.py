import pyautogui
import time


def run(command):

    text = command.lower()


    # TYPE TEXT
    if "type" in text or "likho" in text:

        words = text.replace("type", "")
        words = words.replace("likho", "")

        pyautogui.write(words.strip(), interval=0.05)

        return "Typing done Boss."


    # CLICK
    if "click" in text or "click karo" in text:

        pyautogui.click()

        return "Clicked Boss."


    # DOUBLE CLICK
    if "double click" in text:

        pyautogui.doubleClick()

        return "Double click done Boss."


    # MOVE MOUSE
    if "mouse right" in text:

        pyautogui.moveRel(200,0,duration=1)

        return "Moving mouse right Boss."


    if "mouse left" in text:

        pyautogui.moveRel(-200,0,duration=1)

        return "Moving mouse left Boss."


    if "mouse up" in text:

        pyautogui.moveRel(0,-200,duration=1)

        return "Moving mouse up Boss."


    if "mouse down" in text:

        pyautogui.moveRel(0,200,duration=1)

        return "Moving mouse down Boss."


    return None