import sys
import numpy as np

def step(num):
    return 1 if num > 0 else 0
    
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(num):
    sig = sigmoid(num)
    return sig * (1 - sig)


# def perceptron(A, w, b, x):
#     weighted_sum = 0
#     for i in range(len(w)):
#         weighted_sum += w[i] * x[i]
#     result = A(weighted_sum + b)
#     return result

def p_net(A, x, w_list, b_list):
    newA = np.vectorize(A)
    for layer in range(1, len(w_list)):
        a0 = newA(x @ w_list[layer] + b_list[layer])
        x = a0
    return a0

def accuracy(pt): 
    return 1 if (pt[0][0] ** 2 + pt[0][1] ** 2) ** 0.5 < 1 else 0


def train_network(training, ep_num, w_list, b_list, mode):
    newsig = np.vectorize(sigmoid)
    
    for i in range(ep_num):
        for data in training:
            x, y = data 
            a, dot, delta = [x], [None], [None] * len(w_list)
            
            lr = 0.1
            N = len(w_list) - 1
            
            for L in range(1, len(w_list)):
                dot.append((a[L - 1] @ w_list[L]) + b_list[L])
                a.append(newsig(dot[L]))
            
            delta[N] = (newsig(dot[N]) * (1 - newsig(dot[N]))) * (y - a[N])
            for L in range(N - 1, 0, -1):
                delta[L] = (newsig(dot[L]) * (1 - newsig(dot[L]))) * (delta[L + 1] @ w_list[L + 1].transpose())

            for L in range(1, len(w_list)):
                b_list[L] += lr * delta[L]
                w_list[L] += lr * ((a[L-1]).T @ delta[L])
        
        if mode == "C":
            misclass = 0
            for pt in training:
                if round(p_net(sigmoid, pt[0][0], w_list, b_list)[0][0]) != pt[1][0][0]:
                    misclass += 1
            print("Epoch", i, ":", misclass)
        
            
    return w_list, b_list



mode = sys.argv[1]

if mode == "S":
    trainingSet = [
        (np.array([[0, 0]]), np.array([[0, 0]])), 
        (np.array([[0, 1]]), np.array([[0, 1]])), 
        (np.array([[1, 0]]), np.array([[0, 1]])), 
        (np.array([[1, 1]]), np.array([[1, 0]]))
        
        ]
    weightList = [None, 2 * np.random.rand(2, 2) - 1, 2 * np.random.rand(2, 2) - 1]
    biasList = [None, 2 * np.random.rand(1, 2) - 1, 2 * np.random.rand(1, 2) - 1]
    
    def train(wList, bList):
        newSigmoid = np.vectorize(sigmoid)
        for i in range(7500):
            for data in trainingSet:
                x, y = data
                a, dot, delta = [x], [None], [None] * len(wList)
                learningRate = 0.1
                n = len(wList) - 1
                for layer in range(1, len(wList)):
                    dot.append((a[layer - 1] @ wList[layer]) + bList[layer])
                    a.append(newSigmoid(dot[layer]))
                delta[n] = (newSigmoid(dot[n]) * (1 - newSigmoid(dot[n]))) * (y - a[n])
                for layer in range(n - 1, 0, -1):
                    delta[layer] = (newSigmoid(dot[layer]) * (1 - newSigmoid(dot[layer]))) * (delta[layer + 1] @ (wList[layer + 1]).T)
                for layer in range(1, len(wList)):
                    bList[layer] = bList[layer] + learningRate * delta[layer]
                    wList[layer] = wList[layer] + learningRate * ((a[layer-1]).transpose() @ delta[layer])
                print(a[len(a) - 1])
            print()
        return (wList, bList)
    weightList, biasList = train(weightList, biasList)    

elif mode == "C":
    training = []
    with open("10000_pairs.txt") as f:
        for line in f:
            x, y = line.split()
            pt = np.array([[float(x), float(y)]])
            inOrOut = accuracy(pt)
            training.append((pt, np.array([[inOrOut]])))     
    w_list = [None, np.random.rand(2, 4), np.random.rand(4, 1)]
    b_list = [None, np.random.rand(1, 4), np.random.rand(1, 1), np.random.rand(1, 1)]
    w_list, b_list = train_network(training, 1000, w_list, b_list, mode)