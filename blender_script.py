import os
import json


json_path = "source/output/json"
json_name = "coords.json"


def _read_json(path):
    with open(path, "r") as f:
        coords = json.load(f)


def main():
    path = os.path.join(json_path, json_name)
    _read_json(path)


if __name__ == "__main__":
    main()