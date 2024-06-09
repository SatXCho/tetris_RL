import numpy as np
from tetris.tetris_env import TetrisEnv, GRID_HEIGHT, GRID_WIDTH
from models.dqn_agent import DQNAgent, BATCH_SIZE

EPISODES = 1000
SAVE_EVERY = 10  # Save the model every 10 episodes

def train_dqn(episodes):
    env = TetrisEnv()
    state_size = GRID_WIDTH * GRID_HEIGHT
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [state_size])
        for time in range(5000):
            env.render()  # Render the game
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > BATCH_SIZE:
                agent.replay(BATCH_SIZE)

        # Save the model every SAVE_EVERY episodes
        if e % SAVE_EVERY == 0:
            agent.save(f"models/tetris-dqn-{e}.h5")

    env.close()

if __name__ == "__main__":
    train_dqn(EPISODES)
