import gym
from letterpress.game import Game
from gym import error, spaces, utils
from gym.utils import seeding


class GymEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = Game('hvm')
        self.observation_space = spaces.Box(low=-1, high=1, shape=25)
        self.action_space = spaces.Discrete(625)

    def step(self, action):
        indices = [action[0] // 25, action[0] % 25]
        rec = self.game.genie.recommend(indices=indices, state=self.game.state)
        self.game.state.select_tiles(rec)
        self.game.state.play_selected_word()
        self.game.agent.play('red')
        scores = self.game.state.get_score()
        reward = 1 if self.game.state.is_finished() and scores['blue'] > scores['red'] else 0
        return self.game.state.state, reward, self.game.state.is_finished(), {}

    def reset(self):
        self.game = Game('hvm')
        return self.game.state.state

    def render(self, mode='human'):
        print(self.game.state.state)

    def close(self):
        pass
