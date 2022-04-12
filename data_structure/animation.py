import copy
import numpy as np

from utility.transform import Transform, Translation

from .math import *
from data_structure.bvh_tree import *


class Pose:
    class _ChannelParser:
        def __init__(self, channels, values):
            self.channels = channels
            self.values = values

        def parse(self):
            pos = Vector3()
            rot_seq = ""
            rot_angles = []
            is_root = False
            for i in range(len(self.channels)):
                if self.channels[i].upper() == "XPOSITION":
                    pos.x = self.values[i]
                    is_root = True
                elif self.channels[i].upper() == "YPOSITION":
                    pos.y = self.values[i]
                    is_root = True
                elif self.channels[i].upper() == "ZPOSITION":
                    pos.z = self.values[i]
                    is_root = True
                elif self.channels[i].upper() == "XROTATION":
                    rot_seq += "x"
                    rot_angles.append(np.deg2rad(self.values[i]))
                elif self.channels[i].upper() == "YROTATION":
                    rot_seq += "y"
                    rot_angles.append(np.deg2rad(self.values[i]))
                elif self.channels[i].upper() == "ZROTATION":
                    rot_seq += "z"
                    rot_angles.append(np.deg2rad(self.values[i]))
            if is_root:
                root_trans = Translation.from_vector(pos)
            else:
                root_trans = None
            rot = Rotation.from_euler(rot_seq, rot_angles)
            return rot, root_trans

    def __init__(self, tree: BvhTree, frame_data: list):
        if len(frame_data) != tree.num_nodes() * 3 + 3:
            raise ValueError
        # load index -> get translation and rotaition of frame data

        self.frame_data = copy.copy(frame_data)
        # get root data
        data_index = 0
        self.rotations = [None for _ in range(tree.num_nodes())]
        if tree.get_node_by_index(0) != tree.root:
            raise ValueError
        for i in range(tree.num_nodes()):
            node = tree.get_node_by_index(i)
            channels = node.channels
            values = frame_data[data_index : data_index + len(channels)]
            data_index += len(channels)
            parser = self._ChannelParser(channels, values)
            rotation, root_trans = parser.parse()
            self.rotations[i] = rotation
            if root_trans:
                self.root_translation = root_trans


class Animation:
    def __init__(self, tree, frame, frame_time, motion):
        self.frame = frame
        self.frame_time = frame_time
        self.skeleton = tree
        self.poses = []
        for v in motion:
            self.poses.append(Pose(tree, v))

    def get_pose(self, frame):
        return self.poses[frame]
