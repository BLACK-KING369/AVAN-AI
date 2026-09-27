from modules.typer import type_text, open_and_type


def run(command):

    text = command.lower()


    if text.startswith("type "):

        return type_text(command[5:])


    if "open notepad and type" in text:

        msg = command.replace("open notepad and type", "").strip()

        return open_and_type("notepad", msg)


    return None