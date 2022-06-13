import pybullet as pb
import pybullet_data
import time
import numpy as np

physicsClient = pb.connect(pb.GUI)
pb.setAdditionalSearchPath(pybullet_data.getDataPath())
floorId = pb.createCollisionShape(pb.GEOM_PLANE)
pb.createMultiBody(floorId, 0)
pb.setGravity(0, 0, -9.8)
startPos = [0, 0, 1.5]
startOrientation = pb.getQuaternionFromEuler([0, 0, 0])

sphereId = pb.createCollisionShape(pb.GEOM_SPHERE, radius=0.1)
footId = pb.createCollisionShape(pb.GEOM_BOX, halfExtents=[0.5, 0.2, 0.05])
legId = pb.createCollisionShape(pb.GEOM_BOX, halfExtents=[0.05, 0.05, 0.8])

modelId = pb.createMultiBody(
    1,
    footId,
    -1,
    startPos,
    startOrientation,
    linkMasses=[1, 1],
    linkCollisionShapeIndices=[-1, legId],
    linkVisualShapeIndices=[-1, -1],
    linkPositions=[[0.3, 0, 0], [0, 0, 1]],
    linkOrientations=[[0, 0, 0, 1], [0, 0, 0, 1]],
    linkInertialFramePositions=[[0.3, 0, 0], [0, 0, 0]],
    linkInertialFrameOrientations=[[0, 0, 0, 1], [0, 0, 0, 1]],
    linkParentIndices=[0, 1],
    linkJointTypes=[pb.JOINT_REVOLUTE, pb.JOINT_FIXED],
    linkJointAxis=[[0, 1, 0], [0, 1, 0]],
)
for joint in range(pb.getNumJoints(modelId)):
    pb.setJointMotorControl2(
        modelId, joint, pb.VELOCITY_CONTROL, targetVelocity=1, force=10
    )

pb.changeDynamics(
    modelId, -1, spinningFriction=0.1, rollingFriction=0.001, linearDamping=0.0
)

pb.setRealTimeSimulation(1)

t = 0
while 1:
    time.sleep(0.01)
    t += 0.001
    for joint in range(pb.getNumJoints(modelId)):
        pb.setJointMotorControl2(
            modelId,
            joint,
            pb.VELOCITY_CONTROL,
            targetVelocity=np.sin(t) * 10,
            force=10,
        )
time.sleep(1000)
