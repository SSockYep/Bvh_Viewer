import numpy as np
from data_structure.math import *
from .transform import Rotation
class Node:
    def __init__(self, offset:Vector3=Vector3(0,0,0), name:str=""):
        self.parent = None
        self.children = []
        self.offset = offset

        self._name = name
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_parent(self, parent_node):
        self.parent = parent_node

class RootNode(Node):
    def __init__(self, offset:Vector3=Vector3(0,0,0), name:str="",
                 rotation=Rotation.from_euler('xyz',0,0,0)) :
        super().__init__(offset, name)
        self.rotation = rotation

    def set_parent(self):
        raise RuntimeError