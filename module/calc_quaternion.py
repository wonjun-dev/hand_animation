"""Calculate quaternion between two vectors. """

# import bpy
import numpy as np
from mathutils import Quaternion, Vector
from math import acos


v1 = Vector([0, 0, 1])
v2 = Vector([np.sqrt(2) / 2, np.sqrt(2) / 2, 0])
# v2 = Vector([0, 1, 0])
# v2 = np.array([3.0, 3.0, 3.0])
# v2 = np.array([0.2759, 0.2759, 0.5253])
# v2 = mathutils.Vector(np.array([[np.sqrt(2) / 2], [np.sqrt(2) / 2], [0]]))


def cal_quaternion(v1, v2):
    quart_xyz = np.cross(v1, v2)
    quart_w = np.sqrt(v1.dot(v1) * v2.dot(v2)) + v1.dot(v2)
    quaterion = np.array([quart_w, quart_xyz[0], quart_xyz[1], quart_xyz[2]])
    normalized_quaternion = quaterion / np.sqrt(quaterion.dot(quaterion))
    return normalized_quaternion


def cal_quaternion2(v1, v2):

    dot_product = v1.dot(v2)
    if dot_product > 1:
        dot_product = 1.0
    cross_product = v1.cross(v2)
    angle = acos(dot_product)
    quaternion = Quaternion(cross_product, angle)

    return quaternion


if __name__ == "__main__":
    q1 = cal_quaternion(v1, v2)
    q2 = cal_quaternion2(v1, v2)
    print(q1)
    print(q2)
