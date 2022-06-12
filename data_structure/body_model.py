from .bvh_tree import BvhTree, Node


class Joint(Node):
    def __init__(self, *args, **kwargs):
        super().init(*args, **kwargs)


class BodyModel(BvhTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
