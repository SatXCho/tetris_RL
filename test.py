import numpy as np
import torch
from tetris.tetris_env import TetrisEnv, GRID_HEIGHT, GRID_WIDTH
from models.dqn_agent import DQNAgent

MODEL_PATH = 'models/tetris-dqn-30.h5'

def test_dqn(model_path, episodes=10):
    env = TetrisEnv()
    state_size = GRID_WIDTH * GRID_HEIGHT
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    agent.load(model_path)

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [state_size])
        done = False
        while not done:
            env.render()  # Render the game
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            state = np.reshape(next_state, [state_size])
            if done:
                print(f"Episode: {e+1}/{episodes}, Score: {env.game.score}")
                break

    env.close()

if __name__ == "__main__":
    test_dqn(MODEL_PATH)