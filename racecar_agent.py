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
Genetic Algorithm (general method):

    Makes first generation of NNs, using the same architecure but different weights

    Performance measure used to find the best NN after env.done == True

    Next gen is probabilistically sampled from previous generation, with better performing models
    given higher probability of being picked

    Next generation is then mutated using perform_mutation which probabilistically changes a certain
    percentage of weights by sampling from a normal distribution

    This next then is then tested and performance is measured


Next Steps:

    Add a cross population method

    Keep best 20% of models and sample other 80%



ACTIONS:
    0 == forward + left
    1 == forward + right
    2 == left
    3 == right
    4 == forward

STATE:
    [L_sensor, FL_sensor, F_sensor, FR_sensor, R_sensor, car.vel]

'''
############


class AI():
    def __init__(self, action_space = 5, state_space = 6):
        self.action_space = action_space
        self.state_space = state_space
        self.std_deviation = 0.1
        self.mutation_probability = 0.3

        self.model = self.build_model()                               # creating model


    def build_model(self):
        model = Sequential()
        model.add(Dense(32, activation = "relu", input_shape=(self.state_space, )))
        model.add(Dense(16, activation = "relu"))
        model.add(Dense(self.action_space, activation = "softmax"))

        return model

    def get_action(self, state):      # return action from model
        prediction_values = self.model.predict(state, batch_size=1)
        return np.argmax(prediction_values[0])


    def get_cumulative_probs(self, generation_loss):
        reward = np.array(generation_loss)**2  # better values are favoured
        total = sum(reward)
        reward = reward/total

        cum_probs = [reward[0]]
        for i in range(1, len(reward)):
            cum_probs.append(cum_probs[i-1] + reward[i])
        return cum_probs


    def get_next_gen(self, generation_loss, generation_size):
        cumulative_probabilities = self.get_cumulative_probs(generation_loss)
        next_gen = []
        for i in range(generation_size):
            sample = np.random.rand()
            # print(sample)
            for j in range(len(cumulative_probabilities)):
                if sample <= cumulative_probabilities[j]:
                    next_gen.append(j)
                    break
        return next_gen


    def perform_mutation(self, model):

        child_model = self.build_model()     # new model to save new weights to

        for l in range(len(model.layers)):

            weights = np.array(model.layers[l].get_weights())
            child_weights = weights

            for i in range(len(weights[0])):
                for j in range(len(weights[0][0])):
                    if np.random.rand() < self.mutation_probability:
                        child_weights[0][i][j] = np.random.normal(weights[0][i][j], self.std_deviation, 1)   # writing new weights for child

            child_model.layers[l].set_weights(child_weights)

        return child_model

    def mate_generation():
        # still needs to be implemented
        pass



def train_AI(generations, generation_size = 10, time_steps = 300):

    loss = []
    agent = AI()
    current_gen = []

    # need to create initial generation
    for model in range(generation_size):
        current_gen.append(agent.build_model())


    for generation in range(generations):

        generation_loss = []

        for model in range(generation_size):

            state = env.reset(generation+1, model+1)
            state = np.reshape(state, (1,6))                 # initial state (reshape needed for NN)
            score = 0                                        # cumulative reward for episode
            agent.model = current_gen[model]
            agent.model = agent.perform_mutation(agent.model)# need to create mutation
            max_steps = time_steps

            for i in range(max_steps):

                action = agent.get_action(state)             # action from agent
                reward, next_state, done = env.step(action)  # one frame
                next_state = np.reshape(next_state, (1,6))   # reshape for NN
                score += reward
                state = next_state

                if done:
                    print("--> generation: {}, model: {}/{}, score: {}".format(generation+1, model+1, generation_size, round(score, 3)))
                    break

            generation_loss.append(score)

        # reassign current_gen using probabilistic method rather than deterministic
        next_gen = agent.get_next_gen(generation_loss, generation_size)
        next_gen_temp = []
        for i in next_gen:
            next_gen_temp.append(current_gen[i])
        current_gen = next_gen_temp
        print()

        loss.append(generation_loss[np.argmax(generation_loss)])


        if env.quit == True:
            print("----------User Quit Training---------")
    return loss




if __name__ == "__main__":

    generations = 10
    generation_size = 10
    loss = train_AI(generations, generation_size)
    print(f"Generation Loss: {loss}")

    # plotting
    plt.plot(range(1, generations+1), loss)
    plt.title("Learning of AI in racecar_env")
    plt.xlabel("generation")
    plt.ylabel("loss")
    plt.show()