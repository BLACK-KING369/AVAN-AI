import os


def open_application(app_name):

    app_name = app_name.lower().strip()

    apps = {
        "calculator": "calc",
        "calc": "calc",
        "notepad": "notepad",
        "chrome": "start chrome",
        "vscode": "code"
    }

    if app_name in apps:
        os.system(apps[app_name])
        return f"Opening {app_name} Boss."

    return f"Sorry Boss, I don't know how to open {app_name}."