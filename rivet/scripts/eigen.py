from numpy import *
from pylab import *

def norm_evects(evect_x, freq):
    """normalize and scale eigenvectors"""

    set_printoptions(precision=3)
    evectt = transpose(evect_x)

    for i in range(len(freq)):
        evectt[i] = evectt[i] / evectt[i][0]
    return evectt

def plot_modes(shape):
    """plot three mode shapes"""

    shapes =  insert(shape, 3, 0, axis = 1)

    m3 = shapes[2] * .15 + 3
    m2 = shapes[1] * .3 + 2
    m1 = shapes[0] * .3 + 1

    y = array([3, 2, 1, 0])
    plot(m1,y)
    plot(m2,y)
    plot(m3,y)
    xlim(.5, 4.)
    xlabel('mode')
    ylabel('levels')
    grid(True)
    xticks([1,2,3])
    yticks([0,1,2,3])
    savefig("mode_shapes.png")
    return "mode shapes plotted"
