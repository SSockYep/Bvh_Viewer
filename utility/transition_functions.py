from data_structure.math import *

import numpy as np


def linear(t):
    if t < 0 or t > 1:
        raise ValueError
    return 1 - t


def easeInOutCos(t):
    if t < 0 or t > 1:
        raise ValueError
    return (np.cos(np.pi * t) + 1) / 2


def easeInOutCubic(t):
    if t < 0 or t > 1:
        raise ValueError
    return 1 - (-2 * (t ** 3) + 3 * (t ** 2))
