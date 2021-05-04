import os
import bpy
import bmesh
import numpy as np
import math
import mathutils
from mathutils import Vector
from random import *
import cv2
import json
from collections import OrderedDict


def Armature_generation():
    f = open(Global_path + "1.txt", "r")
    x = []
    y = []
    z = []
    # bpy.ops.object.mode_set(mode='OBJECT')
    ind = 0
    while True:
        line = f.readline()

        if not line:
            break

        split = line.split()
        x.append(float(split[1]))
        y.append(float(split[2]))
        z.append(float(split[3]))
        ind = ind + 1
    f.close()

    p_x = -x[10]
    p_y = -y[10]

    for i in range(0, ind):
        x[i] = x[i] + p_x
        y[i] = y[i] + p_y

    bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))

    Rig_forward(1, 0, x, y, z, 0)
    for i in range(1, 4):
        Rig_forward(i, i + 1, x, y, z, i)

    Rig_forward(1, 5, x, y, z, 4)
    for i in range(5, 7):
        Rig_forward(i, i + 1, x, y, z, i)

    Rig_forward(18, 1, x, y, z, 7)
    Rig_forward(18, 8, x, y, z, 8)
    Rig_forward(8, 9, x, y, z, 9)
    Rig_forward(9, 10, x, y, z, 10)
    Rig_forward(18, 11, x, y, z, 11)
    Rig_forward(11, 12, x, y, z, 12)
    Rig_forward(12, 13, x, y, z, 13)

    bones_parent_child("bone7", "bone1")
    bones_parent_child("bone7", "bone4")
    bones_parent_child("bone7", "bone8")
    bones_parent_child("bone7", "bone11")
    bones_parent_child("bone8", "bone9")
    bones_parent_child("bone11", "bone12")

    bones_parent_child("bone2", "bone3")
    bones_parent_child("bone1", "bone2")
    bones_parent_child("bone5", "bone6")
    bones_parent_child("bone4", "bone5")
    bones_parent_child("bone7", "bone1")
    bones_parent_child("bone7", "bone4")
    bones_parent_child("bone7", "bone0")

    bones_parent_child("bone8", "bone9")
    bones_parent_child("bone9", "bone10")
    bones_parent_child("bone11", "bone12")
    bones_parent_child("bone12", "bone13")


def pose_apply(frame_num):

    f = open(Global_path + "1.txt", "r")
    x = []
    y = []
    z = []

    ind = 0
    while True:
        line = f.readline()

        if not line:
            break

        split = line.split()
        x.append(float(split[1]))
        y.append(float(split[2]))
        z.append(float(split[3]))
        ind = ind + 1
    f.close()

    p_x = 0
    p_y = 0

    for i in range(0, ind):
        x[i] = x[i] + p_x
        y[i] = y[i] + p_y

    pose_bone = bpy.data.objects["Armature"].pose.bones
    # init_rotation(frame_num*10 +10)

    fj = open(json_path, "w")

    for i in range(0, frame_num - 2):
        file_path = Global_path + str(i + 2) + ".txt"
        f = open(file_path, "r")
        x_ani = []
        y_ani = []
        z_ani = []

        while True:
            line = f.readline()

            if not line:
                break

            split = line.split()
            x_ani.append(float(split[1]))
            y_ani.append(float(split[2]))
            z_ani.append(float(split[3]))

        f.close()

        file_path = Global_path + str(1) + ".txt"
        f = open(file_path, "r")
        x_ani_b = []
        y_ani_b = []
        z_ani_b = []

        while True:
            line = f.readline()

            if not line:
                break

            split = line.split()
            x_ani_b.append(float(split[1]))
            y_ani_b.append(float(split[2]))
            z_ani_b.append(float(split[3]))

        f.close()

        for m in range(0, ind):
            x_ani[m] = x_ani[m] + p_x
            y_ani[m] = y_ani[m] + p_y
            x_ani_b[m] = x_ani_b[m] + p_x
            y_ani_b[m] = y_ani_b[m] + p_y
        #        x_ani[18] = (x_ani[1]+(x_ani[8]+x_ani[11])/2)/2
        #        x_ani_b[18] = (x_ani_b[1]+(x_ani_b[8]+x_ani_b[11])/2)/2
        #        y_ani[18] = (y_ani[1]+(y_ani[8]+y_ani[11])/2)/2
        #        y_ani_b[18] = (y_ani_b[1]+(y_ani_b[8]+y_ani_b[11])/2)/2
        #        z_ani[18] = (z_ani[1]+(z_ani[8]+z_ani[11])/2)/2
        #        z_ani_b[18] = (z_ani_b[1]+(z_ani_b[8]+z_ani_b[11])/2)/2

        rotation_cal(pose_bone, x_ani, y_ani, z_ani, x_ani_b, y_ani_b, z_ani_b, i, fj, 2)

    fj.close()
    bpy.ops.object.mode_set(mode="OBJECT")


def rotation_cal(pose_bone, x, y, z, x_b, y_b, z_b, i, fj, freq):

    #    pbone = pose_bone['bone1']
    #    pbone.rotation_quaternion = DOF_1_quat([1,2],[18,1],x,y,z,x_b,y_b,z_b,'x',False)
    #    pbone.keyframe_insert('rotation_quaternion',frame = i*10)
    bpy.ops.object.mode_set(mode="POSE")
    str_fr = str(i * freq) + "frame" + "\n"
    fj.write(str_fr)

    pbone = pose_bone["bone0"]
    pbone.rotation_quaternion = DOF_2_quat_neck([1, 0], x, y, z, x_b, y_b, z_b)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone0"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone2"]
    pbone.rotation_quaternion = DOF_2_quat_arm_r([2, 3], [1, 2], x, y, z, x_b, y_b, z_b, False)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone2"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone3"]
    pbone.rotation_quaternion = DOF_1_quat([3, 4], [2, 3], x, y, z, x_b, y_b, z_b, "x", False)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone3"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone5"]
    pbone.rotation_quaternion = DOF_2_quat_arm([5, 6], [1, 5], x, y, z, x_b, y_b, z_b, False)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone5"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone6"]
    pbone.rotation_quaternion = DOF_1_quat([6, 7], [5, 6], x, y, z, x_b, y_b, z_b, "x", False)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone6"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone7"]
    pbone.rotation_quaternion = DOF_2_quat_body([18, 1], x, y, z, x_b, y_b, z_b)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone7"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone9"]
    pbone.rotation_quaternion = DOF_2_quat_leg([8, 9], [18, 8], x, y, z, x_b, y_b, z_b)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone9"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone10"]
    pbone.rotation_quaternion = DOF_1_quat([9, 10], [8, 9], x, y, z, x_b, y_b, z_b, "x", True)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone10"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone12"]
    pbone.rotation_quaternion = DOF_2_quat_leg([11, 12], [18, 11], x, y, z, x_b, y_b, z_b)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone12"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)

    pbone = pose_bone["bone13"]
    pbone.rotation_quaternion = DOF_1_quat([12, 13], [11, 12], x, y, z, x_b, y_b, z_b, "x", True)
    if pbone.rotation_quaternion[0] < 0.99:
        pbone.keyframe_insert("rotation_quaternion", frame=i * freq)
    str_info = (
        "bone13"
        + " "
        + str(pbone.rotation_quaternion[0])
        + " "
        + str(pbone.rotation_quaternion[1])
        + " "
        + str(pbone.rotation_quaternion[2])
        + " "
        + str(pbone.rotation_quaternion[3])
        + "\n"
    )
    fj.write(str_info)


#    pbone = pose_bone['bone3']
#    pbone.rotation_quaternion = DOF_1_quat([3,4],[2,3],x,y,z,x_b,y_b,z_b)
#    pbone.keyframe_insert('rotation_quaternion',frame = i*10)

#    pbone = pose_bone['bone3']
#    pbone.rotation_quaternion = DOF_1_quat([3,4],[2,3],x,y,z,x_b,y_b,z_b)
#    pbone.keyframe_insert('rotation_quaternion',frame = i*10)

#    pbone = pose_bone['bone3']
#    pbone.rotation_quaternion = DOF_1_quat([3,4],[2,3],x,y,z,x_b,y_b,z_b)
#    pbone.keyframe_insert('rotation_quaternion',frame = i*10)


def DOF_1_quat(b_child, b_parent, x, y, z, x_b, y_b, z_b, axis, check_mirror):
    """
    Get Two Vector
    """
    vector_child = mathutils.Vector(
        [
            x[b_child[1]] - x[b_child[0]],
            y[b_child[1]] - y[b_child[0]],
            z[b_child[1]] - z[b_child[0]],
        ]
    )
    vector_par = mathutils.Vector(
        [
            x[b_parent[1]] - x[b_parent[0]],
            y[b_parent[1]] - y[b_parent[0]],
            z[b_parent[1]] - z[b_parent[0]],
        ]
    )

    vector_child_b = mathutils.Vector(
        [
            x_b[b_child[1]] - x_b[b_child[0]],
            y_b[b_child[1]] - y_b[b_child[0]],
            z_b[b_child[1]] - z_b[b_child[0]],
        ]
    )
    vector_par_b = mathutils.Vector(
        [
            x_b[b_parent[1]] - x_b[b_parent[0]],
            y_b[b_parent[1]] - y_b[b_parent[0]],
            z_b[b_parent[1]] - z_b[b_parent[0]],
        ]
    )

    """
    rotation axis
    """
    if axis is "x":
        rot_vec = Vector([1, 0, 0])

    if axis is "y":
        rot_vec = Vector([0, 1, 0])

    if axis is "z":
        rot_vec = Vector([0, 0, 1])

    if check_mirror is True:
        rot_vec = -rot_vec

    """
    get angle difference and change to quat
    """
    angle = vector_par.angle(vector_child)
    angle2 = vector_par_b.angle(vector_child_b)
    quat_out = mathutils.Quaternion(rot_vec, -angle + angle2)
    return quat_out


def DOF_2_quat_arm(b_child, b_parent, x, y, z, x_b, y_b, z_b, prin):
    """
    up,forward
    """
    vec_up = mathutils.Vector([x[1] - x[18], y[1] - y[18], z[1] - z[18]])
    vec_up.normalize()
    vec_center = vec_up.cross(mathutils.Vector([x[2] - x[1], y[2] - y[1], z[2] - z[1]]))
    vec_center.normalize()

    vec_up_b = mathutils.Vector([x_b[1] - x_b[18], y_b[1] - y_b[18], z_b[1] - z_b[18]])
    vec_up_b.normalize()
    vec_center_b = vec_up_b.cross(
        mathutils.Vector([x_b[2] - x_b[1], y_b[2] - y_b[1], z_b[2] - z_b[1]])
    )
    vec_center_b.normalize()

    """
    Get Three Vector
    """
    vector_par = mathutils.Vector(
        [
            x[b_parent[1]] - x[b_parent[0]],
            y[b_parent[1]] - y[b_parent[0]],
            z[b_parent[1]] - z[b_parent[0]],
        ]
    )
    vector_par.normalize()
    vector_child = mathutils.Vector(
        [
            x[b_child[1]] - x[b_child[0]],
            y[b_child[1]] - y[b_child[0]],
            z[b_child[1]] - z[b_child[0]],
        ]
    )
    vector_child.normalize()

    vector_par_b = mathutils.Vector(
        [
            x_b[b_parent[1]] - x_b[b_parent[0]],
            y_b[b_parent[1]] - y_b[b_parent[0]],
            z_b[b_parent[1]] - z_b[b_parent[0]],
        ]
    )
    vector_par_b.normalize()
    vector_child_b = mathutils.Vector(
        [
            x_b[b_child[1]] - x_b[b_child[0]],
            y_b[b_child[1]] - y_b[b_child[0]],
            z_b[b_child[1]] - z_b[b_child[0]],
        ]
    )
    vector_child_b.normalize()

    """
    Project the skeleton to each axis and get angle difference and change to quat
    """

    #    angle1 = vecangle360(vector_par,vector_child)
    #    angle1_b = vecangle360(vector_par_b,vector_child_b)

    angle1 = vecangle360(vector_par, vector_child)
    angle1_b = vecangle360(vector_par_b, vector_child_b)

    if vecangle360(vector_child, vec_up) > (math.pi / 2):
        angle1 = (math.pi * 2) - angle1

    if vecangle360(vector_child_b, vec_up_b) > (math.pi / 2):
        angle1_b = (math.pi * 2) - angle1_b

    angle2 = vecangle360(vec_center, vector_child)
    angle2_b = vecangle360(vec_center_b, vector_child_b)

    """
    axis angle select
    """
    rot_vec1 = Vector([0, 0, 1])
    rot_vec2 = Vector([1, 0, 0])

    quat_r1 = mathutils.Quaternion(rot_vec1, angle1 - angle1_b)
    quat_r2 = mathutils.Quaternion(rot_vec2, angle2 - angle2_b)
    if prin is True:
        print(quat_r1)
        print(angle1 - angle1_b)
        print(angle1)
        print(angle1_b)

    quat_out = quat_r1 @ quat_r2
    return quat_out


def DOF_2_quat_arm_r(b_child, b_parent, x, y, z, x_b, y_b, z_b, prin):
    """
    up,forward
    """
    vec_up = mathutils.Vector([x[1] - x[18], y[1] - y[18], z[1] - z[18]])
    vec_up.normalize()
    vec_center = vec_up.cross(mathutils.Vector([x[2] - x[1], y[2] - y[1], z[2] - z[1]]))
    vec_center.normalize()

    vec_up_b = mathutils.Vector([x_b[1] - x_b[18], y_b[1] - y_b[18], z_b[1] - z_b[18]])
    vec_up_b.normalize()
    vec_center_b = vec_up_b.cross(
        mathutils.Vector([x_b[2] - x_b[1], y_b[2] - y_b[1], z_b[2] - z_b[1]])
    )
    vec_center_b.normalize()

    """
    Get Three Vector
    """
    vector_par = mathutils.Vector(
        [
            x[b_parent[1]] - x[b_parent[0]],
            y[b_parent[1]] - y[b_parent[0]],
            z[b_parent[1]] - z[b_parent[0]],
        ]
    )
    vector_par.normalize()
    vector_child = mathutils.Vector(
        [
            x[b_child[1]] - x[b_child[0]],
            y[b_child[1]] - y[b_child[0]],
            z[b_child[1]] - z[b_child[0]],
        ]
    )
    vector_child.normalize()

    vector_par_b = mathutils.Vector(
        [
            x_b[b_parent[1]] - x_b[b_parent[0]],
            y_b[b_parent[1]] - y_b[b_parent[0]],
            z_b[b_parent[1]] - z_b[b_parent[0]],
        ]
    )
    vector_par_b.normalize()
    vector_child_b = mathutils.Vector(
        [
            x_b[b_child[1]] - x_b[b_child[0]],
            y_b[b_child[1]] - y_b[b_child[0]],
            z_b[b_child[1]] - z_b[b_child[0]],
        ]
    )
    vector_child_b.normalize()

    """
    Project the skeleton to each axis and get angle difference and change to quat
    """

    #    angle1 = vecangle360(vector_par,vector_child)
    #    angle1_b = vecangle360(vector_par_b,vector_child_b)

    angle1 = vecangle360(vector_par, vector_child)
    angle1_b = vecangle360(vector_par_b, vector_child_b)

    if vecangle360(vector_child, vec_up) > (math.pi / 2):
        angle1 = (math.pi * 2) - angle1

    if vecangle360(vector_child_b, vec_up_b) > (math.pi / 2):
        angle1_b = (math.pi * 2) - angle1_b

    angle2 = vecangle360(vec_center, vector_child)
    angle2_b = vecangle360(vec_center_b, vector_child_b)

    """
    axis angle select
    """
    rot_vec1 = Vector([0, 0, 1])
    rot_vec2 = Vector([-1, 0, 0])

    quat_r1 = mathutils.Quaternion(rot_vec1, angle1 - angle1_b)
    quat_r2 = mathutils.Quaternion(rot_vec2, angle2 - angle2_b)
    if prin is True:
        print(quat_r1)
        print(angle1 - angle1_b)
        print(angle1)
        print(angle1_b)

    quat_out = quat_r1 @ quat_r2
    return quat_out


def DOF_2_quat_neck(bone, x, y, z, x_b, y_b, z_b):
    """
    up,forward
    """
    vec_up = mathutils.Vector([x[18] - x[1], y[18] - y[1], z[18] - z[1]])
    vec_up.normalize()
    vec_right = mathutils.Vector([x[2] - x[5], y[2] - y[5], z[2] - z[5]])
    vec_right.normalize
    vec_center = vec_up.cross(vec_right)
    vec_center.normalize()

    vec_up_b = mathutils.Vector([x_b[1] - x_b[18], y_b[1] - y_b[18], z_b[1] - z_b[18]])
    vec_up_b.normalize()
    vec_right_b = mathutils.Vector([x_b[2] - x_b[5], y_b[2] - y_b[5], z_b[2] - z_b[5]])
    vec_right_b.normalize
    vec_center_b = vec_up_b.cross(vec_right_b)
    vec_center_b.normalize()

    """
    Get Three Vector
    """
    vector_par = mathutils.Vector(
        [x[bone[1]] - x[bone[0]], y[bone[1]] - y[bone[0]], z[bone[1]] - z[bone[0]]]
    )
    vector_par.normalize()

    vector_par_b = mathutils.Vector(
        [x_b[bone[1]] - x_b[bone[0]], y_b[bone[1]] - y_b[bone[0]], z_b[bone[1]] - z_b[bone[0]]]
    )
    vector_par_b.normalize()

    """
    Project the skeleton to each axis and get angle difference and change to quat
    """

    #    angle1 = vecangle360(vector_par,vector_child)
    #    angle1_b = vecangle360(vector_par_b,vector_child_b)

    angle1 = vecangle360(vector_par, vec_right)
    angle1_b = vecangle360(vector_par_b, vec_right_b)

    angle2 = vecangle360(vec_center, vector_par)
    angle2_b = vecangle360(vec_center_b, vector_par_b)

    """
    axis angle select
    """
    rot_vec1 = Vector([1, 0, 0])
    rot_vec2 = Vector([0, 0, 1])

    quat_r1 = mathutils.Quaternion(rot_vec1, angle1 - angle1_b)
    quat_r2 = mathutils.Quaternion(rot_vec2, angle2 - angle2_b)

    quat_out = quat_r1 @ quat_r2
    return quat_out


def DOF_2_quat_body(bone, x, y, z, x_b, y_b, z_b):

    """
    Get Three Vector
    """
    vector_par = mathutils.Vector(
        [x[bone[1]] - x[bone[0]], y[bone[1]] - y[bone[0]], z[bone[1]] - z[bone[0]]]
    )
    vector_par.normalize()

    vector_par_b = mathutils.Vector(
        [x_b[bone[1]] - x_b[bone[0]], y_b[bone[1]] - y_b[bone[0]], z_b[bone[1]] - z_b[bone[0]]]
    )
    vector_par_b.normalize()

    """
    Project the skeleton to each axis and get angle difference and change to quat
    """

    angle1 = vecangle360(Vector([0, 0, 1]), vector_par)
    angle1_b = vecangle360(Vector([0, 0, 1]), vector_par_b)

    angle2 = vecangle360(Vector([1, 0, 0]), vector_par)
    angle2_b = vecangle360(Vector([1, 0, 0]), vector_par_b)

    """
    axis angle select
    """
    rot_vec1 = Vector([0, 0, 1])
    rot_vec2 = Vector([1, 0, 0])

    quat_r1 = mathutils.Quaternion(rot_vec1, angle1 - angle1_b)
    quat_r2 = mathutils.Quaternion(rot_vec2, angle2 - angle2_b)

    quat_out = quat_r1 @ quat_r2
    return quat_out


def DOF_2_quat_leg(b_child, b_parent, x, y, z, x_b, y_b, z_b):
    """
    up,forward
    """
    vec_up = mathutils.Vector([x[1] - x[18], y[1] - y[18], z[1] - z[18]])
    vec_up.normalize()
    vec_right = mathutils.Vector([x[8] - x[11], y[8] - y[11], z[8] - z[11]])
    vec_center = vec_up.cross(vec_right)
    vec_center.normalize()

    vec_up_b = mathutils.Vector([x_b[1] - x_b[18], y_b[1] - y_b[18], z_b[1] - z_b[18]])
    vec_up_b.normalize()
    vec_right_b = mathutils.Vector([x[8] - x[11], y[8] - y[11], z[8] - z[11]])
    vec_center_b = vec_up_b.cross(vec_right_b)
    vec_center_b.normalize()

    """
    Get Three Vector
    """
    vector_par = mathutils.Vector(
        [
            x[b_parent[1]] - x[b_parent[0]],
            y[b_parent[1]] - y[b_parent[0]],
            z[b_parent[1]] - z[b_parent[0]],
        ]
    )
    vector_par.normalize()
    vector_child = mathutils.Vector(
        [
            x[b_child[1]] - x[b_child[0]],
            y[b_child[1]] - y[b_child[0]],
            z[b_child[1]] - z[b_child[0]],
        ]
    )
    vector_child.normalize()

    vector_par_b = mathutils.Vector(
        [
            x_b[b_parent[1]] - x_b[b_parent[0]],
            y_b[b_parent[1]] - y_b[b_parent[0]],
            z_b[b_parent[1]] - z_b[b_parent[0]],
        ]
    )
    vector_par_b.normalize()
    vector_child_b = mathutils.Vector(
        [
            x_b[b_child[1]] - x_b[b_child[0]],
            y_b[b_child[1]] - y_b[b_child[0]],
            z_b[b_child[1]] - z_b[b_child[0]],
        ]
    )
    vector_child_b.normalize()

    """
    Project the skeleton to each axis and get angle difference and change to quat
    """

    angle1 = vecangle360(vec_center, vector_child)
    angle1_b = vecangle360(vec_center_b, vector_child_b)

    angle2 = vecangle360(vec_right, vector_child)
    angle2_b = vecangle360(vec_right_b, vector_child_b)

    """
    axis angle select
    """
    rot_vec1 = Vector([1, 0, 0])
    rot_vec2 = Vector([0, 0, -1])

    quat_r1 = mathutils.Quaternion(rot_vec1, angle1 - angle1_b)
    quat_r2 = mathutils.Quaternion(rot_vec2, angle2 - angle2_b)

    quat_out = quat_r1 @ quat_r2
    #    quat_out = quat_r1
    return quat_out


def vecangle360(ref_v, find_v):
    crossprodv = ref_v.cross(find_v)
    dotlen = ref_v.dot(find_v)
    #    x = crossprodv.length/dotlen
    #    return (math.pi/2) + math.atan(x)
    return math.atan2(crossprodv.length, dotlen)


def Rig_forward(st, lt, x, y, z, bone_ind):
    obj = bpy.data.objects["Armature"]
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects["Armature"].select_set(True)

    bpy.ops.object.mode_set(mode="EDIT")

    edit_bones = obj.data.edit_bones
    ama_name = "bone" + str(bone_ind)
    b = edit_bones.new(ama_name)
    b.tail = (x[lt], y[lt], z[lt])
    b.head = (x[st], y[st], z[st])


"""   
def Rig_forward(st,lt,x,y,z,bone_ind):
    obj = bpy.data.objects['Armature']
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action= 'DESELECT')
    bpy.data.objects['Armature'].select_set(True)
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    
    edit_bones = obj.data.edit_bones
    ama_name = (bone_ind)
    b= edit_bones.new(ama_name)
    b.tail = (x[lt],y[lt],z[lt])
    b.head = (x[st],y[st],z[st])
"""


def Rig_backward(st, lt, x, y, z, bone_ind):
    obj = bpy.data.objects["Armature"]
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects["Armature"].select_set(True)

    bpy.ops.object.mode_set(mode="EDIT")

    edit_bones = obj.data.edit_bones
    ama_name = "bone" + str(bone_ind)
    b = edit_bones.new(ama_name)
    b.tail = (x[st], y[st], z[st])
    b.head = (x[lt], y[lt], z[lt])


def bones_parent_child(parent, child):
    bpy.ops.armature.select_all(action="DESELECT")
    arm = bpy.data.objects["Armature"].data.edit_bones
    arm.active = arm[child]
    arm.active = arm[parent]
    bpy.ops.armature.parent_set(type="OFFSET")


def Armature_generation_(json_data):
    # json_data['frames'][frame number]['boides'][0]
    x = []
    y = []
    z = []

    for i in range(0, 32):
        x.append(float(json_data["frames"][0]["bodies"][0]["joint_positions"][i][0]))
        y.append(float(json_data["frames"][0]["bodies"][0]["joint_positions"][i][1]))
        z.append(float(json_data["frames"][0]["bodies"][0]["joint_positions"][i][2] - 1600))

    bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))

    Rig_forward(4, 5, x, y, z, "Clavicle_Left-Shoulder_Left")
    Rig_forward(5, 6, x, y, z, "Shoulder_Left-Elbow_Left")
    Rig_forward(6, 7, x, y, z, "Elbow_Left-Wrist_Left")
    Rig_forward(7, 8, x, y, z, "Wrist_Left-Hand_Left")

    Rig_forward(11, 12, x, y, z, "Clavicle_Right-Shoulder_Right")
    Rig_forward(12, 13, x, y, z, "Shoulder_Right-Elbow_Right")
    Rig_forward(13, 14, x, y, z, "Elbow_Right-Wrist_Right")
    Rig_forward(14, 15, x, y, z, "Wrist_Right-Hand_Right")

    Rig_forward(0, 18, x, y, z, "Pelvis-Hip_Left")
    Rig_forward(18, 19, x, y, z, "Hip_Left-Knee_Left")
    Rig_forward(19, 20, x, y, z, "Knee_Left-Ankle_Left")
    Rig_forward(20, 21, x, y, z, "Ankle_Left-Foot_Left")

    Rig_forward(0, 22, x, y, z, "Pelvis-Hip_Right")
    Rig_forward(22, 23, x, y, z, "Hip_Right-Knee_Right")
    Rig_forward(23, 24, x, y, z, "Knee_Right-Ankle_Right")
    Rig_forward(24, 25, x, y, z, "Ankle_Right-Foor_Right")

    Rig_forward(0, 1, x, y, z, "Pelvis-Spine_Naval")
    Rig_forward(1, 2, x, y, z, "Spine_Naval-Spine_Chest")
    Rig_forward(2, 3, x, y, z, "Spine_Chest-Neck")

    Rig_forward(2, 4, x, y, z, "Spine_Chest-Clavicle_Left")
    Rig_forward(2, 11, x, y, z, "Spine_Chest-Clavicle_Right")

    bones_parent_child("Pelvis-Spine_Naval", "Spine_Naval-Spine_Chest")
    bones_parent_child("Spine_Naval-Spine_Chest", "Spine_Chest-Neck")

    bones_parent_child("Spine_Naval-Spine_Chest", "Spine_Chest-Clavicle_Left")
    bones_parent_child("Spine_Naval-Spine_Chest", "Spine_Chest-Clavicle_Right")

    bones_parent_child("Spine_Chest-Clavicle_Left", "Clavicle_Left-Shoulder_Left")
    bones_parent_child("Clavicle_Left-Shoulder_Left", "Shoulder_Left-Elbow_Left")
    bones_parent_child("Shoulder_Left-Elbow_Left", "Elbow_Left-Wrist_Left")
    bones_parent_child("Elbow_Left-Wrist_Left", "Wrist_Left-Hand_Left")

    bones_parent_child("Spine_Chest-Clavicle_Right", "Clavicle_Right-Shoulder_Right")
    bones_parent_child("Clavicle_Right-Shoulder_Right", "Shoulder_Right-Elbow_Right")
    bones_parent_child("Shoulder_Right-Elbow_Right", "Elbow_Right-Wrist_Right")
    bones_parent_child("Elbow_Right-Wrist_Right", "Wrist_Right-Hand_Right")

    bones_parent_child("Pelvis-Hip_Right", "Hip_Right-Knee_Right")
    bones_parent_child("Hip_Right-Knee_Right", "Knee_Right-Ankle_Right")
    bones_parent_child("Knee_Right-Ankle_Right", "Ankle_Right-Foor_Right")

    bones_parent_child("Pelvis-Hip_Left", "Hip_Left-Knee_Left")
    bones_parent_child("Hip_Left-Knee_Left", "Knee_Left-Ankle_Left")
    bones_parent_child("Knee_Left-Ankle_Left", "Ankle_Left-Foot_Left")


def init_rotation(pose_bone, bone_ind, frame_ind):
    bone_name = bone + str(bone_ind)
    bpy.ops.object.mode_set(mode="POSE")
    pbone = pose_bone[bone_name]

    pbone.rotation_quaternion[0] = 1
    pbone.rotation_quaternion[1] = 0
    pbone.rotation_quaternion[2] = 0
    pbone.rotation_quaternion[3] = 0

    pbone.keyframe_insert("rotation_quaternion", frame=frame_ind)


def init_rot(pose_bone, json_data, bone_ind, frame_ind):
    bone_name = bone_ind
    bpy.ops.object.mode_set(mode="POSE")
    pbone = pose_bone[bone_name]

    pbone.rotation_quaternion[0] = 1
    pbone.rotation_quaternion[1] = 0
    pbone.rotation_quaternion[2] = 0
    pbone.rotation_quaternion[3] = 0

    pbone.keyframe_insert("rotation_quaternion", frame=frame_ind)


def rotation_json(json_data):

    bpy.ops.object.mode_set(mode="POSE")
    pose_bone = bpy.data.objects["Armature"].pose.bones

    frame_num = 0
    for i in json_data["frames"]:
        frame_num = frame_num + 1

    for i in range(0, frame_num):
        if i % 5 == 0:
            pbone = pose_bone["Pelvis-Spine_Naval"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][1][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][1][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][1][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][1][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Spine_Naval-Spine_Chest"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][2][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][2][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][2][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][2][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Spine_Chest-Clavicle_Left"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][4][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][4][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][4][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][4][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Spine_Chest-Clavicle_Right"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][11][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][11][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][11][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][11][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Clavicle_Left-Shoulder_Left"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][5][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][5][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][5][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][5][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Shoulder_Left-Elbow_Left"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][6][0]
            pbone.rotation_quaternion[1] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][6][2]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][6][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][6][3]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Clavicle_Right-Shoulder_Right"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][12][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][12][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][12][1]
            pbone.rotation_quaternion[3] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][12][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Shoulder_Right-Elbow_Right"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][13][0]
            pbone.rotation_quaternion[1] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][13][2]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][13][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][13][3]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Pelvis-Hip_Right"]
            pbone.rotation_quaternion[0] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][22][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][22][3]
            pbone.rotation_quaternion[2] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][22][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][22][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Hip_Right-Knee_Right"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][23][0]
            pbone.rotation_quaternion[1] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][23][3]
            pbone.rotation_quaternion[2] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][23][1]
            pbone.rotation_quaternion[3] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][23][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Pelvis-Hip_Left"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][18][0]
            pbone.rotation_quaternion[1] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][18][2]
            pbone.rotation_quaternion[2] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][18][3]
            pbone.rotation_quaternion[3] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][18][1]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)

            pbone = pose_bone["Hip_Left-Knee_Left"]
            pbone.rotation_quaternion[0] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][19][0]
            pbone.rotation_quaternion[1] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][19][3]
            pbone.rotation_quaternion[2] = -json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][19][1]
            pbone.rotation_quaternion[3] = json_data["frames"][i]["bodies"][0][
                "joint_orientations"
            ][19][2]
            pbone.keyframe_insert("rotation_quaternion", frame=i * 10)


def convert_data(json_data):
    frame_num = 0
    for i in json_data["frames"]:
        frame_num = frame_num + 1

    for i in range(1, frame_num):

        text_name = Global_path + str(i) + ".txt"
        f = open(text_name, "w")
        """
        if json_data['frames'][i]['num_bodies']>0:
            json_pos = json_data['frames'][i]['bodies'][0]['joint_positions']
        if json_data['frames'][i]['num_bodies']==0:
            json_pos = json_data['frames'][i-1]['bodies'][0]['joint_positions']
        """
        if json_data["frames"][i]["num_bodies"] > 0:
            json_pos = json_data["frames"][i]["bodies"][0]["joint_positions"]
        if json_data["frames"][i]["num_bodies"] == 0:
            json_pos = json_data["frames"][i - 1]["bodies"][0]["joint_positions"]

        if json_data["frames"][i]["num_bodies"] > 0:
            json_now = json_data["frames"][i]["bodies"][0]["joint_positions"]
        if json_data["frames"][i]["num_bodies"] == 0:
            json_now = json_data["frames"][i - 1]["bodies"][0]["joint_positions"]

        if json_data["frames"][i - 1]["num_bodies"] > 0:
            json_prev = json_data["frames"][i - 1]["bodies"][0]["joint_positions"]
        if json_data["frames"][i - 1]["num_bodies"] == 0:
            json_prev = json_data["frames"][i]["bodies"][0]["joint_positions"]

        for j in range(0, 32):
            for k in range(0, 3):
                json_pos[j][k] = (json_now[j][k] + json_prev[j][k]) / 2

        str1 = (
            str(i)
            + " "
            + str(json_pos[26][0])
            + " "
            + str(json_pos[26][1])
            + " "
            + str(json_pos[26][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[3][0])
            + " "
            + str(json_pos[3][1])
            + " "
            + str(json_pos[3][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[12][0])
            + " "
            + str(json_pos[12][1])
            + " "
            + str(json_pos[12][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[13][0])
            + " "
            + str(json_pos[13][1])
            + " "
            + str(json_pos[13][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[14][0])
            + " "
            + str(json_pos[14][1])
            + " "
            + str(json_pos[14][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[5][0])
            + " "
            + str(json_pos[5][1])
            + " "
            + str(json_pos[5][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[6][0])
            + " "
            + str(json_pos[6][1])
            + " "
            + str(json_pos[6][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[7][0])
            + " "
            + str(json_pos[7][1])
            + " "
            + str(json_pos[7][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[22][0])
            + " "
            + str(json_pos[22][1])
            + " "
            + str(json_pos[22][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[23][0])
            + " "
            + str(json_pos[23][1])
            + " "
            + str(json_pos[23][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[24][0])
            + " "
            + str(json_pos[24][1])
            + " "
            + str(json_pos[24][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[18][0])
            + " "
            + str(json_pos[18][1])
            + " "
            + str(json_pos[18][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[19][0])
            + " "
            + str(json_pos[19][1])
            + " "
            + str(json_pos[19][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[20][0])
            + " "
            + str(json_pos[20][1])
            + " "
            + str(json_pos[20][2])
            + "\n"
        )
        f.write(str1)

        str1 = (
            str(i)
            + " "
            + str(json_pos[20][0])
            + " "
            + str(json_pos[20][1])
            + " "
            + str(json_pos[20][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[20][0])
            + " "
            + str(json_pos[20][1])
            + " "
            + str(json_pos[20][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[20][0])
            + " "
            + str(json_pos[20][1])
            + " "
            + str(json_pos[20][2])
            + "\n"
        )
        f.write(str1)
        str1 = (
            str(i)
            + " "
            + str(json_pos[20][0])
            + " "
            + str(json_pos[20][1])
            + " "
            + str(json_pos[20][2])
            + "\n"
        )
        f.write(str1)

        str1 = (
            str(i)
            + " "
            + str(json_pos[1][0])
            + " "
            + str(json_pos[1][1])
            + " "
            + str(json_pos[1][2])
            + "\n"
        )
        f.write(str1)

        f.close()

    return frame_num


def apply_model(json_name, model):

    f = open(json_name, "r")

    ind = 0
    pose_bone = bpy.data.objects[model].pose.bones

    while True:
        line = f.readline()

        if ind % 11 == 0:
            frame_num = int(ind / 11) * 2

        key_frame = int(frame_num / 2)
        if frame_num % 10 == 0:
            if ind % 11 > 0:
                if ind % 11 == 1:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "neckLower"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = z[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = x[0]

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 2:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "rShldrBend"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = x[0]
                    pbone.rotation_quaternion[2] = z[0]
                    pbone.rotation_quaternion[3] = y[0]
                    """        
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = -z[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = -x[0]
                    """

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 3:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "rForearmBend"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = -z[0]

                    """
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = -z[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = -x[0]
                    """

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 4:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "lShldrBend"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = z[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = x[0]
                    """
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = -x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = -z[0]
                    """

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 5:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "lForearmBend"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = -x[0]
                    pbone.rotation_quaternion[2] = -y[0]
                    pbone.rotation_quaternion[3] = -z[0]
                    """
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = -x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = -z[0]
                    """

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 6:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "abdomenUpper"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = z[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = x[0]

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 7:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "rThighBend"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = z[0]

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 8:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "rShin"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = z[0]

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 9:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "lThighBend"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = z[0]

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

                if ind % 11 == 10:
                    w = []
                    x = []
                    y = []
                    z = []
                    bone_ind = ind % 11
                    bone_name = "lShin"
                    split = line.split()
                    w.append(float(split[1]))
                    x.append(float(split[2]))
                    y.append(float(split[3]))
                    z.append(float(split[4]))

                    pbone = pose_bone[bone_name]
                    pbone.rotation_quaternion[0] = w[0]
                    pbone.rotation_quaternion[1] = x[0]
                    pbone.rotation_quaternion[2] = y[0]
                    pbone.rotation_quaternion[3] = z[0]

                    pbone.keyframe_insert("rotation_quaternion", frame=key_frame)

        if not line:
            break

        ind = ind + 1

    f.close()


def reset_rot(obj):

    pose_bone = bpy.data.objects[obj].pose.bones

    for i in pose_bone:
        i.rotation_mode = "QUATERNION"
        i.rotation_quaternion[0] = 1
        i.rotation_quaternion[1] = 0
        i.rotation_quaternion[2] = 0
        i.rotation_quaternion[3] = 0
        i.keyframe_insert("rotation_quaternion", frame=0)


def smooth_ani(obj, frame_num):
    ob = bpy.data.objects[obj]
    pose_bone = ob.pose.bones
    """
    for i in pose_bone:
        i.rotation_quaternion.normalized()
        
        for j in range(0,frame_num):
            i.keyframe_insert('rotation_quaternion',frame = j)
    
    """

    bpy.data.SpaceGraphEditor.use_normalization()


def mouth_animation(obj, voca, data, frame_num, vari):
    ob = bpy.data.objects[obj]
    pose_bone = ob.pose.bones

    voc = data[voca]

    pbone = pose_bone["upperTeeth"]
    pbone.location[0] = float(voc["upperTeeth"][0] / 100) * vari
    pbone.location[1] = float(voc["upperTeeth"][1] / 100) * vari
    pbone.location[2] = float(voc["upperTeeth"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["lowerTeeth"]
    pbone.location[0] = float(voc["lowerTeeth"][0] / 100) * vari
    pbone.location[1] = float(voc["lowerTeeth"][1] / 100) * vari
    pbone.location[2] = float(voc["lowerTeeth"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["LipUpperMiddle"]
    pbone.location[0] = float(voc["LipUpperMiddle"][0] / 100) * vari
    pbone.location[1] = float(voc["LipUpperMiddle"][1] / 100) * vari
    pbone.location[2] = float(voc["LipUpperMiddle"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["rLipUpperOuter"]
    pbone.location[0] = float(voc["rLipUpperOuter"][0] / 100) * vari
    pbone.location[1] = float(voc["rLipUpperOuter"][1] / 100) * vari
    pbone.location[2] = float(voc["rLipUpperOuter"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["rLipLowerOuter"]
    pbone.location[0] = float(voc["rLipLowerOuter"][0] / 100) * vari
    pbone.location[1] = float(voc["rLipLowerOuter"][1] / 100) * vari
    pbone.location[2] = float(voc["rLipLowerOuter"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["rLipUpperInner"]
    pbone.location[0] = float(voc["rLipUpperInner"][0] / 100) * vari
    pbone.location[1] = float(voc["rLipUpperInner"][1] / 100) * vari
    pbone.location[2] = float(voc["rLipUpperInner"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["lLipUpperInner"]
    pbone.location[0] = float(voc["lLipUpperInner"][0] / 100) * vari
    pbone.location[1] = float(voc["lLipUpperInner"][1] / 100) * vari
    pbone.location[2] = float(voc["lLipUpperInner"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["lLipUpperOuter"]
    pbone.location[0] = float(voc["lLipUpperOuter"][0] / 100) * vari
    pbone.location[1] = float(voc["lLipUpperOuter"][1] / 100) * vari
    pbone.location[2] = float(voc["lLipUpperOuter"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["lLipLowerOuter"]
    pbone.location[0] = float(voc["lLipLowerOuter"][0] / 100) * vari
    pbone.location[1] = float(voc["lLipLowerOuter"][1] / 100) * vari
    pbone.location[2] = float(voc["lLipLowerOuter"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["rLipLowerInner"]
    pbone.location[0] = float(voc["rLipLowerInner"][0] / 100) * vari
    pbone.location[1] = float(voc["rLipLowerInner"][1] / 100) * vari
    pbone.location[2] = float(voc["rLipLowerInner"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["LipLowerMiddle"]
    pbone.location[0] = float(voc["LipLowerMiddle"][0] / 100) * vari
    pbone.location[1] = float(voc["LipLowerMiddle"][1] / 100) * vari
    pbone.location[2] = float(voc["LipLowerMiddle"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)

    pbone = pose_bone["lLipLowerInner"]
    pbone.location[0] = float(voc["lLipLowerInner"][0] / 100) * vari
    pbone.location[1] = float(voc["lLipLowerInner"][1] / 100) * vari
    pbone.location[2] = float(voc["lLipLowerInner"][2] / 100) * vari
    pbone.keyframe_insert("location", frame=frame_num)


with open("/Users/yongsung/Desktop/test_0303/out.json", "r") as f:
    json_data = json.load(f)

with open("/Users/yongsung/Desktop/test_0303/mouth_info/mouth.json", "r") as fm:
    mouth_data = json.load(fm)

# json_data['frames'][frame number]['boides'][0]


json_path = "/Users/yongsung/Desktop/test_0303/rotation_info/rot.json"
Global_path = "/Users/yongsung/Desktop/test_0303/temp/"
# Global_path ='/Users/yongsung/Desktop/test_0303/jh_data/'
fbx_path = "/Users/yongsung/Desktop/learnopencv/OpenPose/test.fbx"

frame = convert_data(json_data)
print(frame)
Armature_generation()
pose_apply(frame)
bpy.data.objects["Armature"].select_set(True)  # Blender 2.8x
bpy.ops.object.delete()

reset_rot("Genesis8Male")
apply_model(json_path, "Genesis8Male")

mouth_animation("Genesis8Male", "base", mouth_data, 0, 1)
mouth_animation("Genesis8Male", "oh", mouth_data, 10, 1)
mouth_animation("Genesis8Male", "base", mouth_data, 30, 1)
mouth_animation("Genesis8Male", "ee", mouth_data, 50, 1)
mouth_animation("Genesis8Male", "oh", mouth_data, 70, 1)
mouth_animation("Genesis8Male", "base", mouth_data, 100, 1)

mouth_animation("Genesis8Male", "oh", mouth_data, 130, 1)
mouth_animation("Genesis8Male", "ee", mouth_data, 150, 1)
mouth_animation("Genesis8Male", "ah", mouth_data, 180, 1)
mouth_animation("Genesis8Male", "ee", mouth_data, 220, 1)
mouth_animation("Genesis8Male", "base", mouth_data, 280, 1)
