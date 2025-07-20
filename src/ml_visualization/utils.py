import numpy as np

def inbounds(a, b, xlim, ylim):
    xlow, xhigh = xlim
    ylow, yhigh = ylim
    ax, ay = a
    bx, by = b
    if (ax > xlow and ax < xhigh) and (bx > xlow and bx < xhigh) \
            and (ay > ylow and ay < yhigh) and (by > ylow and by < yhigh):
        return True
    return False

def add_line(dj_dx, x1, y1, d, ax):
    x = np.linspace(x1 - d, x1 + d, 50)
    y = dj_dx * (x - x1) + y1
    ax.scatter(x1, y1, color='darkblue', s=50)
    ax.plot(x, y, '--', c='darkred', zorder=10, linewidth=1)
    xoff = 30 if x1 == 200 else 10
    ax.annotate(r"$\frac{\partial J}{\partial w}$ =%d" % dj_dx, fontsize=14,
                xy=(x1, y1), xycoords='data',
                xytext=(xoff, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle="->"),
                horizontalalignment='left', verticalalignment='top')