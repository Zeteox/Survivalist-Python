import json
from json import JSONDecodeError


def json_reader(file_path: str) -> list | dict | None:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except JSONDecodeError:
        return None
    except Exception:
        return None


def json_writer(file_path: str, data: dict) -> bool:
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
            return True
    except Exception:
        return False
