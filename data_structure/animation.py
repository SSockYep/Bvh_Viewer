import copy
import numpy as np

from utility.transform import Transform, Translation

from .math import *
from data_structure.bvh_tree import *


class Pose:
    def __init__(self, tree: BvhTree, rotations: list, root_translation: Translation):
        if tree.num_nodes != len(rotations):
            assert ValueError
        self.root_translation = copy.deepcopy(rotations)
        self.rotations = Translation(root_translation.to_vector())

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

    def from_bvh_data(cls, tree: BvhTree, frame_data: list):
        if len(frame_data) != tree.num_nodes() * 3 + 3:
            raise ValueError
        # load index -> get translation and rotaition of frame data

        frame_data = copy.deepcopy(frame_data)
        # get root data
        data_index = 0
        rotations = [None for _ in range(tree.num_nodes())]
        if tree.get_node_by_index(0) != tree.root:
            raise ValueError
        for i in range(tree.num_nodes()):
            node = tree.get_node_by_index(i)
            channels = node.channels
            values = frame_data[data_index : data_index + len(channels)]
            data_index += len(channels)
            parser = cls._ChannelParser(channels, values)
            rotation, root_trans = parser.parse()
            rotations[i] = rotation
            if root_trans:
                root_translation = root_trans
        return cls(rotations, root_translation)


class Animation:
    def __init__(self, tree, frame, frametime, poses):
        self.frame = frame
        self.skeleton = tree
        self.frame_time = frametime
        self.poses = copy.deepcopy(poses)

    def from_bvh_data(cls, tree, frame, frame_time, motion):
        poses = []
        for v in motion:
            poses.append(Pose.from_bvh_data(tree, v))
        return cls(tree, frame, frame_time, motion)

    def get_pose(self, frame):
        return self.poses[frame]

    def get_joint_pos_on_frame(self, node_name, frame):
        node = self.skeleton.get_node_by_name(node_name)
        pose = self.poses[frame]
        pos = self._get_node_global_position(node, pose)
        return pos

    def get_joint_velocity(self, node_name, frame, vel_scale=0.5):
        if frame <= 0 or frame >= len(self.poses):
            raise ValueError
        node = self.skeleton.get_node_by_name(node_name)
        pose_now = self.get_pose(frame)
        pose_prev = self.get_pose(frame - 1)
        position_now = self._get_node_global_position(node, pose_now)
        position_prev = self._get_node_global_position(node, pose_prev)

        velocity = position_now + (
            (position_now - position_prev) / self.frame_time * vel_scale
        )
        return position_now, velocity

    def _get_node_global_position(self, node, pose):
        mat = Matrix4x4(np.eye(4, 4))
        idx = self.skeleton.get_index_of_node(node)
        while True:
            if node.is_root():
                mat = (
                    pose.root_translation.to_matrix()
                    # Translation(node.offset).to_matrix()
                    @ pose.rotations[idx].to_matrix()
                    @ mat
                )
                break
            mat = (
                Translation(node.offset).to_matrix()
                @ pose.rotations[idx].to_matrix()
                @ mat
            )
            node = node.parent
            idx = self.skeleton.get_index_of_node(node)
        pos = mat @ Vector3(0, 0, 0)
        return pos

