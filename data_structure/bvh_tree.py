import numpy as np
from data_structure.math import *
from utility.transform import Rotation
import pdb


class Node:
    def __init__(
        self,
        offset: Vector3 = Vector3(0, 0, 0),
        name: str = "",
        parent=None,
        end=Vector3(),
    ):
        self.children = []
        self.offset = offset
        if parent:
            self.parent = parent
            self.parent.add_child(self)
        else:
            self.parent = None
        self._name = name
        self.channels = []
        self._is_leaf = False
        if end != Vector3():
            self._is_leaf = True
        self.end = end

    def __hash__(self):
        hash_val = hash(self._name)
        hash_val += (
            2 * hash(self.offset.x) + 3 * hash(self.offset.y) + 4 * hash(self.offset.z)
        )
        hash_val += 5 * hash(len(self.channels))
        for channel in self.channels:
            hash_val += hash(channel)
        return hash_val

    def __repr__(self):
        return self._name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def delete_child(self, name):
        for child in self.children:
            if child.get_name() == name:
                self.children.remove(child)

    def set_parent(self, parent_node):
        if not self.is_root():
            self.parent.delete_child(self.get_name())
        self.parent = parent_node
        parent_node.add_child(self)

    def get_hier(self):
        children_names = self._depth_first_trav()
        return_string = ""
        for child_name in children_names:
            return_string += child_name + "\n"
        return return_string

    def is_root(self):
        return self.parent == None

    def is_leaf(self):
        return self._is_leaf

    def _depth_first_trav(self):
        ret = []
        for child in self.children:
            ret += child._depth_first_trav()
        for i in range(len(ret)):
            ret[i] = "  " + ret[i]
        ret = [self.get_name()] + ret
        return ret


class BvhTree:
    def __init__(self, root: Node, node_list: list = None):
        if not root.is_root():
            raise ValueError
        self.root = root
        if not node_list:
            node_list = []
            stack = [root]
            while len(stack) > 0:
                n = stack.pop()
                node_list.append(n)
                for c in n.children:
                    stack.append(c)
        self._node_list = node_list
        self._name_dict = {}
        self._node_dict = {}
        for i in range(len(node_list)):
            self._name_dict[node_list[i].get_name()] = i
            self._node_dict[node_list[i]] = i

    def get_node_by_index(self, index):
        return self._node_list[index]

    def get_node_by_name(self, name):
        return self._node_list[self._name_dict[name]]

    def get_index_of_node(self, node):
        return self._node_dict[node]

    def print_hier(self):
        print(self.root.get_hier())

    def num_nodes(self):
        print(self._node_list)
        return len(self._node_list)

