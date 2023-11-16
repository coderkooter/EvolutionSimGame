import gym
from gym_game import Gym_Game
import random
import pygame
from stable_baselines3 import PPO
import time

# Create the game environment
env = gym.make('MyGameEnv-v0')

# start = time.time()
# model = PPO('MultiInputPolicy', env, ent_coef = 0.01)
# # model = PPO('MultiInputPolicy', env, ent_coef = 0.03)
# # model.learn(total_timesteps=1800000)
# model.learn(total_timesteps=3000000)
# model.save('trained_model')
# print("model saved")
# print("time taken: " + str(time.time() - start))

# start = time.time()
# model = PPO('MlpPolicy', env, ent_coef = 0.03)
# model.learn(total_timesteps=600000)
# model.save('small_model')
# print("model saved")
# print("time taken: " + str(time.time() - start))

# model = PPO.load('trained_model.zip')
model = PPO.load('small_model.zip')

# Reset the environment
observation = env.reset()
pygame.init()

done = False
while not done:
    # action = 1
    action, _ = model.predict(observation)  # Get the action predicted by the model
    # print(action)
    observation, reward, done, _ = env.step(action)  # Take a step in the environment based on the action
    env.render()

env.close()

pygame.quit()