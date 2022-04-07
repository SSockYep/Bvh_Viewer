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
        child_node.parent = self
    
    def delete_child(self, name):
        for child in self.children:
            if child.get_name() == name:
                self.children.remove(child)

    def set_parent(self, parent_node):
        if self.parent != None:
            self.parent.delete_child(self.get_name())
        self.parent = parent_node
        parent_node.add_child(self)

    def get_heir(self):
        return_string = self.get_name()
        for child in self.children:
            return_string += '\n\t' + child.get_heir()
        return return_string


class RootNode(Node):
    def __init__(self, offset:Vector3=Vector3(0,0,0), name:str="",
                 rotation=Rotation.from_euler('xyz',0,0,0)) :
        super().__init__(offset, name)
        self.rotation = rotation

    def set_parent(self):
        raise RuntimeError