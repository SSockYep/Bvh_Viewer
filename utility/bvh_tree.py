import numpy as np
from data_structure.math import *

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
