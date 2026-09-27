import os
import subprocess


def run(command):

    text = command.lower()


    # ---------------- CLOSE APPS ----------------

    if "close" in text or "band karo" in text or "band kar do" in text:

        if "notepad" in text:

            os.system("taskkill /f /im notepad.exe")

            return "Closing Notepad Boss."


        if "chrome" in text:

            os.system("taskkill /f /im chrome.exe")

            return "Closing Chrome Boss."


        if "calculator" in text:

            os.system("taskkill /f /im CalculatorApp.exe")

            return "Closing Calculator Boss."



    # ---------------- OPEN APPS ----------------

    apps = {

        "chrome": "start chrome",
        "google chrome": "start chrome",

        "vs code": "code",
        "visual studio code": "code",

        "calculator": "calc",

        "notepad": "notepad",

        "file explorer": "explorer"

    }


    for app, action in apps.items():

        if app in text and (
            "open" in text
            or "khol" in text
            or "start" in text
        ):

            try:

                os.system(action)

                return f"Opening {app} Boss."

            except:

                return f"Sorry Boss, I couldn't open {app}."


    return None