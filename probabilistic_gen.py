import numpy as np

gen_loss = [38.1098315462866, 13.196932910066216, 89.252232817577294, 39.252232817577294, 39.252232817577294]

def get_cumulative_probs(gen_loss):
    reward = np.array(gen_loss)
    total = sum(reward)
    reward = reward/total
    print(reward)

    cum_probs = [reward[0]]
    for i in range(1, len(reward)):
        cum_probs.append(cum_probs[i-1] + reward[i])

    return cum_probs

def get_next_gen(cumulative_probabilities, generation_size = 5):
    next_gen = []
    for i in range(generation_size):
        sample = np.random.rand()
        # print(sample)
        for j in range(len(cumulative_probabilities)):
            if sample <= cumulative_probabilities[j]:
                next_gen.append(j)
                break
    return next_gen



cum_probs = get_cumulative_probs(gen_loss)
print(cum_probs)
print(get_next_gen(cum_probs))