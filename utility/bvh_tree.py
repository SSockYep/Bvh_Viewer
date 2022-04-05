import numpy as np
from data_structure.math import *

class Node:
    def __init__(self, offset=Vector3(0,0,0)):
        self.parent = None
        self.children = None
        self.offset = offset