import pdb
import numpy as np


class Mesh:
    def __init__(self, vertices=np.array([]), triangles=np.array([])):
        self.vertices = vertices
        self.triangles = triangles

    @classmethod
    def from_obj(cls, filepath):
        assert filepath[-4:] in [".obj", ".OBJ"]
        vs = []
        fs = []
        with open(filepath, "r") as f:

            lines = f.readlines()
            for l in lines:
                line = l.split()
                if line[0] == "v":
                    vs.append(list(map(float, line[1:])))
                elif line[0] == "f":
                    idx_list = list(map(lambda x: x.split(sep="/"), line[1:]))
                    fs.append([int(idx_list[i][0]) for i in range(3)])

        return cls(np.array(vs), np.array(fs, dtype=np.uint32) - 1)
