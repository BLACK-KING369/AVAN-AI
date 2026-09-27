import json
import os

MEMORY_FILE = "memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except Exception as e:
        print(f"❌ Memory Load Error: {e}")
        return {}


def save_memory(data):

    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:
        print(f"❌ Memory Save Error: {e}")
        return False


def normalize_key(key):

    return " ".join(
        key.lower().strip().split()
    )


def remember(key, value):

    memory = load_memory()

    key = normalize_key(key)

    memory[key] = value

    if save_memory(memory):
        print(f"🧠 MEMORY SAVED: {key} = {value}")
        return True

    return False


def recall(key):

    memory = load_memory()

    key = normalize_key(key)

    value = memory.get(key)

    if value is not None:
        print(f"🧠 MEMORY FOUND: {key} = {value}")

    return value


def forget(key):

    memory = load_memory()

    key = normalize_key(key)

    if key in memory:

        del memory[key]

        if save_memory(memory):
            print(f"🗑️ MEMORY DELETED: {key}")
            return True

    return False


def all_memory():

    return load_memory()


def clear_memory():

    return save_memory({})