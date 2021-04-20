import os
import sys
import imp
import json
import bpy
import mathutils
import numpy as np


def read_json(path):
    with open(path, "r") as f:
        coords = json.load(f)
    return coords


def calc_normal_vector(coords, points=[0, 5, 13]):
    """
    Return a normal vector of a plane (Ax+By+Cz+D=0).

    Args:
        points: (dict) 3 points of 3-dim coordinates.

    Return:
        nv: (np.array) 3-dim normal vector([A,B,C]) of a plane.
    """

    def _determinant(array):
        det = np.linalg.det(array)
        return det

    p1, p2, p3 = coords[str(points[0])], coords[str(points[1])], coords[str(points[2])]

    _A = np.array([[1.0, p1["y"], p1["z"]], [1.0, p2["y"], p2["z"]], [1.0, p3["y"], p3["z"]]])
    _B = np.array([[p1["x"], 1.0, p1["z"]], [p2["x"], 1.0, p2["z"]], [p3["x"], 1.0, p3["z"]]])
    _C = np.array([[p1["x"], p1["y"], 1.0], [p2["x"], p2["y"], 1.0], [p3["x"], p3["y"], 1.0]])

    A, B, C = _determinant(_A), _determinant(_B), _determinant(_C)
    nv = np.array([A, B, C])
    norm = np.linalg.norm(nv)
    nv = mathutils.Vector(nv / norm)

    return nv


def calc_quaternion(v1, v2):
    quart_xyz = np.cross(v1, v2)
    quart_w = np.sqrt(v1.dot(v1) * v2.dot(v2)) + v1.dot(v2)
    quaterion = np.array([quart_w, quart_xyz[0], quart_xyz[1], quart_xyz[2]])
    normalized_quaternion = quaterion / np.sqrt(quaterion.dot(quaterion))
    return normalized_quaternion


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
    world_vector_bone_space_loc.normalize()

    return world_vector_bone_space_loc


def world_quaternion_to_local_quaternion(world_quaternion, armature):
    angle = world_quaternion[0]  # w
    cross = mathutils.Vector([world_quaternion[1], world_quaternion[2], world_quaternion[3]])

    cross_vector_local_space_loc = _world_to_local(cross, armature)
    origin_vector_local_space_loc = _world_to_local(cross - cross, armature)

    cross_local = cross_vector_local_space_loc - origin_vector_local_space_loc

    local_quaternion = mathutils.Vector([angle, cross_local[0], cross_local[1], cross_local[2]])

    return local_quaternion


def main(coords):
    scene = bpy.context.scene
    obj = scene.objects.get("Genesis8Male")
    rForearmTwist = obj.pose.bones["rForearmTwist"]
    lForearmTwist = obj.pose.bones["lForearmTwist"]

    bpy.ops.object.mode_set(mode="POSE")

    intp = 5

    for frame, coords in frame_wise_coords.items():
        frame = int(frame)

        if frame % intp == 1:
            if frame == 1:
                init_normal = calc_normal_vector(coords)
                continue

            else:
                cur_normal = calc_normal_vector(coords)
                world_quaternion = calc_quaternion(init_normal, cur_normal)
                lForearmTwist.rotation_quaternion[0] = world_quaternion[0]
                lForearmTwist.rotation_quaternion[2] = world_quaternion[2]
                lForearmTwist.keyframe_insert("rotation_quaternion", frame=frame)


if __name__ == "__main__":
    os.chdir("/home/wonjun/Blender/blender-2.91.2-linux64/projects/hand_animation")
    json_path = "source/output/json"
    json_name = "video.json"

    path = os.path.join(json_path, json_name)
    frame_wise_coords = read_json(path)

    main(frame_wise_coords)