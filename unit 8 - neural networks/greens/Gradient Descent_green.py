import sys 
import numpy as np  

def p_deriv(x, y):

    if sys.argv[1] == 'A':  # if func a

        return np.array([[8*x - 3*y + 24, -3*x + 4*y - 20]])
    else: # if func b
        return np.array([[2*(x-y), -2*x + 4*y - 2]])

n = 1 
x = np.array([[0, 0]])  
lr = 0.1  
gradient = p_deriv(x[0][0], x[0][1])  

print("Iteration:", n)
print("x:", x[0])
print("Gradient:", gradient[0])

while np.linalg.norm(gradient[0]) > pow(10, -8):

    x = x - lr*gradient
    gradient = p_deriv(x[0][0], x[0][1])

    n += 1

    print("Iteration:", n)
    print("x:", x[0])
    print("Gradient:", gradient[0])
