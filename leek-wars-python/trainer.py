import gym
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset(seed=42)


def V(state, player) -> float :
  return 42

for _ in range(1000):

   action = policy(observation)  # User-defined policy function
   observation, reward, terminated, truncated, info = env.step(action)

   if terminated or truncated:
      observation, info = env.reset()
env.close()
import gym

from stable_baselines3 import PPO

env = gym.make("CartPole-v1")
for _ in range(10) :
  policies.append("MlpPolicy")

model = PPO(policies, env, verbose=1)
model.learn(total_timesteps=10_000)
