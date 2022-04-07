from utility.bvh_tree import RootNode
from .math import *
from utility.bvh_tree import *

class Pose:
    def __init__(self, root: RootNode):
        self.bone = root
