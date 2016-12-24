
import math
import nelder_mead
import random
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def cost(x,y):
    return (pow(x,4) + pow(y,4) - 4*x*y)

#plt.hold(True)
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-2, 2, 0.25)
Y = np.arange(-2, 2, 0.25)
X, Y = np.meshgrid(X, Y)
Z = cost(X,Y)

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False, alpha=0.5)
ax.set_zlim(-2.0, 25.0)

fig.colorbar(surf, shrink=0.5, aspect=5)

points = []
for i in range (0, 3):
    x = random.uniform(-2,2)
    y = random.uniform(-2,2)
    z = cost(x,y)
    ax.scatter(x,y,z)
    points.append(nelder_mead.NelderMeadPoint(np.array([x,y]),z))

model = nelder_mead.NelderMead(2,points)

color = "b"
for i in range (0, 30):
    point = model.get_next_point()
    point.cost = cost(point.coordinates[0],point.coordinates[1])
    model.set_next_point(point)
    if (i > 5): color = "r"
    else: color = "b"
    ax.scatter(point.coordinates[0],point.coordinates[1],point.cost, c=color)

plt.show()
