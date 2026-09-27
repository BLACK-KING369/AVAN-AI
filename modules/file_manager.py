import os
import shutil

DESKTOP = os.path.join(
    os.path.expanduser("~"),
    "OneDrive",
    "Desktop"
)


def create_folder(name):

    path = os.path.join(DESKTOP, name)

    os.makedirs(path, exist_ok=True)

    return f"Folder {name} created Boss."


def create_file(name):

    path = os.path.join(DESKTOP, name)

    with open(path, "w") as file:
        file.write("")

    return f"File {name} created Boss."


def open_desktop():

    os.startfile(DESKTOP)

    return "Opening Desktop Boss."

def delete_file(name):

    path = os.path.join(DESKTOP, name)

    if os.path.exists(path):

        os.remove(path)

        return f"File '{name}' deleted successfully Boss."

    return f"File '{name}' not found Boss."


def delete_folder(name):

    path = os.path.join(DESKTOP, name)

    if os.path.exists(path):

        shutil.rmtree(path)

        return f"Folder '{name}' deleted successfully Boss."

    return f"Folder '{name}' not found Boss."