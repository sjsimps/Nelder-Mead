# Nelder-Mead

This is an implementation of the Nelder-Mead multidimensional cost minimization algorithm.
It is implemented in Python.

### Example

![](https://github.com/sjsimps/Nelder-Mead/blob/master/example.png)

The above example plot can be generated using [this code](https://github.com/sjsimps/Nelder-Mead/blob/master/example.py),
which takes a cost function and attempts to find local minima.

The plot's mesh indicates the cost function, and scatter plot
points represent the values searched by the algorithm.
The blue points indicate the results from the beginning of the search, and
the red points show the end results.

### Sample Code
```python
import nelder_mead as nm
import numpy as np

# Randomly sample the cost function to provide a starting point for Nelder Mead method
# The number of initial points is equal to the dimensionality + 1
dimension = 2
points = []
for i in range (0, dimension+1):
    x = random.uniform(-2,2)
    y = random.uniform(-2,2)
    z = cost(x,y)
    points.append(nm.Point(np.array([x,y]),z))

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

    print point
```
