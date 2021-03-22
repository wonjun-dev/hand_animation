import os
import sys
import imp
import json
import bpy
import numpy as np


os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")
json_path = "source/output/json"
json_name = "video.json"

# 커스텀 모듈 import 하기 위한 path 추가
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)


# 커스텀 모듈
from module import body_part

# 커스텀 모듈 편집후 자동 리로드
imp.reload(body_part)


def read_json(path):
    with open(path, "r") as f:
        coords = json.load(f)
    return coords


def initialzie(init_pose):
    hand_model = body_part.Hand(init_pose)
    bone_connection = hand_model.BONE_CONNECTION

    amt = bpy.data.armatures.new("HandJointArmature")
    rig = bpy.data.objects.new("HandJointRig", amt)

    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig

    bpy.ops.object.mode_set(mode="EDIT")
    for conn in bone_connection:
        head_idx, tail_idx = conn[0], conn[1]
        bone = amt.edit_bones.new(f"{head_idx}_{tail_idx}")
        head_coord, tail_coord = (
            hand_model.init_pose[str(head_idx)],
            hand_model.init_pose[str(tail_idx)],
        )
        bone.head = [head_coord["x"], head_coord["y"], head_coord["z"]]
        bone.tail = [tail_coord["x"], tail_coord["y"], tail_coord["z"]]

    bpy.ops.object.mode_set(mode="OBJECT")

    return hand_model


def _parenting():
    pass


def move_hand(coords):
    hand_model
    pass


def main():
    path = os.path.join(json_path, json_name)
    frame_wise_coords = read_json(path)
    init_pose = frame_wise_coords["1"]
    hand_model = initialzie(init_pose)

    # for frame, coords in frame_wise_coords.items():
    #     move_hand(coords)


if __name__ == "__main__":
    main()