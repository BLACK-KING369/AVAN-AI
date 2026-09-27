from skills.calculator_skill import run as calculator
from skills.app_skill import run as app
from skills.browser_skill import run as browser
from skills.file_skill import run as files
from skills.typing_skill import run as typing


def execute_skill(command):

    skills = [
        files,
        browser,
        typing,
        calculator,
        app
    ]

    for skill in skills:

        result = skill(command)

        if result:
            return result

    return None

# Delete Folder
    if "delete folder" in text:

     name = command.replace("delete folder", "").strip()

    return delete_folder(name)


# Delete File
    if "delete file" in text:

     name = command.replace("delete file", "").strip()

    return delete_file(name)