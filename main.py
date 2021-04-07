import os
import sys
import imp
import json
import bpy
import mathutils
import numpy as np


os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")
json_path = "source/output/json"
json_name = "video_2.json"

# 커스텀 모듈 import 하기 위한 path 추가
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)


# 커스텀 모듈
from module import body_part
from module import palm_normal
from module import calc_quaternion

# 커스텀 모듈 편집후 자동 리로드
imp.reload(body_part)
imp.reload(palm_normal)
imp.reload(calc_quaternion)


def read_json(path):
    with open(path, "r") as f:
        coords = json.load(f)
    return coords


def initialize(init_pose):
    """
    Initialzie Hand rig in .blend file.
    (1. Generate rig. 2. Parenting rig. 3. Generate palm plane, 4. Copy roll constraint of palm plane and lower arm.)

    Args:
        init_pose: (dict) 3-dim 21 points of first frame.

    Return:
        hand_model: Hand instance
    """

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

    # make lower arm
    head_idx, tail_idx = 21, 0
    bone = amt.edit_bones.new(f"{head_idx}_{tail_idx}")
    tail_coord = hand_model.init_pose[str(tail_idx)]

    bone.head = [tail_coord["x"], tail_coord["y"] + 1, tail_coord["z"] + 0.1]
    bone.tail = [tail_coord["x"], tail_coord["y"], tail_coord["z"]]

    _parenting(amt)
    hand_model.rig = rig

    bpy.ops.object.mode_set(mode="OBJECT")

    print(_palm_normal(init_pose))

    return hand_model


def _parenting(amt):
    """
    Pareting all bones in hand.

    Args:
        relation: (list of tuple)
    """
    parent_relation = [
        ("3_4", "2_3", "1_2", "0_1", "21_0"),
        ("7_8", "6_7", "5_6", "0_5", "21_0"),
        ("11_12", "10_11", "9_10", "0_9", "21_0"),
        ("15_16", "14_15", "13_14", "0_13", "21_0"),
        ("19_20", "18_19", "17_18", "0_17", "21_0"),
    ]

    bpy.ops.object.mode_set(mode="EDIT")

    for finger in parent_relation:
        num_bone = len(finger)
        for i in range(num_bone - 1):
            amt.edit_bones[finger[i]].parent = amt.edit_bones[finger[i + 1]]

    bpy.ops.object.mode_set(mode="OBJECT")


def _frame_quaternion(prev_normal, cur_normal):
    """
    Calculate frame-wise quaternion of palm normal vector.
    """
    q = calc_quaternion.cal_quaternion2(prev_normal, cur_normal)
    return q


def _palm_normal(coords):
    return palm_normal.normal_vector(coords)


##########################################################################################


def main():
    path = os.path.join(json_path, json_name)
    frame_wise_coords = read_json(path)
    init_pose = frame_wise_coords["1"]
    hand_model = initialize(init_pose)

    bpy.ops.object.mode_set(mode="POSE")
    bones = hand_model.rig.pose.bones
    lower_arm = bones["21_0"]

    normals = []
    locations = []

    for frame, coords in frame_wise_coords.items():
        frame = int(frame)
        # mw = lower_arm.matrix.copy()
        # print(mw)
        # if frame == 1 or frame == 223:
        if frame % 10 == 1:
            palm_normal = _palm_normal(coords)
            # print(palm_normal)
            print(coords)
            normals.append(palm_normal)
            locations.append(coords)

            if frame == 1:
                # lower_arm.keyframe_insert("location", frame=frame)
                lower_arm.keyframe_insert("rotation_quaternion", frame=frame)
                continue

            else:
                assert len(normals) == 2
                prev_normal = normals[0]
                cur_normal = normals[1]
                quaterion = _frame_quaternion(prev_normal, cur_normal)
                print(quaterion)
                del normals[0]  # remove prev_normal
                # lower_arm.rotation_quaternion[1] = local_quaternion[1]
                lower_arm.rotation_quaternion[2] = quaterion[2]
                # lower_arm.rotation_quaternion[3] = local_quaternion[3]
                lower_arm.keyframe_insert("rotation_quaternion", frame=int(frame))

                # local_quaternion = mw.inverted() @ mathutils.Vector(quaterion)
                lower_arm.rotation_quaternion[0] = quaterion[0]
                # lower_arm.rotation_quaternion[1] = local_quaternion[1]
                lower_arm.rotation_quaternion[2] = quaterion[2]
                # lower_arm.rotation_quaternion[3] = local_quaternion[3]
                lower_arm.keyframe_insert("rotation_quaternion", frame=int(frame))


if __name__ == "__main__":
    main()