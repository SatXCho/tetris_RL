import gym
from gym import spaces
import numpy as np
import pygame
from .tetris_game import Tetris

GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

class TetrisEnv(gym.Env):
    def __init__(self):
        super(TetrisEnv, self).__init__()
        self.action_space = spaces.Discrete(6)  # 0: left, 1: right, 2: down, 3: rotate, 4: drop, 5: no-op
        self.observation_space = spaces.Box(low=0, high=1, shape=(GRID_HEIGHT, GRID_WIDTH), dtype=np.uint8)
        self.game = Tetris()
        self.screen = None

    def reset(self):
        self.game = Tetris()
        return self._get_state()

    def step(self, action):
        if action == 0:  # move left
            if self.game.valid_move(-1, 0):
                self.game.move_piece(-1, 0)
        elif action == 1:  # move right
            if self.game.valid_move(1, 0):
                self.game.move_piece(1, 0)
        elif action == 2:  # move down
            if self.game.valid_move(0, 1):
                self.game.move_piece(0, 1)
        elif action == 3:  # rotate
            rotated_piece = [list(row) for row in zip(*self.game.current_piece['shape'][::-1])]
            if self.game.valid_move(0, 0, rotated_piece):
                self.game.rotate_piece()
        elif action == 4:  # drop
            while self.game.valid_move(0, 1):
                self.game.move_piece(0, 1)
            self.game.lock_piece()

        # Automatically move piece down after rotation or move action
        if not action == 2 and not action == 4:
            if self.game.valid_move(0, 1):
                self.game.move_piece(0, 1)
            else:
                self.game.lock_piece()

        reward = self.game.score
        done = self.game.game_over
        return self._get_state(), reward, done, {}

    def _get_state(self):
        state = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.uint8)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.game.grid[y][x] != 0:
                    state[y][x] = 1
        return state

    def render(self, mode='human'):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))

        self.screen.fill((0, 0, 0))
        self.game.draw_grid(self.screen)
        self.game.draw_piece(self.screen)
        pygame.display.flip()

    def close(self):
        if self.screen is not None:
            pygame.quit()
            self.screen = None
