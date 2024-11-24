import json
import os


def load_settings(filename: str) -> dict:
    with open(filename, "r") as file:
        text = file.read()
        return json.loads(text)


def save_settings(filename: str, data: dict) -> None:
    with open(filename, "w") as file:
        text = json.dumps(data)
        file.write(text)


def check_validity(filename: str) -> bool:
    return os.path.isfile(filename)
