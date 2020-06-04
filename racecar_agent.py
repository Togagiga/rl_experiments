from racecar_env import Game

import random
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

env = Game()    # initialising environment


### NOTE ###

'''
AI class is doing nothing at this point

defining two nested for loop:
	outer loops through episodes:

		env.reset() called

	inner loops through frames by calling env.step():

		input to step() is randomly generated integer, i~[0,4] (sampled from the closed interval 0 to 4)
		cumulative reward (score) represents loss of episode
'''


class AI():
	def __init__(self, action_space = 5, state_space = 6):
		self.action_space = action_space
		self.state_space = state_space

		self.model = self.build_model()

	def build_model(self):
		model = Sequential()
		# model.add(.......)	 

		return model


def train_AI(episode):
	loss = []
	agent = AI()
	for e in range(episode):
		state = env.reset()
		score = 0                               # cumulative reward for episode
		max_steps = 10000                       # up to 10000 frames/episode
		for i in range(max_steps):
			action = random.randint(0,4)
			# action = AI()     --------------> need to generate action from AI (agent)
			reward, next_state, done = env.step(action)
			# print(f"Step Reward: {reward}")
			# print(f"State: {state}")
			# print(f"Done: {done}")
			score += reward
			state = next_state
			if done:
				print("--> episode: {}/{}, score: {}".format(e+1, episode, score))
				break
		loss.append(score)
	if env.quit == True:
		print("----------User Quit Training---------")
	return loss



if __name__ == "__main__":
	episodes = 50
	loss = train_AI(episodes)
	plt.plot(range(episodes), loss)
	plt.title("Learning of AI in racecar_env")
	#plt.xticks(range(episodes), range(1, episodes + 1))
	plt.xlabel("episode")
	plt.ylabel("loss")
	plt.show()