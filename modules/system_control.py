import os
import webbrowser
import ctypes

# pyright: reportMissingImports=false
try:
    import pyautogui  # type: ignore[import-not-found]
except ImportError:
    pyautogui = None  # type: ignore[assignment]


# ==================================================
# OPEN WEBSITE
# ==================================================

def open_website(site):

    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "flipkart": "https://flipkart.com",
        "amazon": "https://amazon.in"
    }

    if site in websites:

        webbrowser.open(websites[site])

        return f"Opening {site} in browser Boss."

    return None


# ==================================================
# OPEN FOLDER
# ==================================================

def open_folder(folder):

    folders = {
        "desktop": os.path.join(
            os.path.expanduser("~"),
            "OneDrive",
            "Desktop"
        ),

        "documents": os.path.join(
            os.path.expanduser("~"),
            "Documents"
        )
    }

    if folder in folders:

        if os.path.exists(folders[folder]):

            os.startfile(folders[folder])

            return f"Opening {folder} Boss."

        return f"{folder} folder was not found Boss."

    return None


# ==================================================
# OPEN YOUTUBE APP
# ==================================================

def open_youtube_app():

    try:

        os.system("start youtube:")

        return "Opening YouTube app Boss."

    except Exception:

        return "YouTube app not found Boss."


# ==================================================
# SHUTDOWN
# ==================================================

def shutdown_pc():

    os.system("shutdown /s /t 1")

    return "Shutting down your PC Boss."


# ==================================================
# RESTART
# ==================================================

def restart_pc():

    os.system("shutdown /r /t 1")

    return "Restarting your PC Boss."


# ==================================================
# LOCK PC
# ==================================================

def lock_pc():

    try:

        ctypes.windll.user32.LockWorkStation()

        return "Locking your PC Boss."

    except Exception as e:

        return f"Could not lock the PC: {e}"


# ==================================================
# SLEEP
# ==================================================

def sleep_pc():

    os.system(
        "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
    )

    return "Putting your PC to sleep Boss."


# ==================================================
# LOG OFF
# ==================================================

def logoff_pc():

    os.system("shutdown /l")

    return "Logging off Boss."


# ==================================================
# SCREENSHOT
# ==================================================

def screenshot():

    try:

        image = pyautogui.screenshot()

        desktop = os.path.join(
            os.path.expanduser("~"),
            "OneDrive",
            "Desktop"
        )

        if not os.path.exists(desktop):

            desktop = os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            )

        os.makedirs(desktop, exist_ok=True)

        path = os.path.join(
            desktop,
            "Avan_screenshot.png"
        )

        image.save(path)

        return "Screenshot saved on Desktop Boss."

    except Exception as e:

        return f"Screenshot failed: {e}"