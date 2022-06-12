from .bvh_tree import BvhTree


class BodyModel(BvhTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
