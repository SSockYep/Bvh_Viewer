from multiprocessing.sharedctypes import Value
from data_structure.math import *
from data_structure.bvh_tree import Node, BvhTree


class BvhLoader:
    def __init__(self, filename):
        self.filename = filename
        skeleton, frames, frame_time, motion = self.parse(filename)
        self.skeleton = skeleton

    def parse(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            lines = list(map(str.strip, lines))
            lines = list(map(str.split, lines))
            node_stack = []
            node_list = []
            root = None
            node = None
            for line in lines:
                if line[0].upper() == "HIERARCHY":
                    pass
                elif line[0].upper() == "ROOT":
                    node = Node(name=line[1])
                    node_list.append(node)
                    root = node
                elif line[0].upper() == "JOINT":
                    node = Node(name=line[1], parent=node_stack[-1])
                    node_list.append(node)
                elif line[0] == "{":
                    node_stack.append(node)
                elif line[0] == "}":
                    node = node_stack.pop()
                    if not node.is_root():
                        node.set_parent(node_stack[-1])
                elif line[0].upper() == "OFFSET":
                    offset = Vector3(float(line[1]), float(line[2]), float(line[3]))
                    node_stack[-1].offset = offset
                elif line[0].upper() == "CHANNELS":
                    if int(line[1]) + 2 != len(line):
                        raise ValueError
                    channels = line[2 : int(line[1]) + 2]
                    node_stack[-1].channels = channels
                elif line[0].upper() == "END":
                    pass

                elif line[0].upper() == "MOTION":
                    pass
                elif line[0].upper() == "FRAMES:":
                    frames = int(line[1])
                elif line[0].upper() == "FRAME" and line[1].upper() == "TIME:":
                    frame_time = float(line[2])
                else:
                    motion = list(map(float, line))

            return (BvhTree(root, node_list), frames, frame_time, motion)

