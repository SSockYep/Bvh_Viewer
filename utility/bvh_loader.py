from multiprocessing.sharedctypes import Value
from data_structure.animation import Animation
from data_structure.math import *
from data_structure.bvh_tree import Node, BvhTree


class BvhLoader:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        filename = self.filename
        with open(filename, "r") as f:
            lines = f.readlines()
            lines = list(map(str.strip, lines))
            lines = list(map(str.split, lines))
            node_stack = []
            node_list = []
            root = None
            node = None
            motion = []
            leaf = False
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
                    if not leaf:
                        node_stack.append(node)
                elif line[0] == "}":
                    if not leaf:
                        node = node_stack.pop()
                        if not node.is_root():
                            node.set_parent(node_stack[-1])
                    else:
                        leaf = False
                elif line[0].upper() == "OFFSET":
                    offset = Vector3(float(line[1]), float(line[2]), float(line[3]))
                    if not leaf:
                        node_stack[-1].offset = offset
                    else:
                        node.end = offset
                elif line[0].upper() == "CHANNELS":
                    if int(line[1]) + 2 != len(line):
                        raise ValueError
                    channels = line[2 : int(line[1]) + 2]
                    node_stack[-1].channels = channels
                elif line[0].upper() == "END":
                    node._is_leaf = True
                    leaf = True
                elif line[0].upper() == "MOTION":
                    pass
                elif line[0].upper() == "FRAMES:":
                    frames = int(line[1])
                elif line[0].upper() == "FRAME" and line[1].upper() == "TIME:":
                    frame_time = float(line[2])
                else:
                    motion.append(list(map(float, line)))
            tree = BvhTree(root, node_list)
            animation = Animation(tree, frames, frame_time, motion)
            return animation
