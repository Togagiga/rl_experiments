from test_env import Car

import random
import numpy as np
import tensorflow as tf
from collections import deque
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt



env = Car()

class DQN():

	### Based on Q Learning Paper: https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf###

	def __init__(self, action_space = 3, state_space = 4):
		self.action_space = action_space
		self.state_space = state_space
		self.epsilon = 1
		self.gamma = 0.95
		self.batch_size = 64
		self.epsilon_min = 0.01
		self.epsilon_decay = 0.995
		self.learning_rate = 0.001
		self.memory = deque(maxlen=100000)
		self.model = self.build_model()

	def build_model(self):

		model = Sequential()
		model.add(Dense(64, input_shape=(self.state_space,), activation="relu"))
		model.add(Dense(64, activation="relu"))
		model.add(Dense(self.action_space, activation="linear"))
		model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
		return model

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))    # write to memory

	def act(self, state):
		if np.random.rand() <= self.epsilon:        # with prob epsilon pick random action
			return random.randrange(self.action_space)
		act_values = self.model.predict(state)      # pass state into model
		return np.argmax(act_values[0])             # choose best outcome from model as action


	# Why is this needed????
	def replay(self):

		if len(self.memory) < self.batch_size:
			return

		# when memory is bigger than batch_size create minibatch
		minibatch = random.sample(self.memory, self.batch_size)     # sequence, length of sample
		states = np.array([i[0] for i in minibatch])
		actions = np.array([i[1] for i in minibatch])
		rewards = np.array([i[2] for i in minibatch])
		next_states = np.array([i[3] for i in minibatch])
		dones = np.array([i[4] for i in minibatch])

		states = np.squeeze(states)
		next_states = np.squeeze(next_states)

		targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones) # for non-terminal
		targets_full = self.model.predict_on_batch(states)                                                   # for terminal

		# assemble complete target matrix
		targets_fin = np.zeros((64,3))    # cannot index tf.tensor -> workaround
		for i,t in enumerate(actions):
			targets_fin[i] = targets_full[i]
			targets_fin[i][t] = targets[i]

		# perform gradient descent
		self.model.fit(states, targets_fin, epochs=1, verbose=0)
		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay


def train_dpn(episode):
	loss = []
	agent = DQN()
	for e in range(episode):
		state = env.reset()
		state = np.reshape(state, (1,4))
		score = 0
		max_steps = 10000                     # if = 1000 does not go beyond scor:14
		for i in range(max_steps):
			action = agent.act(state)
			reward, next_state, done = env.step(action)
			score += reward
			next_state = np.reshape(next_state, (1,4))
			agent.remember(state, action, reward, next_state, done)
			state = next_state
			agent.replay()     # Why?
			if done:
				print("episode: {}/{}, score: {}".format(e, episode, score))
				break
		loss.append(score)
	return loss

if __name__ == "__main__":

	ep = 100
	loss = train_dpn(ep)
	plt.plot([i for i in range(ep)], loss)
	plt.xlabel("episodes")
	plt.ylabel("reward")
	plt.show()
