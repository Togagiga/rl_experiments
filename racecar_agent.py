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
Genetic Algorithm (general procedure):

    Makes first generation of NN, using the same architecure but different weights

    Performance measure find the best NN after env.done == True

    Best NN is used to create the next generation    (May be necessary to use the best 3...)

    Weights of next generation are found by using the weights as the mean of a normal
    distribution and sampling from it

    Next generation is evaluated, best if chosen


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


    def get_child(self, best_model):

        child_model = self.build_model()     # new model to save new weights to

        for l in range(len(best_model.layers)):

            weights = np.array(best_model.layers[l].get_weights())
            child_weights = weights

            for i in range(len(weights[0])):
                for j in range(len(weights[0][0])):
                    child_weights[0][i][j] = np.random.normal(weights[0][i][j], self.std_deviation, 1)   # writing new weights for child

            child_model.layers[l].set_weights(child_weights)

        return child_model




def train_AI(generations, generation_size = 10, time_steps = 300):

    loss = []
    agent = AI()
    best_model = agent.model

    for generation in range(generations):

        generation_loss = []
        models = []

        for model in range(generation_size):                 # create offspring from best_model
            models.append(agent.get_child(best_model))


        for model in range(generation_size):

            state = env.reset(generation+1, model+1)
            state = np.reshape(state, (1,6))                 # initial state (reshape needed for NN)
            score = 0                                        # cumulative reward for episode
            agent.model = models[model]
            max_steps = time_steps

            for i in range(max_steps):

                action = agent.get_action(state)             # action from agent
                # print(f"Action Generated: {action}")
                reward, next_state, done = env.step(action)
                next_state = np.reshape(next_state, (1,6))
                score += reward
                state = next_state
                
                # print(f"Step Reward: {reward}")
                # print(f"State: {state}")
                # print(f"Done: {done}\n")

                if done:
                    print("--> model: {}/{}, score: {}".format(model+1, generation_size, score))
                    break

            generation_loss.append(score)


        max_gen_loss = np.argmax(generation_loss)

        if generation == 0:                               # for first gen only
            best_model = models[max_gen_loss]           

        elif generation_loss[max_gen_loss] > loss[np.argmax(loss)]:    # check whether new gen is better than best_model
            best_model = models[max_gen_loss]             # reassigning best_model based on highest loss
            # if agent.std_deviation > 0.1:
            #     agent.std_deviation -= 0.1

        else:
            # generation_loss[max_gen_loss] = loss[-1]      # if not add previous best loss to loss
            # if agent.std_deviation < 0.3:
            #     agent.std_deviation += 0.1
            pass


        loss.append(generation_loss[max_gen_loss])


        if env.quit == True:
            print("----------User Quit Training---------")
    return loss





if __name__ == "__main__":

    generations = 5
    generation_size = 3
    loss = train_AI(generations, generation_size)
    print(loss)

    # plotting
    plt.plot(range(1, generations+1), loss)
    plt.title("Learning of AI in racecar_env")
    plt.xlabel("generation")
    plt.ylabel("loss")
    plt.show()