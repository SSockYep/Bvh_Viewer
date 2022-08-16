import pybullet as p
import numpy as np


class Leg:
    def __init__(self, client):
        self.client = client
        footId = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.2, 0.05])
        legId = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.8])
        basePos = [0, 0, 10]
        self.leg = p.createMultiBody(
            1,
            footId,
            -1,
            basePos,
            [0, 0, 0, 1],
            linkMasses=[1, 1],
            linkCollisionShapeIndices=[-1, legId],
            linkVisualShapeIndices=[-1, -1],
            linkPositions=[[0.3, 0, 0], [0, 0, 1]],
            linkOrientations=[[0, 0, 0, 1], [0, 0, 0, 1]],
            linkInertialFramePositions=[[0.3, 0, 0], [0, 0, 0]],
            linkInertialFrameOrientations=[[0, 0, 0, 1], [0, 0, 0, 1]],
            linkParentIndices=[0, 1],
            linkJointTypes=[p.JOINT_REVOLUTE, p.JOINT_FIXED],
            linkJointAxis=[[0, 1, 0], [0, 0, 0]],
        )

    def get_ids(self):
        return self.client, self.car

    def apply_action(self, action):
        pass

    def get_observation(self):
        pass
