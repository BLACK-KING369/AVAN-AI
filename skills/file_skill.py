from modules.file_manager import (
    create_folder,
    create_file,
    open_desktop,
    delete_file,
    delete_folder
)


def run(command):

    text = command.lower()

    # Create Folder
    if "create folder" in text:

        name = command.replace("create folder", "").strip()

        return create_folder(name)


    # Create File
    if "create file" in text:

        name = command.replace("create file", "").strip()

        return create_file(name)


    # Delete Folder
    if "delete folder" in text:

        name = command.replace("delete folder", "").strip()

        return delete_folder(name)


    # Delete File
    if "delete file" in text:

        name = command.replace("delete file", "").strip()

        return delete_file(name)


    # Open Desktop
    if "open desktop" in text:

        return open_desktop()

    return None