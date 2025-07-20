import numpy as np
import matplotlib.pyplot as plt
from src.ml_visualization.plotting import plt_house_x, mk_cost_lines, plt_intuition, plt_stationary, plt_divergence, plt_gradients, soup_bowl, plt_contour_wgrad
from src.ml_visualization.cost_functions import compute_cost

def test_plt_house_x():
    X = np.array([1, 2, 3])
    y = np.array([1, 2, 3])
    plt_house_x(X, y)
    plt.close()

def test_mk_cost_lines():
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])
    w = 1
    b = 0
    fig, ax = plt.subplots()
    mk_cost_lines(x, y, w, b, ax)
    plt.close()

def test_plt_intuition():
    x_train = np.array([1, 2, 3])
    y_train = np.array([1, 2, 3])
    plt_intuition(x_train, y_train)
    plt.close()

def test_plt_stationary():
    x_train = np.array([1, 2, 3])
    y_train = np.array([1, 2, 3])
    plt_stationary(x_train, y_train)
    plt.close()

def test_plt_divergence():
    p_hist = [(1, 1), (2, 2), (3, 3)]
    J_hist = [1, 2, 3]
    x_train = np.array([1, 2, 3])
    y_train = np.array([1, 2, 3])
    plt_divergence(p_hist, J_hist, x_train, y_train)
    plt.close()

def test_plt_gradients():
    x_train = np.array([1, 2, 3])
    y_train = np.array([1, 2, 3])
    f_compute_cost = compute_cost
    f_compute_gradient = lambda x, y, w, b: (1, 1)  # Dummy gradient function
    plt_gradients(x_train, y_train, f_compute_cost, f_compute_gradient)
    plt.close()

def test_soup_bowl():
    soup_bowl()

def test_plt_contour_wgrad():
    x = np.array([1, 2, 3])
    y = np.array([1, 2, 3])
    hist = [(1, 1), (2, 2), (3, 3)]
    fig, ax = plt.subplots()
    plt_contour_wgrad(x, y, hist, ax)
    plt.close()