import numpy as np

def compute_cost(x, y, w, b):
    m = len(y)  # number of training examples
    cost = (1 / (2 * m)) * np.sum(np.square(np.dot(x, w) + b - y))
    return cost