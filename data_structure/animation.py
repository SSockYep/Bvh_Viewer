import copy
from .math import *
from data_structure.bvh_tree import *


class Pose:
    def __init__(self, tree: BvhTree, motion: list):
        self.bone = tree
        self.motion = copy.copy(motion)

    def calc_rotations(self):
        m = copy.copy(self.motion)
        bone_idx = 0
        while len(m) > 0:
            bone = self.bone.get_node_by_index(bone_idx)
            if bone.is_root():
                if len(bone.channels) != 6:
                    raise ValueError
                pos = Vector3()  # blah blah
