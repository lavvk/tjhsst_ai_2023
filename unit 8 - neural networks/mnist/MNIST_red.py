import numpy as np
import pickle
from scipy.ndimage import rotate

weight = []
bias = []
    

def save_weights(weights_file):
    with open(weights_file, 'wb') as f:
        var = [weight, bias]
        pickle.dump(var, f)

def step(nums):
    row = nums[0, :]
    val = np.max(row)
    row[:] = np.where(row == val, 1, 0)

def sigmoid(num):
    return 1 / (1 + np.exp(-num))

def p_net(A, x, weight, bias):
    new_A = np.vectorize(A)
    a0 = x
    for weights, biases in zip(weight, bias):
        a0 = new_A(a0 @ weights + biases)
    return a0

def error(out, correct):
    misclassified = np.sum(np.argmax(out, axis=1) != np.argmax(correct, axis=1))
    total = out.shape[0]
    return misclassified / total

def jitter_image(image):
    transformations = [
        lambda img: np.roll(img, 1, axis=0),  # shift up
        lambda img: np.roll(img, -1, axis=0),  # shift down
        lambda img: np.roll(img, 1, axis=1),  # shift left
        lambda img: np.roll(img, -1, axis=1),  # shift right
        lambda img: rotate(img, 15, reshape=False),  # rotate right 15 degrees
        lambda img: rotate(img, -15, reshape=False)  # rotate left 15 degrees
    ]
    transform = np.random.choice(transformations)
    return transform(image)

def backpropagate(A, train, weight, bias, lr, epochs):
    new_A = np.vectorize(A)
    weights_file = input("save data to file:")
    for epoch in range(epochs):
        for x, y in train:
            x = jitter_image(x.reshape(28, 28)).flatten().reshape(1, -1)  
            a = [x]
            for weights, biases in zip(weight, bias):
                a.append(new_A(a[-1] @ weights + biases))
            delta = [(a[-1] * (1 - a[-1])) * (y - a[-1])]
            t_lr = np.sqrt(error(a[-1], y)) * lr  # variable lr
            for layer in range(len(weight) - 2, -1, -1):
                delta = [(a[layer + 1] * (1 - a[layer + 1])) * (delta[0] @ weight[layer + 1].T)] + delta
            for layer in range(len(weight)):
                bias[layer] += t_lr * delta[layer]
                weight[layer] += t_lr * (a[layer].T @ delta[layer])
            out = p_net(sigmoid, x, weight, bias)
            err = error(out, y)
        accuracy = sum((p_net(sigmoid, x, weight, bias) == y).all() for x, y in train)
        print(f"num of misclassified points for Epoch {epoch + 1}: {len(train) - accuracy}")
        save_weights(weights_file)
    return err

choice = input("new or load (type n or l) ").lower()
if choice == 'l':
    filename = input("Filename? ")
    with open(filename, 'rb') as f:
        myVar = pickle.load(f)
        weight, bias = myVar
else:
    arch = [784, 300, 100, 10]
    for i in range(len(arch) - 1):
        weights = []
        for _ in range(arch[i]):
            weights_row = []
            for _ in range(arch[i + 1]):
                weight_value = 2 * np.random.rand() - 1
                weights_row.append(weight_value)
            weights.append(weights_row)
        weights = np.array(weights)

        biases = []
        for _ in range(arch[i + 1]):
            bias_value = 2 * np.random.rand() - 1
            biases.append([bias_value])
        biases = np.array(biases)

        weight.append(weights)
        bias.append(biases)

train = []
with open('mnist_train.csv') as f:
    lines = f.readlines()
    
    for line in lines:
        x_values = []
        for i in line.split(',')[1:]:
            x_values.append(float(i) / 255)
        
        x = np.array(x_values)
        
        y_values = []
        for i in range(10):
            if i != int(line[0]):
                y_values.append(0)
            else:
                y_values.append(1)
        
        y = np.array(y_values)
        train.append([np.array([x]), y])

run = backpropagate(sigmoid, train, weight, bias, 0.6, 10)
