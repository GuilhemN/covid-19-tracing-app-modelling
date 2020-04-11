import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from random import *

style.use('fivethirtyeight')

def init_viz():
    fig = plt.figure()
    ax = fig.add_subplot()
    xs = []
    y_D = []
    y_MS = []
    y_MAS = []
    y_S = []
    return (fig, ax, xs, y_D, y_MS, y_MAS, y_S)


def animate(i):
    (fig, ax, xs, y_D, y_MS, y_MAS, y_S) = data
    xs.append(len(xs))
    y_D.append(2*random())      # ajoute le nombre de decedes
    y_MS.append(2*random())     # ajoute le nombre de malade symptomatiques
    y_MAS.append(2*random())    # ajoute le nombre de malade asymptomatiques
    y_S.append(2*random())      # ajoute le nombre de personnes saines
    ax.clear()
    def plot_with_label(ys, label):
        line, = ax.plot(xs, ys)
        line.set_label(label)
    plot_with_label(y_D, "Morts")
    plot_with_label(y_MAS, "Malades asymp.")
    plot_with_label(y_MS, "Malades symp.")
    plot_with_label(y_S, "Sains")
    ax.legend(loc='upper left')

data = init_viz()
fig = data[0]
while True:
    animate(0)
    fig.show()
    plt.pause(0.05)
# ani = animation.FuncAnimation(fig, animate, interval=100)
# plt.show()