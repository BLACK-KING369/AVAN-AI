import time

try:
    import pyautogui  # type: ignore
except ModuleNotFoundError:
    pyautogui = None

from modules.open_app import open_application


def _ensure_pyautogui():
    if pyautogui is None:
        raise ModuleNotFoundError(
            "pyautogui is not installed. Install it with: pip install pyautogui"
        )


def type_text(text):
    _ensure_pyautogui()
    time.sleep(2)
    pyautogui.write(text, interval=0.03)
    return "Done Boss."


def open_and_type(app, text):
    _ensure_pyautogui()
    open_application(app)
    time.sleep(2)
    pyautogui.write(text, interval=0.03)
    return f"Opened {app} and typed the text Boss."