
import math
import nelder_mead as nm
import random
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

### COST FUNCTION

def cost(x,y):
    return (pow(x,4) + pow(y,4) - 4*x*y)

### PLOT CONFIGURATION

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

### NELDER-MEAD EXAMPLE

# Randomly sample the cost function to provide a starting point for Nelder Mead method
# The number of initial points is equal to the dimensionality + 1
dimension = 2
points = []
for i in range (0, 3):
    x = random.uniform(-2,2)
    y = random.uniform(-2,2)
    z = cost(x,y)
    points.append(nm.Point(np.array([x,y]),z))
    ax.scatter(x,y,z)

# Initializing the Nelder-Mead model
model = nm.NelderMead(dimension,points)

# Iteratively minimizing cost
for i in range (0, 30):
    # 1: Fetch a suggested next point from the model
    point = model.get_next_point()

    # 2 : Compute the result cost of the proposed point
    point.cost = cost(point.coordinates[0],point.coordinates[1])

    # 3 : Return the point with updated cost back to the model
    model.set_next_point(point)

    color = "b"
    if (i > 5): color = "r"
    ax.scatter(point.coordinates[0],point.coordinates[1],point.cost, c=color)

plt.show()
