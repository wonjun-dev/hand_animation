"""
Load hand pose and generate rig
"""

import os
import json
import bpy
import numpy as np

os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/dancing_mesh")

json_path = "source/output/json"
json_name = "coords.json"


def read_json(path):
    with open(path, "r") as f:
        coords = json.load(f)
    return coords


def vectorize(coords):
    """
    Vectorize coordinate dictionary

    Args:
        coords: (json) 21 hand cooordinates

    Return:
        vector_coords: (list) A list of vectroized 21 hand coordinates
    """

    from mathutils import Vector

    for idx, coord in coords.items():
        print(idx, coord)


def main():
    path = os.path.join(json_path, json_name)
    coords = read_json(path)
    vectorize(coords)


if __name__ == "__main__":
    main()