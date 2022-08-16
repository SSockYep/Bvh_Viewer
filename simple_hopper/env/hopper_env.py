import gym
import numpy as np
from gl_render.renderer import Renderer


class HopperEnv(gym.Env):
    """
    Description:
        Hopper with one joint

    Observation:
        Dim     Observation         min     max
        0       angle of joint      -60deg  60deg
        1       velocity of x       ?       ?
        2       velocity of z       ?       ?
        3       position of x
        4       position of z
        5       angular velocity    -100    100

    Actions:
        Num     Action
        0       Torque of joint
    """

    def __init__(self):
        self.gravity = 9.8
        self.massfoot = 0.8
        self.massleg = 1.0
        self.total_mass = self.massfoot + self.massleg
        self.height = 0.5  # length of leg
        self.width = 0.12  # width of foot
        self.length = 0.28  # length of foot
        self.theta_max_rad = 60 * np.pi / 180
        self.angular_vel_max = 100

        observation_max = np.array(
            [
                self.theta_max_rad,
                np.finfo(np.float32).max,
                np.finfo(np.float32).max,
                np.finfo(np.float32).max,
                np.finfo(np.float32).max,
                self.angular_vel_max,
            ]
        )
        self.observation_space = gym.spaces.Box(
            -observation_max, observation_max, dtype=np.float32
        )

        self.action_space = gym.spaces.box([-100], [100], dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None
        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = gym.util.seeding.np_random(seed)
        return [seed]

    def reset(self):
        self.state = self.np_random.uniform(low=0.05, high=0.05, size=(6,))
        self.steps_beyond_done = None
        return np.array(self.state)

    def close(self):
        pass

    def step(self):
        pass

    def render(self):
        theta, _, _, posx, posy, _ = self.state()
        foot_min = np.array([-self.length / 2, -0.012, -self.width / 2])
        foot_max = -foot_min
        leg_min = np.array([-0.012, -self.height / 2, -0.012])
        leg_max = -leg_min
