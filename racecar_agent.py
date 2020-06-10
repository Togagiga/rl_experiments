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
	def __init__(self, action_space = 5, state_space = 6, no_models):
		self.action_space = action_space
		self.state_space = state_space

		# self.models = []
		# for i in range(no_models+1):
		# 	self.models.append(self.build_model())

		self.model = build_model()


	def build_model(self):
		model = Sequential()
		model.add(Dense(30, activation = "relu", input_shape(6,1)))
		model.add(Dense(15, activation = "relu"))
		model.add(Dense(5, activation = "softmax"))

		return model


# run whole gen then call choose_best
	def choose_best():
		# if prev_score < cur_score:
			# model.save_weighs()
		pass

	def next_gen():
		# new_weights = np.sample(data, normal)
		# new_model = old_model.load_weight(new_weights)

		pass

'''
figure out how to randomise model weight for inilialising first gen

be able to save weight of best models  (weight = model.save_weight())

use a normal distrib on weight to make generation 2....-> for loop to sample from normal distrib for each weight???
'''


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
			if i == 0:
				action = 0

			reward, next_state, done = env.step(action)
			train(model)
			action = model.evaluate(next_state)

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