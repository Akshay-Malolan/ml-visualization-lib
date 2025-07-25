import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from ipywidgets import interact
from .cost_functions import compute_cost
from .utils import inbounds, add_line
import os

style_path = os.path.join(os.path.dirname(__file__), 'deeplearning.mplstyle')
plt.style.use(style_path)
n_bin = 5
dlcm = LinearSegmentedColormap.from_list('dl_map', ['#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#8c564b'], N=n_bin)

def plt_house_x(X, y, f_wb=None, ax=None):
    if not ax:
        fig, ax = plt.subplots(1, 1)
    ax.scatter(X, y, marker='x', c='r', label="Actual Value")
    ax.set_title("Housing Prices")
    ax.set_ylabel('Price (in 1000s of dollars)')
    ax.set_xlabel(f'Size (1000 sqft)')
    if f_wb is not None:
        ax.plot(X, f_wb, c='#1f77b4', label="Our Prediction")
    ax.legend()

def mk_cost_lines(x, y, w, b, ax):
    cstr = "cost = (1/m)*("
    ctot = 0
    label = 'cost for point'
    addedbreak = False
    for p in zip(x, y):
        f_wb_p = w * p[0] + b
        c_p = ((f_wb_p - p[1]) ** 2) / 2
        c_p_txt = c_p
        ax.vlines(p[0], p[1], f_wb_p, lw=3, color='#9467bd', ls='dotted', label=label)
        label = ''
        cxy = [p[0], p[1] + (f_wb_p - p[1]) / 2]
        ax.annotate(f'{c_p_txt:0.0f}', xy=cxy, xycoords='data', color='#9467bd',
                    xytext=(5, 0), textcoords='offset points')
        cstr += f"{c_p_txt:0.0f} +"
        if len(cstr) > 38 and not addedbreak:
            cstr += "\n"
            addedbreak = True
        ctot += c_p
    ctot = ctot / len(x)
    cstr = cstr[:-1] + f") = {ctot:0.0f}"
    ax.text(0.15, 0.02, cstr, transform=ax.transAxes, color='#9467bd')

def plt_intuition(x_train, y_train):
    w_range = np.array([200 - 200, 200 + 200])
    tmp_b = 100
    w_array = np.arange(*w_range, 5)
    cost = np.zeros_like(w_array)
    for i in range(len(w_array)):
        tmp_w = w_array[i]
        cost[i] = compute_cost(x_train, y_train, tmp_w, tmp_b)

    @interact(w=(*w_range, 10), continuous_update=False)
    def func(w=150):
        f_wb = np.dot(x_train, w) + tmp_b
        fig, ax = plt.subplots(1, 2, constrained_layout=True, figsize=(8, 4))
        fig.canvas.toolbar_position = 'bottom'
        mk_cost_lines(x_train, y_train, w, tmp_b, ax[0])
        plt_house_x(x_train, y_train, f_wb=f_wb, ax=ax[0])
        ax[1].plot(w_array, cost)
        cur_cost = compute_cost(x_train, y_train, w, tmp_b)
        ax[1].scatter(w, cur_cost, s=100, color='#d62728', zorder=10, label=f"cost at w={w}")
        ax[1].hlines(cur_cost, ax[1].get_xlim()[0], w, lw=4, color='#9467bd', ls='dotted')
        ax[1].vlines(w, ax[1].get_ylim()[0], cur_cost, lw=4, color='#9467bd', ls='dotted')
        ax[1].set_title("Cost vs. w, (b fixed at 100)")
        ax[1].set_ylabel('Cost')
        ax[1].set_xlabel('w')
        ax[1].legend(loc='upper center')
        fig.suptitle(f"Minimize Cost: Current Cost = {cur_cost:0.0f}", fontsize=12)
        plt.show()

def plt_stationary(x_train, y_train):
    fig = plt.figure(figsize=(9, 8))
    fig.set_facecolor('#ffffff')
    fig.canvas.toolbar_position = 'top'
    gs = GridSpec(2, 2, figure=fig)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, :], projection='3d')
    ax = np.array([ax0, ax1, ax2])

    w_range = np.array([200 - 300., 200 + 300])
    b_range = np.array([50 - 300., 50 + 300])
    b_space = np.linspace(*b_range, 100)
    w_space = np.linspace(*w_range, 100)

    tmp_b, tmp_w = np.meshgrid(b_space, w_space)
    z = np.zeros_like(tmp_b)
    for i in range(tmp_w.shape[0]):
        for j in range(tmp_w.shape[1]):
            z[i, j] = compute_cost(x_train, y_train, tmp_w[i][j], tmp_b[i][j])
            if z[i, j] == 0: z[i, j] = 1e-6

    w0 = 200
    b = -100
    f_wb = np.dot(x_train, w0) + b
    mk_cost_lines(x_train, y_train, w0, b, ax[0])
    plt_house_x(x_train, y_train, f_wb=f_wb, ax=ax[0])

    CS = ax[1].contour(tmp_w, tmp_b, np.log(z), levels=12, linewidths=2, alpha=0.7, colors=['#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#8c564b'])
    ax[1].set_title('Cost(w,b)')
    ax[1].set_xlabel('w', fontsize=10)
    ax[1].set_ylabel('b', fontsize=10)
    ax[1].set_xlim(w_range)
    ax[1].set_ylim(b_range)
    cscat = ax[1].scatter(w0, b, s=100, color='#1f77b4', zorder=10, label="cost with \ncurrent w,b")
    chline = ax[1].hlines(b, ax[1].get_xlim()[0], w0, lw=4, color='#9467bd', ls='dotted')
    cvline = ax[1].vlines(w0, ax[1].get_ylim()[0], b, lw=4, color='#9467bd', ls='dotted')
    ax[1].text(0.5, 0.95, "Click to choose w,b", bbox=dict(facecolor='white', ec='black'), fontsize=10,
                transform=ax[1].transAxes, verticalalignment='center', horizontalalignment='center')

    ax[2].plot_surface(tmp_w, tmp_b, z, cmap=dlcm, alpha=0.3, antialiased=True)
    ax[2].plot_wireframe(tmp_w, tmp_b, z, color='k', alpha=0.1)
    plt.xlabel("$w$")
    plt.ylabel("$b$")
    ax[2].zaxis.set_rotate_label(False)
    ax[2].xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax[2].yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax[2].zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax[2].set_zlabel("J(w, b)\n\n", rotation=90)
    plt.title("Cost(w,b) \n [You can rotate this figure]", size=12)
    ax[2].view_init(30, -120)

    return fig, ax, [cscat, chline, cvline]

def plt_divergence(p_hist, J_hist, x_train, y_train):
    x = np.zeros(len(p_hist))
    y = np.zeros(len(p_hist))
    v = np.zeros(len(p_hist))
    for i in range(len(p_hist)):
        x[i] = p_hist[i][0]
        y[i] = p_hist[i][1]
        v[i] = J_hist[i]

    fig = plt.figure(figsize=(12, 5))
    plt.subplots_adjust(wspace=0)
    gs = fig.add_gridspec(1, 5)
    fig.suptitle(f"Cost escalates when learning rate is too large")

    ax = fig.add_subplot(gs[:2])
    fix_b = 100
    w_array = np.arange(-70000, 70000, 1000, dtype="int64")
    cost = np.zeros_like(w_array, float)

    for i in range(len(w_array)):
        tmp_w = w_array[i]
        cost[i] = compute_cost(x_train, y_train, tmp_w, fix_b)

    ax.plot(w_array, cost)
    ax.plot(x, v, c='#9467bd')
    ax.set_title("Cost vs w, b set to 100")
    ax.set_ylabel('Cost')
    ax.set_xlabel('w')
    ax.xaxis.set_major_locator(MaxNLocator(2))

    tmp_b, tmp_w = np.meshgrid(np.arange(-35000, 35000, 500), np.arange(-70000, 70000, 500))
    tmp_b = tmp_b.astype('int64')
    tmp_w = tmp_w.astype('int64')
    z = np.zeros_like(tmp_b, float)
    for i in range(tmp_w.shape[0]):
        for j in range(tmp_w.shape[1]):
            z[i][j] = compute_cost(x_train, y_train, tmp_w[i][j], tmp_b[i][j])

    ax = fig.add_subplot(gs[2:], projection='3d')
    ax.plot_surface(tmp_w, tmp_b, z, alpha=0.3, color='#1f77b4')
    ax.xaxis.set_major_locator(MaxNLocator(2))
    ax.yaxis.set_major_locator(MaxNLocator(2))

    ax.set_xlabel('w', fontsize=16)
    ax.set_ylabel('b', fontsize=16)
    ax.set_zlabel('\ncost', fontsize=16)
    plt.title('Cost vs (b, w)')
    ax.view_init(elev=20., azim=-65)
    ax.plot(x, y, v, c='#9467bd')

    return

def plt_gradients(x_train, y_train, f_compute_cost, f_compute_gradient):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    fix_b = 100
    w_array = np.linspace(-100, 500, 50)
    cost = np.zeros_like(w_array)

    for i in range(len(w_array)):
        tmp_w = w_array[i]
        cost[i] = f_compute_cost(x_train, y_train, tmp_w, fix_b)
    ax[0].plot(w_array, cost, linewidth=1)
    ax[0].set_title("Cost vs w, with gradient; b set to 100")
    ax[0].set_ylabel('Cost')
    ax[0].set_xlabel('w')

    for tmp_w in [100, 200, 300]:
        fix_b = 100
        dj_dw, dj_db = f_compute_gradient(x_train, y_train, tmp_w, fix_b)
        j = f_compute_cost(x_train, y_train, tmp_w, fix_b)
        add_line(dj_dw, tmp_w, j, 30, ax[0])

    tmp_b, tmp_w = np.meshgrid(np.linspace(-200, 200, 10), np.linspace(-100, 600, 10))
    U = np.zeros_like(tmp_w)
    V = np.zeros_like(tmp_b)
    for i in range(tmp_w.shape[0]):
        for j in range(tmp_w.shape[1]):
            U[i][j], V[i][j] = f_compute_gradient(x_train, y_train, tmp_w[i][j], tmp_b[i][j])
    X = tmp_w
    Y = tmp_b
    n = -2
    color_array = np.sqrt(((V - n) / 2) ** 2 + ((U - n) / 2) ** 2)

    ax[1].set_title('Gradient shown in quiver plot')
    Q = ax[1].quiver(X, Y, U, V, color_array, units='width')
    ax[1].quiverkey(Q, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E', coordinates='figure')
    ax[1].set_xlabel("w")
    ax[1].set_ylabel("b")

def soup_bowl():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_rotate_label(False)
    ax.view_init(45, -120)

    w = np.linspace(-20, 20, 100)
    b = np.linspace(-20, 20, 100)
    z = np.zeros((len(w), len(b)))
    j = 0
    for x in w:
        i = 0
        for y in b:
            z[i, j] = x ** 2 + y ** 2
            i += 1
        j += 1

    W, B = np.meshgrid(w, b)
    ax.plot_surface(W, B, z, cmap="Spectral_r", alpha=0.7, antialiased=False)
    ax.plot_wireframe(W, B, z, color='k', alpha=0.1)
    ax.set_xlabel("$w$")
    ax.set_ylabel("$b$")
    ax.set_zlabel("$J(w,b)$", rotation=90)
    ax.set_title("$J(w,b)$\n [You can rotate this figure]", size=15)

    plt.show()

def plt_contour_wgrad(x, y, hist, ax, w_range=[-100, 500, 5], b_range=[-500, 500, 5],
                      contours=[0.1, 50, 1000, 5000, 10000, 25000, 50000],
                      resolution=5, w_final=200, b_final=100, step=10):
    b0, w0 = np.meshgrid(np.arange(*b_range), np.arange(*w_range))
    z = np.zeros_like(b0)
    for i in range(w0.shape[0]):
        for j in range(w0.shape[1]):
            z[i][j] = compute_cost(x, y, w0[i][j], b0[i][j])

    CS = ax.contour(w0, b0, z, contours, linewidths=2,
                     colors=['#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#8c564b'])
    ax.clabel(CS, inline=1, fmt='%1.0f', fontsize=10)
    ax.set_xlabel("w")
    ax.set_ylabel("b")
    ax.set_title('Contour plot of cost J(w,b), vs b,w with path of gradient descent')
    w = w_final
    b = b_final
    ax.hlines(b, ax.get_xlim()[0], w, lw=2, color='#9467bd', ls='dotted')
    ax.vlines(w, ax.get_ylim()[0], b, lw=2, color='#9467bd', ls='dotted')

    base = hist[0]
    for point in hist[0::step]:
        edist = np.sqrt((base[0] - point[0]) ** 2 + (base[1] - point[1]) ** 2)
        if edist > resolution or point == hist[-1]:
            if inbounds(point, base, ax.get_xlim(), ax.get_ylim()):
                plt.annotate('', xy=point, xytext=base, xycoords='data',
                             arrowprops={'arrowstyle': '->', 'color': 'r', 'lw': 3},
                             va='center', ha='center')
            base = point
    return