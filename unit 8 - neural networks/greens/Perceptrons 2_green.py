import sys


def truth_table(bits, n):
    table = []
    for i in range(2 ** bits -1,-1,-1): ## trial and error w -2, -1, 1 
        input_vec = tuple(int(x) for x in format(i, '0{}b'.format(bits)))
        output = (n >> i) & 1
        table.append((input_vec, output))
    return table

'''
def truth_table(bits, n):
    table = []
    for i in range(2 ** bits):
        input_vec = tuple(int(x) for x in format(i, '0{}b'.format(bits)))
        output = (n >> i) & 1
        table.append((input_vec, output))
    return table
    
truth table returning wrong results?? ughafioaks;fjao
------
Final w: [3, 2, 3, 1]
Final b: -5
Accuracy: 0.9375 

should be :: ((3, 0, 2, 2), -4, 0.8125)
debug--?
error in truth table loooping range cus logic is fine
https://www.pythonclassroom.com/loops/for-loop-range-three-arguments

example:: 
for i in range(100,0,-10):
   print(i)

'''

def add_scaled(vec1, vec2, scale):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i] + scale * vec2[i])
    return result

def step(num):
    return 1 if num > 0 else 0

def perceptron(A, w, b, x):
    weighted_sum = 0
    for i in range(len(w)):
        weighted_sum += w[i] * x[i]

    result = A(weighted_sum + b)  
    return result

def accuracy(truth_table_data, w, b):
    correct_count = 0
    for inp_row, n_out in truth_table_data:
        conv_inputs = [int(val) for val in inp_row]
        if perceptron(step, w, b, conv_inputs) == int(n_out):
            correct_count += 1
    
    total_count = len(truth_table_data)
    accuracy = correct_count / total_count
    return accuracy


def update_weights_and_bias(init_w, init_b, truth_data):
    lr = 1
    for inp_row, n_out in truth_data:
        conv_inputs = [int(ch) for ch in inp_row]
        out = perceptron(step, init_w, init_b, conv_inputs)
        init_w = add_scaled(init_w, conv_inputs, (int(n_out) - out) * lr)
        init_b += (int(n_out) - out) * lr
    return init_w, init_b

def check_convergence(init_w, init_b, prev_w, prev_b):
    if prev_w is not None and prev_b is not None:
        equal_w = all(init_w[i] == prev_w[i] for i in range(len(init_w)))
        if equal_w and init_b == prev_b:
            return True
    return False

def stabilize_b(bits, init_w, init_b):
    max_epoch = 100
    truth_data = truth_table(len(init_w), bits)
    prev_w = None
    prev_b = None
    epoch = 0
    
    while epoch < max_epoch:
        init_w, init_b = update_weights_and_bias(init_w, init_b, truth_data)
        if check_convergence(init_w, init_b, prev_w, prev_b):
            return init_w, init_b
        prev_w = init_w.copy()
        prev_b = init_b
        epoch += 1
    
    return init_w, init_b


# bits = 4
# n = 60800
bits = int(sys.argv[1])
n = int(sys.argv[2])

init_w = []
for _ in range(bits):
    init_w.append(0)

init_b = 0

final_w, final_b = stabilize_b(n, init_w, init_b)

print("Final w:", final_w)
print("Final b:", final_b)
print("Accuracy:", accuracy(truth_table(bits, n), final_w, final_b))

