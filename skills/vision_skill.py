import pyautogui
import base64
from io import BytesIO
from ai.openrouter import ask_openrouter_vision


def screenshot_base64():

    image = pyautogui.screenshot()

    buffer = BytesIO()

    image.save(buffer, format="PNG")

    image_bytes = buffer.getvalue()

    encoded = base64.b64encode(image_bytes).decode()

    return f"data:image/png;base64,{encoded}"



def run(command):

    text = command.lower()


    if (
        "screen dekho" in text
        or "screen check" in text
        or "screen par kya hai" in text
        or "analyze screen" in text
    ):

        image = screenshot_base64()


        prompt = """
You are Avan AI.

Analyze the computer screenshot.

Tell Boss:
- What is visible on screen
- Which applications are open
- Any important information

Answer naturally.
"""


        return ask_openrouter_vision(prompt, image)


    return None