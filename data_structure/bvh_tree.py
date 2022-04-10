import numpy as np
from data_structure.math import *
from .transform import Rotation
import pdb


class Node:
    def __init__(
        self, offset: Vector3 = Vector3(0, 0, 0), name: str = "", parent=None,
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
        print(children_names)
        return_string = ""
        for child_name in children_names:
            return_string += child_name + "\n"
        print(return_string)
        return return_string

    def is_root(self):
        return self.parent == None

    def _depth_first_trav(self):
        ret = []
        for child in self.children:
            ret += child._depth_first_trav()
        for i in range(len(ret)):
            ret[i] = "  " + ret[i]
        ret = [self.get_name()] + ret
        return ret


class BvhTree:
    def __init__(self, root: Node, node_list: list):
        if not root.is_root():
            raise ValueError
        self.root = root
        self._node_list = node_list
        self._name_dict = {}
        for i in range(len(node_list)):
            self._name_dict[node_list[i].name] = i

    def get_node_by_index(self, index):
        return self._node_list[index]

    def get_node_by_name(self, name):
        return self._node_list[self._name_dict[name]]

    def print_hier(self):
        print(self.root.get_hier())
