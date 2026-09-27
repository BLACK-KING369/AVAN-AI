from skills.manager import execute_skill
from modules.file_manager import (
    create_folder,
    create_file,
    open_desktop,
    delete_file,
    delete_folder
)

def execute_command(command):
    return execute_skill(command)

