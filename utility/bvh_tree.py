import numpy as np
from data_structure.math import *

class Node:
    def __init__(self, offset:Vector3=Vector3(0,0,0)):
        self.parent = None
        self.children = None
        self.offset = offset
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name