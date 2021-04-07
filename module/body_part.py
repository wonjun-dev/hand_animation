import numpy as np


class Hand:
    def __init__(self, init_pose):

        self.BONE_CONNECTION = [
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

        self.init_pose = init_pose
        self.init_normal = None

        self.prev_pose = init_pose
        self.prev_normal = self.init_normal
        self.cur_pose = None
        self.cur_normal = None

        self.rig = None

    def gen_palm_vertexes(self):
        pass

    def copy_rotation(self):
        pass

    def move(self, pose):
        pass
