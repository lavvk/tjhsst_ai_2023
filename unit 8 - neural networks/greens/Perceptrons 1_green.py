import ast
import sys

def truth_table(bits, n):
    table = []
    for i in range(2 ** bits):
        input_vec = tuple(int(x) for x in format(i, '0{}b'.format(bits)))
        output = (n >> i) & 1
        table.append((input_vec, output))
    return table

def pretty_print_tt(table):
    max_input_length = 0
    for row in table:
        input_str = ''
        for bit in row[0]:
            input_str += str(bit)
        if len(input_str) > max_input_length:
            max_input_length = len(input_str)
    
    for row in reversed(table):
        input_str = ''
        for bit in row[0]:
            input_str += str(bit)
        padding = " " * (max_input_length - len(input_str))
        print("{0} | {1}".format(input_str + padding, row[1]))


def perceptron(A, w, b, x):
    result = sum(w[i] * x[i] for i in range(len(w))) + b
    return A(result)

def check(n, w, b):
    inputs = len(w)
    truth_table_data = truth_table(inputs, n)
    correct_count = 0
    total_count = len(truth_table_data)
    for row in truth_table_data:
        input_vec = row[0]
        expected_output = row[1]
        perceptron_output = perceptron(step, w, b, input_vec)
        
        if perceptron_output == expected_output:
            correct_count += 1
    accuracy = correct_count / total_count
    return accuracy

def step(num):
    return 1 if num > 0 else 0

    
n = int(sys.argv[1])
w = ast.literal_eval(sys.argv[2])
b = float(sys.argv[3])

accuracy = check(n, w, b)
print(accuracy)
tt = truth_table(len(w), n)
print("\nTruth Table:")
pretty_print_tt(tt)