import sys
import numpy as np
import ast

def truth_table(bits, n):
    table = []
    for i in range(2 ** bits - 1, -1, -1):
        input_vec = tuple(int(x) for x in format(i, '0{}b'.format(bits)))
        output = (n >> i) & 1
        table.append((input_vec, output))
    return table

def add_scaled(vec1, vec2, scale):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i] + scale * vec2[i])
    return result

def step(num):
    return 1 if num > 0 else 0

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def perceptron(A, w, b, x):
    weighted_sum = 0
    for i in range(len(w)):
        weighted_sum += w[i] * x[i]
    result = A(weighted_sum + b)
    return result

def check(n, w, b):
    tt = truth_table(len(w), n)
    accuracy = 0
    for val in tt:
        converted = [int(ch) for ch in val[0]]
        if perceptron(step, w, b, converted) == int(val[1]):
            accuracy += 1
    return accuracy / len(tt)

def p_net(A, x, w_list, b_list):
    aL = x
    for layer in range(len(w_list[0])):
        aL = np.vectorize(A)(aL@w_list[layer] + b_list[layer])
    return aL


def challenge1(argv):
    if len(argv) ==2:
        w_list = [np.array([[-1, 1],[-2, 1]]),np.array([[1],[2]])]
        b_list = [np.array([[3,0]]),np.array([[-2]])]
    inp = list(ast.literal_eval(argv[1]))
    # XOR HAPPENS HERE
    print(p_net(step, np.array([[inp[0],inp[1]]]), w_list, b_list)[0][0])

def challenge2(argv): ## diamond
    if len(argv) == 3:
        w_list = [np.array([[1,1,-1,-1],[1,-1,1,-1]]),np.array([[1],[2],[3],[4]])]
        b_list = [np.array([[1,1,1,1]]),np.array([[-9]])]
    if p_net(step, np.array([[float(argv[1]), float(argv[2])]]), w_list, b_list)[0][0] == 1:
        result = 'Inside'
    else:
        result = 'Outside'   
             
    print(result)

def challenge3(): ## circle
    np.random.seed(42)  
    x = np.random.uniform(-1, 1, 500)
    y = np.random.uniform(-1, 1, 500)
    
    w_list = [ np.array([[1, 1, -1, -1], [1, -1, 1, -1]]), np.array([[1], [1], [1], [1]]) ]
    b_list = [np.array([[2.1, 2.1, 2.1, 2.1]]), np.array([[-3.42]])]
    accuracy = 0
    points = []
    for i in range(500):
        if p_net(sigmoid, np.array([[x[i], y[i]]]), w_list, b_list)[0][0] > 0.5:
            value = 1
        else:
            value = 0
        if np.power(x[i], 2) + np.power(y[i], 2) < 1:
            real = 1
        else:
            real = 0
        if value == real:
            accuracy += 1
        else:
            points.append((x[i], y[i]))
            
    print("Points:", points)
    print("Accuracy:", str(accuracy / 5) + '%')

if len(sys.argv) == 2:
    challenge1(sys.argv)
elif len(sys.argv) == 3:
    challenge2(sys.argv)
else:
    challenge3()
