from modules.calculator import calculate


def run(command):
    result = calculate(command)

    if result:
        return result

    return None