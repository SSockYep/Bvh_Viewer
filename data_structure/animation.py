import copy
from .math import *
from data_structure.bvh_tree import *


class Pose:
    def __init__(self, tree: BvhTree, rotation_data: list):
        self.bone = tree
        self.rotations = copy.copy(rotation_data)

    def calc_rotations(self):
        m = copy.copy(self.rotations)
        for i in range(len(tree.num_nodes())):
            pass
