from letterpress.game import Game
from letterpress.arena import Arena
from letterpress.genie import Genie
from letterpress.state import State
from letterpress.agent import Agent
from gym.envs.registration import register

register(
    id='letterpress-v0',
    entry_point='letterpress.envs:GymEnv',
)
