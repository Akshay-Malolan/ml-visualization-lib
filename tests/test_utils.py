import pytest
import numpy as np
from src.ml_visualization.utils import inbounds, add_line

def test_inbounds():
    assert inbounds((5, 5), (10, 10), (0, 15), (0, 15) ) == True
    assert inbounds((5, 5), (10, 10), (0, 5), (0, 15) ) == False
    assert inbounds((5, 5), (10, 10), (0, 15), (0, 5) ) == False
    assert inbounds((5, 5), (10, 10), (5, 15), (5, 15) ) == True

def test_add_line():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    x1, y1 = 200, 100
    dj_dx = 2
    d = 30

    add_line(dj_dx, x1, y1, d, ax)

    # Check if the line is added correctly
    assert len(ax.lines) == 1  # One line should be added
    line = ax.lines[0]
    assert line.get_xdata()[0] == x1 - d
    assert line.get_xdata()[-1] == x1 + d
    assert line.get_ydata()[0] == dj_dx * (x1 - d - x1) + y1
    assert line.get_ydata()[-1] == dj_dx * (x1 + d - x1) + y1

    plt.close(fig)  # Close the figure after testing