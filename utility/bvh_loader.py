from data_structure.math import *


class BvhLoader:
    def __init__(self, filename):
        self.filename = filename
        static, dynamic = self.parse(filename)

    def parse(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
