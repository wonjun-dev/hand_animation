"""Calculate normal vector of a palm using 3x3 matrix determinant"""

import os
import json
import numpy as np

os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")

json_path = "source/output/json"
json_name = "2.json"


def read_json(path):
    with open(path, "r") as f:
        coords = json.load(f)
    return coords


def normal_vector(coords, points=[0, 5, 13]):
    """
    Return a normal vector of a plane (Ax+By+Cz+D=0).

    Args:
        points: (dict) 3 points of 3-dim coordinates.

    Return:
        nv: (list) 3-dim normal vector([A,B,C]) of a plane.
    """

    p1, p2, p3 = coords[str(points[0])], coords[str(points[1])], coords[str(points[2])]

    _A = np.array([[1.0, p1["y"], p1["z"]], [1.0, p2["y"], p2["z"]], [1.0, p3["y"], p3["z"]]])
    _B = np.array([[p1["x"], 1.0, p1["z"]], [p2["x"], 1.0, p2["z"]], [p3["x"], 1.0, p3["z"]]])
    _C = np.array([[p1["x"], p1["y"], 1.0], [p2["x"], p2["y"], 1.0], [p3["x"], p3["y"], 1.0]])

    A, B, C = _determinant(_A), _determinant(_B), _determinant(_C)
    nv = [A, B, C]

    return nv


def _determinant(array):
    det = np.linalg.det(array)
    return det


if __name__ == "__main__":
    path = os.path.join(json_path, json_name)
    coords = read_json(path)
    nv = normal_vector(coords)
    print(nv)