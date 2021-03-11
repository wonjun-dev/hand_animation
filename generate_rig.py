"""
Load hand pose and generate rig
"""

import os
import json
import bpy
import numpy as np

os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")

json_path = "source/output/json"
json_name = "2.json"


BONE_CONNECTION = [
    [0, 1],
    [0, 5],
    [0, 9],
    [0, 13],
    [0, 17],
    [1, 2],
    [2, 3],
    [3, 4],
    [5, 6],
    [6, 7],
    [7, 8],
    [9, 10],
    [10, 11],
    [11, 12],
    [13, 14],
    [14, 15],
    [15, 16],
    [17, 18],
    [18, 19],
    [19, 20],
]


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

    pose = []
    for key, coord in coords.items():
        pose.append([coord["x"], coord["y"], coord["z"]])

    return pose


def visualize(pose):
    amt = bpy.data.armatures.new("HandJointArmature")
    rig = bpy.data.objects.new("HandJointRig", amt)

    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig

    bpy.ops.object.mode_set(mode="EDIT")

    for conn in BONE_CONNECTION:
        head_idx, tail_idx = conn[0], conn[1]
        bone = amt.edit_bones.new(f"{head_idx}_{tail_idx}")
        head_coord, tail_coord = pose[head_idx], pose[tail_idx]
        bone.head = head_coord
        bone.tail = tail_coord

    bpy.ops.object.mode_set(mode="OBJECT")


def main():
    path = os.path.join(json_path, json_name)
    coords = read_json(path)
    pose = vectorize(coords)
    visualize(pose)


if __name__ == "__main__":
    main()