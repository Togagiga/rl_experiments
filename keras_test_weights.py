import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

action_space = 5
state_space = 6


# takes in state of env and outputs action
def build_model():
    model = Sequential()
    model.add(Dense(32, activation = "relu", input_shape=(state_space,)))
    model.add(Dense(16, activation = "relu"))
    model.add(Dense(action_space, activation = "softmax"))
#     model.compile(optimizer = "rmsprop",
#                   loss = "categorical_crossentropy",
#                   metrics=["accuracy"])

    return model


model = build_model()
input_data = np.array([165, 120, 60, 30, 150, 5.5])
input_data = input_data.reshape(1,input_data.shape[0])
# ensuring input shape is correct
print(f"\n\nShape of input of model: {input_data.shape}")

# making predictions based on initialised model
prediction = model.predict(input_data, batch_size=1)
print(prediction[0])
print(f"------> PREDICTED ACTION: {np.argmax(prediction[0])}\n\n")


for layer in model.layers:
    weights = np.array(layer.get_weights())
    inputs = weights[0]
    outputs = weights[1]
    print(f"----------LAYER {layer.name}----------")
    print(f"Weights per Neuron: {len(inputs)}, No of Neurons: {len(inputs[0])}")
    print(inputs)
    print(f"Outputs of Layer (one for each Neuron): {len(outputs)}")
    print(outputs)
    print("\n")
    
# layer.set_weights(weights)