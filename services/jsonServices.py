import json


def json_reader(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def json_writer(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

