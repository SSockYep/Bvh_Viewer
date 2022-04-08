from utility.bvh_tree import Node
from .math import *
from utility.bvh_tree import *

class Pose:
    def __init__(self, root: Node):
        self.bone = root
