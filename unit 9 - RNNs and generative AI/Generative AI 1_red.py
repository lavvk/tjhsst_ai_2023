import re
import numpy as np
from collections import Counter
import pickle

with open('Shakespeare.txt', 'r') as f:
    text = f.read().lower()

text = re.sub(r'[^a-z0-9\s]', '', text)

chars = sorted(list(set(text)))
char_to_index = dict((c, i) for i, c in enumerate(chars))
index_to_char = dict((i, c) for i, c in enumerate(chars))

seq_length = 101  
step = 3  

sentences = []
next_chars = []
for i in range(0, len(text) - seq_length, step):
    sentences.append(text[i:i+seq_length])
    next_chars.append(text[i+seq_length])

X = np.zeros((len(sentences), seq_length, len(chars)), dtype=np.bool_)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool_)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_to_index[char]] = 1
    y[i, char_to_index[next_chars[i]]] = 1
    
num_test = int(0.2 * len(X))
X_train = X[:-num_test]
y_train = y[:-num_test]
X_test = X[-num_test:]
y_test = y[-num_test:]

np.random.seed(42)

# architecture 
hidden_size = 128
input_dim = len(chars)
output_dim = len(chars)

# initialize weights
Wgx = np.random.randn(input_dim, hidden_size) / np.sqrt(input_dim)  
Wgh = np.random.randn(hidden_size, hidden_size) / np.sqrt(hidden_size)
Wgo = np.zeros((hidden_size, 1))

Wox = np.random.randn(input_dim, output_dim) / np.sqrt(input_dim)
Woh = np.random.randn(hidden_size, output_dim) / np.sqrt(hidden_size)
Woo = np.zeros((output_dim, 1))  

bg = np.zeros((hidden_size, 1))
bo = np.zeros((output_dim, 1))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / np.sum(e_x, axis=-1, keepdims=True)
    
def forward(X):
    T = len(X)
    g = np.zeros((T+1, hidden_size, 1))  
    o = np.zeros((T+1, output_dim, 1))
    
    for t in range(T):
        x_t = X[t, :].reshape(-1, 1) 
        g_t = tanh(Wgx @ x_t + Wgh @ g[t-1] + bg)
        o_t = softmax(Wox @ x_t + Woh @ g_t + bo)
        g[t] = g_t
        o[t] = o_t
        
    return g, o

def backward(y, o):
    T = len(y)
    
    dWgx, dWgh, dWgo = np.zeros_like(Wgx), np.zeros_like(Wgh), np.zeros_like(Wgo)
    dWox, dWoh, dWoo = np.zeros_like(Wox), np.zeros_like(Woh), np.zeros_like(Woo)
    dbg, dbo = np.zeros_like(bg), np.zeros_like(bo)
    
    dg_next = np.zeros_like(bg)
    for t in range(T, 0, -1):
        y_t = y[t-1].reshape(-1, 1)
        o_t = o[t].reshape(-1, 1)
        
        do_t = o_t - y_t
        dWox += np.outer(X[t-1], do_t).T
        dWoh += do_t @ dg_next.T
        dWoo += do_t
        dbo += do_t.reshape(-1)
        
        dg = (Woh.T @ do_t) * (1 - g[t]**2)  
        dWgh += dg @ g[t-1].T  
        dWgx += dg @ X[t-1].reshape(-1, 1).T
        dWgo += dg
        dbg += dg.reshape(-1)
        
        dg_next = dg
        
    return dWgx, dWgh, dWgo, dWox, dWoh, dWoo, dbg, dbo

learning_rate = 0.001
epochs = 60

for epoch in range(epochs):
    
    permutation = np.random.permutation(len(X_train))
    X_train = X_train[permutation]
    y_train = y_train[permutation]
    
    for i in range(0, len(X_train), 128):
        X_batch = X_train[i:i+128]
        y_batch = y_train[i:i+128]
        
        g, o = forward(X_batch)
        
        dWgx, dWgh, dWgo, dWox, dWoh, dWoo, dbg, dbo = backward(y_batch, o)
        
        Wgx -= learning_rate * dWgx
        Wgh -= learning_rate * dWgh  
        Wgo -= learning_rate * dWgo
        Wox -= learning_rate * dWox
        Woh -= learning_rate * dWoh
        Woo -= learning_rate * dWoo
        bg -= learning_rate * dbg
        bo -= learning_rate * dbo
        
    g, o = forward(X_test)
    y_pred = np.argmax(o[1:], axis=1)
    y_true = np.argmax(y_test, axis=1)
    test_acc = np.mean(y_pred == y_true)
    print(f'Epoch {epoch+1}, Test acc: {test_acc:.4f}')
    
    with open(f'model_epoch_{epoch+1}.pkl', 'wb') as f:
        pickle.dump((Wgx, Wgh, Wgo, Wox, Woh, Woo, bg, bo), f)
        
seed_text = "ROMEO:"
seed = [char_to_index[c] for c in seed_text]
g = np.zeros((1, hidden_size, 1))

for i in range(50):
    x = np.zeros((1, len(chars)))
    x[0, seed] = 1
    
    g = tanh(Wgx @ x.T + Wgh @ g + bg)
    o = softmax(Wox @ x.T + Woh @ g + bo)
    
    next_index = np.argmax(o)
    next_char = index_to_char[next_index]
    
    seed_text += next_char
    seed = seed[1:]
    seed.append(next_index)

print(seed_text)