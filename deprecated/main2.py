import os
import sys
import imp
import json
import bpy
import mathutils
import numpy as np


os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")
json_path = "source/output/json"
json_name = "video.json"

# 커스텀 모듈 import 하기 위한 path 추가
dir = os.path.dirname(bpy.data.filepath)
print(dir)
input()
if not dir in sys.path:
    sys.path.append(dir)
    sys.path.append("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")

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
    hand_model.armature = rig

    bpy.ops.object.mode_set(mode="OBJECT")

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
    q = calc_quaternion.cal_quaternion(prev_normal, cur_normal)
    return q


def _palm_normal(coords):

    return palm_normal.normal_vector2(coords)


def _world_to_local(world_vector, armature, bone_name="21_0"):
    """
    Convert world space vector to local space vector

    Args:
        world_vector: 3-dim Vector in world-coordinate systems.
        armature: Armature of local-coordinate system owner.

    Return:
        world_vector_armature_space_loc: Converted 3-dim Vector w.r.t armature coordinate system.
        world_vector_bone_space_loc: Converted 3-dim Vector w.r.t bone coordinate system.
    """

    bone = armature.pose.bones[bone_name]

    bone_world_matrix = armature.matrix_world @ bone.matrix

    world_vector_armature_space_loc = (
        armature.matrix_world.inverted() @ world_vector
    )  # not used for handling roll of lower arm
    world_vector_bone_space_loc = bone_world_matrix.inverted() @ world_vector

    # print(world_vector_bone_space_loc)
    world_vector_bone_space_loc.normalize()
    # print(world_vector_bone_space_loc)
    return world_vector_bone_space_loc




# def _world_to_local_quat(world_quaternion, armature, bone_name="21_0"):
#     bone = armature.pose.bones[bone_name]

#     bone_world_matrix = armature.matrix_world @ bone.matrix

#     world_quaternion_armature_space_quat = armature.matrix_world.inverted() @ world_quaternion
#     world_quaternion_bone_space_quat = bone_world_matrix.inverted() @ world_quaternion

#     world_quaternion_bone_space_quat.normalize()

#     return world_quaternion_bone_space_quat


def _world_quaternion_to_local_quaternion(world_quaternion, armature):
    angle = world_quaternion[0]  # w
    cross = mathutils.Vector([world_quaternion[1], world_quaternion[2], world_quaternion[3]])

    print("a", cross)
    cross_vector_local_space_loc = _world_to_local(cross, armature)
    origin_vector_local_space_loc = _world_to_local(cross - cross, armature)
    print("b", cross_vector_local_space_loc)
    print("c", origin_vector_local_space_loc)
    # input("sdf")

    cross_local = cross_vector_local_space_loc - origin_vector_local_space_loc

    local_quaternion = mathutils.Vector([angle, cross_local[0], cross_local[1], cross_local[2]])

    return local_quaternion


##########################################################################################


def main():
    path = os.path.join(json_path, json_name)
    frame_wise_coords = read_json(path)
    init_pose = frame_wise_coords["1"]
    hand_model = initialize(init_pose)

    bpy.ops.object.mode_set(mode="POSE")
    armt = hand_model.armature
    bones = armt.pose.bones
    lower_arm = bones["21_0"]

    normals = []
    locations = []

    for frame, coords in frame_wise_coords.items():
        frame = int(frame)
        print(frame)

        # p1, p2, p3 = coords["0"], coords["5"], coords["13"]

        # p1 = _world_to_local(
        #     world_vector=mathutils.Vector([p1["x"], p1["y"], p1["z"]]), armature=armt
        # )
        # p2 = _world_to_local(
        #     world_vector=mathutils.Vector([p2["x"], p2["y"], p2["z"]]), armature=armt
        # )
        # p3 = _world_to_local(
        #     world_vector=mathutils.Vector([p3["x"], p3["y"], p3["z"]]), armature=armt
        # )

        if frame % 1 == 0:
            palm_normal = _palm_normal(coords)
            # palm_normal = _world_to_local(palm_normal, armt)
            normals.append(_world_to_local(palm_normal, armt))
            locations.append(coords)

            print("n", normals)
            if frame == 1:
                # lower_arm.keyframe_insert("location", frame=frame)
                lower_arm.keyframe_insert("rotation_quaternion", frame=frame)
                continue

            else:
                assert len(normals) == 2
                prev_normal = normals[0]
                cur_normal = normals[1]
                # if frame == 20:
                #     prev_normal.normalize()
                #     cur_normal.normalize()
                #     print(np.linalg.norm(prev_normal))
                #     print(np.linalg.norm(cur_normal))
                #     print(prev_normal.dot(cur_normal))
                #     input()
                world_quaterion = _frame_quaternion(prev_normal, cur_normal)

                # del normals[0]  # remove prev_normal
                normals.pop()
                # print(world_quaterion)

                local_quaternion = _world_quaternion_to_local_quaternion(world_quaterion, armt)
                # print(local_quaternion)

                lower_arm.rotation_quaternion[0] = world_quaterion[0]
                # lower_arm.rotation_quaternion[1] = local_quaternion[1] * 30
                lower_arm.rotation_quaternion[2] = world_quaterion[2] * 3
                # lower_arm.rotation_quaternion[3] = local_quaternion[3] * 30
                lower_arm.keyframe_insert("rotation_quaternion", frame=int(frame))


if __name__ == "__main__":
    main()