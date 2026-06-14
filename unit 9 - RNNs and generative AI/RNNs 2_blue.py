import numpy as np

def generate_data(n_seqs):
    seq_len = 50
    x = np.random.uniform(-1, 1, (n_seqs, seq_len))
    noise = np.random.normal(0, 0.1, (n_seqs, seq_len))
    
    for i in range(1, seq_len):
        x[:, i] = x[:, i-1] * 0.9 + noise[:, i]
    
    y = x.copy()
    
    x_train, y_train = x[:1000], y[:1000]
    x_test, y_test = x[1000:], y[1000:]
    
    return x_train, y_train, x_test, y_test

x_train, y_train, x_test, y_test = generate_data(1200)


def sig(x):
    return 1 / (1 + np.exp(-x))

def sig_deriv(x):
    return x * (1 - x)

def set_w_s(layer_sizes):
    w_s, bs = [], []
    for i in range(len(layer_sizes) - 1):
        input_size, output_size = layer_sizes[i], layer_sizes[i + 1]
        temp = (input_size + 2 * output_size) / 2
        r = np.sqrt(3 / temp)
        wl = np.random.uniform(-r, r, (output_size, input_size))
        ws = np.random.uniform(-r, r, (output_size, output_size))
        b = np.random.uniform(-r, r, (output_size, 1))
        w_s.append((wl, ws))
        bs.append(b)
    return w_s, bs

def new_w_s(w_s, bs, delts, activs, lr):
    seq_len = len(activs)
    n_layers = len(w_s)
    
    for l in range(n_layers):
        wl, ws = w_s[l]
        wl_grad = np.zeros_like(wl)
        ws_grad = np.zeros_like(ws)
        b_grad = np.zeros_like(bs[l])
        
        for s in range(seq_len):
            wl_grad += np.dot(delts[s][l], activs[s][-1].T)
            if s > 0:
                ws_grad += np.dot(delts[s][l], activs[s - 1][l].T)
            b_grad += delts[s][l]
        
        w_s[l] = (wl - lr * wl_grad, ws - lr * ws_grad)
        bs[l] -= lr * b_grad
    
    return w_s, bs

def forward_prop(x, w_s, bs):
    seq_len, n_layers = x.shape[1], len(w_s)
    activs = [{} for _ in range(seq_len)]
    for s in range(seq_len):
        activs[s][-1] = x[:, s].reshape(-1, 1)
        for l in range(n_layers):
            wl, ws = w_s[l]
            b = bs[l]
            if l == 0:
                activs[s][l] = sig(np.dot(wl, activs[s][-1]) + b)
            else:
                if s == 0:
                    activs[s][l] = sig(np.dot(wl, activs[s][l-1]) + b)
                else:
                    activs[s][l] = sig(np.dot(wl, activs[s][l-1]) + np.dot(ws, activs[s-1][l]) + b)
    return activs

def back_prop(activs, w_s, y):
    seq_len = len(activs)
    n_layers = len(w_s)
    delts = []
    for _ in range(seq_len):
        delts.append({})

    
    for s in range(seq_len - 1, -1, -1):
        curr_activ = activs[s][n_layers - 1]
        target = y[:, s].reshape(-1, 1)
        deriv = sig_deriv(curr_activ)
        delts[s][n_layers - 1] = (curr_activ - target) * deriv
        
        for l in range(n_layers - 2, -1, -1):
            wl_nxt, ws_nxt = w_s[l + 1]
            if s < seq_len - 1:
                delt_l_nxt = delts[s + 1][l + 1]
            else:
                delt_l_nxt = np.zeros_like(delts[s][l + 1])
            
            nxt_activ = activs[s][l]
            nxt_delt = delts[s][l + 1]
            deriv = sig_deriv(nxt_activ)
            
            delts[s][l] = (np.dot(wl_nxt.T, nxt_delt) + np.dot(ws_nxt.T, delt_l_nxt)) * deriv
    
    return delts

def train(x_train, y_train, x_test, y_test, epochs, lr):
    layer_sizes = [1, 6, 1]
    w_s, bs = set_w_s(layer_sizes)
    for epoch in range(epochs):
        for i in range(x_train.shape[0]):
            activs = forward_prop(x_train[i].reshape(1, -1), w_s, bs)
            delts = back_prop(activs, w_s, y_train[i].reshape(1, -1))
            w_s, bs = new_w_s(w_s, bs, delts, activs, lr)    
        test_mse = 0
        for i in range(x_test.shape[0]):
            predictions = []
            for s in range(x_test.shape[1]):
                test_input = x_test[i].reshape(1, -1)
                forward_result = forward_prop(test_input, w_s, bs)
                prediction = forward_result[s][len(w_s) - 1]
                predictions.append(prediction)
            test_mse += np.mean(((np.array(predictions).reshape(1, -1))*0.1 - y_test[i].reshape(1, -1)) ** 2 *0.1)
        test_mse /= x_test.shape[0]
        print(f"Epoch {epoch + 1}: Test MSE = {test_mse}")
    return w_s, bs

x_train, y_train, x_test, y_test = generate_data(1200)
train(x_train, y_train, x_test, y_test, epochs = 50, lr = 0.01)
