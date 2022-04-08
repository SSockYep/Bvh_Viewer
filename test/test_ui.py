import numpy as np
import pytest
from ui.renderer import Renderer

class TestRenderer:
    def test_init(self):
        assert Renderer()