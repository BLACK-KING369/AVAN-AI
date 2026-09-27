import os
import ctypes
import subprocess
import pyautogui
import time
import psutil
import platform 
from datetime import datetime


def run(command):

    text = command.lower().strip()

    # ==============================
    # CURRENT DATE
    # ==============================

    if (
    "date" in text
    or "today" in text
    or "aaj ki date" in text
    or "aaj kya date" in text
    or "current date" in text
    or "what is the date" in text
    or "what's the date" in text
  ):
        now = datetime.now()
        return f"Aaj {now.strftime('%d %B %Y')} hai, Sir."


# ==============================
# CURRENT TIME
# ==============================

    if (
    "time kya hai" in text
    or "abhi time" in text
    or "kitne baje" in text
    or "current time" in text
    or "what time is it" in text
    or "what's the time" in text
):
        now = datetime.now()
        return f"Abhi {now.strftime('%I:%M %p')} ho rahe hain, Sir."
    # ==================================================
    # SCREENSHOT
    # ==================================================

    if "screenshot" in text or "screen shot" in text:

        desktop = os.path.join(
            os.path.expanduser("~"),
            "OneDrive",
            "Desktop"
        )

        # Fallback if OneDrive Desktop doesn't exist
        if not os.path.exists(desktop):
            desktop = os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            )

        os.makedirs(desktop, exist_ok=True)

        filename = time.strftime("Avan_screenshot_%Y%m%d_%H%M%S.png")

        path = os.path.join(desktop, filename)

        image = pyautogui.screenshot()
        image.save(path)

        return f"Screenshot saved on Desktop Sir."


    # ==================================================
    # SHOW DESKTOP
    # ==================================================

    if (
        "show desktop" in text
        or "desktop dikhao" in text
        or "desktop kholo" in text
        or "desktop dikha" in text
    ):

        pyautogui.hotkey("win", "d")

        return "Desktop shown, Sir."

    # ==================================================
    # LOCK PC
    # ==================================================

    if (
        "lock pc" in text
        or "lock computer" in text
        or "pc lock" in text
        or "computer lock" in text
        or "system lock" in text
        or "system ko lock" in text
        or "computer ko lock" in text
        or "pc ko lock" in text
    ):

        ctypes.windll.user32.LockWorkStation()

        return "PC locked, Sir."
 


    # ==================================================
    # VOLUME UP
    # ==================================================

    if (
        "volume up" in text
        or "increase volume" in text
        or "volume badhao" in text
        or "volume badao" in text
    ):

        pyautogui.press("volumeup", presses=3)

        return "Volume increased, Sir."


    # ==================================================
    # VOLUME DOWN
    # ==================================================

    if (
        "volume down" in text
        or "decrease volume" in text
        or "volume kam" in text
        or "volume ghatao" in text
    ):

        pyautogui.press("volumedown", presses=3)

        return "Volume decreased, Sir."


    # ==================================================
    # MUTE
    # ==================================================

    if (
        "mute" in text
        or "sound mute" in text
        or "awaaz band" in text
        or "awaz band" in text
    ):

        pyautogui.press("volumemute")

        return "Volume muted, Sir."


    # ==================================================
    # OPEN FILE EXPLORER
    # ==================================================

    if (
        "open file explorer" in text
        or "file explorer kholo" in text
        or "file explorer open" in text
    ):

        subprocess.Popen("explorer.exe")

        return "Opening File Explorer, Sir."


    # ==================================================
    # CLOSE FILE EXPLORER
    # ==================================================

    if (
        "close file explorer" in text
        or "file explorer band" in text
        or "file explorer close" in text
    ):

        os.system(
            'taskkill /f /im explorer.exe'
        )

        time.sleep(1)

        # Restart Windows Explorer
        subprocess.Popen("explorer.exe")

        return "File Explorer closed, Sir."


    # ==================================================
    # OPEN NOTEPAD
    # ==================================================

    if (
        "open notepad" in text
        or "notepad kholo" in text
        or "notepad open" in text
    ):

        subprocess.Popen("notepad.exe")

        return "Opening Notepad, Sir."


    # ==================================================
    # CLOSE NOTEPAD
    # ==================================================

    if (
        "close notepad" in text
        or "notepad band" in text
        or "notepad close" in text
    ):

        os.system(
            'taskkill /f /im notepad.exe'
        )

        return "Notepad closed, Sir."


    # ==================================================
    # OPEN CALCULATOR
    # ==================================================

    if (
        "open calculator" in text
        or "calculator kholo" in text
        or "calculator open" in text
    ):

        subprocess.Popen("calc.exe")

        return "Opening Calculator, Sir."


    # ==================================================
    # CLOSE CALCULATOR
    # ==================================================

    if (
        "close calculator" in text
        or "calculator band" in text
        or "calculator close" in text
    ):

        os.system(
            'taskkill /f /im CalculatorApp.exe'
        )

        return "Calculator closed, Sir."


    # ==================================================
    # OPEN CHROME
    # ==================================================

    if (
        "open chrome" in text
        or "chrome kholo" in text
        or "chrome open" in text
    ):

        subprocess.Popen(
            "cmd /c start chrome",
            shell=True
        )

        return "Opening Chrome, Sir."


    # ==================================================
    # CLOSE CHROME
    # ==================================================

    if (
        "close chrome" in text
        or "chrome band" in text
        or "chrome close" in text
    ):

        os.system(
            'taskkill /f /im chrome.exe'
        )

        return "Chrome closed, Sir."


    # ==================================================
    # OPEN VS CODE
    # ==================================================

    if (
        "open vs code" in text
        or "open visual studio code" in text
        or "vs code kholo" in text
        or "vs code open" in text
    ):

        subprocess.Popen(
            "code",
            shell=True
        )

        return "Opening VS Code, Sir."


    # ==================================================
    # CLOSE VS CODE
    # ==================================================

    if (
        "close vs code" in text
        or "vs code band" in text
        or "vs code close" in text
    ):

        os.system(
            'taskkill /f /im Code.exe'
        )

        return "VS Code closed, Sir."


    # ==================================================
    # RESTART
    # ==================================================

    if "restart" in text:

        return (
            "Restart command detected, Sir. "
            "I won't restart the PC automatically yet."
        )


    # ==================================================
    # SHUTDOWN
    # ==================================================

    if "shutdown" in text or "shut down" in text:

        return (
            "Shutdown command detected, Sir. "
            "I won't shut down the PC automatically yet."
        )


    return None