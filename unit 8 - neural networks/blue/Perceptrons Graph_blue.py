from matplotlib import pyplot as plt

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

def set_vals(weights, bias, start_x, end_x, step_size):
    current_x = start_x
    grid_x = []
    grid_y = []
    grid_color = []

    while current_x < end_x + step_size:
        current_y = start_x
        while current_y < end_x + step_size:
            grid_x.append(current_x)
            grid_y.append(current_y)
            value = perceptron(step, weights, bias, [current_x, current_y])
            grid_color.append('#FF0000' if value == 0 else '#00FF00')
            current_y += step_size
        current_x += step_size
    
    return grid_x, grid_y, grid_color


def plot_decision_boundaries(figure, axis, w, b, i):
    r = i // 4
    c = i % 4
    axis[r, c].axhline(0, color='black')
    axis[r, c].axvline(0, color='black')
    x, y, color = set_vals(w, b, -2, 2, 0.1)
    axis[r, c].scatter(x, y, s=1, color=color) 
    for true_val in truth_table(len(w), i):
        color = '#FF0000' if int(true_val[1]) == 0 else '#00FF00'
        axis[r, c].scatter(int(true_val[0][0]), int(true_val[0][1]), color=color)

def all_graphs():
    n = 2
    figure, axis = plt.subplots(4, 4)
    for i in range(2 ** (2 ** n)):
        w = [0 for j in range(n)]
        b = 0
        w, b = stabilize_b(i, w, b)
        plot_decision_boundaries(figure, axis, w, b, i)
    plt.show()

all_graphs()
