import json
from urllib.request import Request, urlopen
from urllib.error import URLError


STATUS_URL = "http://127.0.0.1:8765/status"


def update_status(
    status=None,
    last_command=None,
    modules=None
):
    data = {}

    if status is not None:
        data["status"] = status

    if last_command is not None:
        data["last_command"] = last_command

    if modules is not None:
        data["modules"] = modules

    try:
        request = Request(
            STATUS_URL,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urlopen(request, timeout=1) as response:
            return response.status == 200

    except (URLError, TimeoutError):
        return False

    except Exception as e:
        print(f"[STATUS CLIENT] {e}")
        return False


def set_status(status):
    return update_status(
        status=status
    )


def set_command(command):
    return update_status(
        last_command=command
    )


def set_module(module, online=True):
    return update_status(
        modules={
            module.upper(): online
        }
    )