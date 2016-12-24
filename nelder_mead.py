
import numpy as np

class NelderMeadPoint:
    def __init__(self, coordinates, cost):
        self.coordinates = coordinates
        self.cost = cost
    def __lt__(a,b):
        return a.cost < b.cost
    def __gt__(a,b):
        return a.cost > b.cost
    def __str___(self):
        return str(cost) + " " + str(coordinates)


class NelderMead:
    REFLECTION = 0.0
    EXPANSION = 1.0
    CONTRACTION = 2.0

    ALPHA = 1.0
    GAMMA = 2.0
    RHO = 0.5
    THETA = 0.5

    REVERSE = False

    def __init__(self, dimension, points):
        assert isinstance(points, list)
        assert all(isinstance(point, NelderMeadPoint) for point in points)
        assert len(points) == dimension+1 and dimension >= 2

        self.state = self.REFLECTION
        self.dimension = dimension
        self.n_points = dimension+1
        self.centroid = None
        self.expanded = None
        self.reflected = None
        self.contracted = None
        self.points = list(points)
        self.points = sorted(self.points, reverse=self.REVERSE) # SHOULD BE ASCENDING COST!!
        print self

    def __str__(self):
        retval = ""
        if self.state == self.REFLECTION: retval += "REFLECTION\n"
        elif self.state == self.EXPANSION: retval += "EXPANSION\n"
        elif self.state == self.CONTRACTION: retval += "CONTRACTION\n"
        for x in range (0, self.n_points):
            retval += str(self.points[x].cost) + " : " + str(self.points[x].coordinates) + "\n"
        return retval

    def get_next_point(self):
        if self.state == self.REFLECTION:
            self.centroid = np.zeros(self.dimension)
            for point in self.points:
                self.centroid = self.centroid + point.coordinates
            self.centroid = self.centroid*(1.0/(self.n_points))
            reflection = (self.ALPHA+1.0)*self.centroid - self.ALPHA*self.points[self.n_points-1].coordinates
            self.reflected = NelderMeadPoint(reflection, None)
            return self.reflected

        elif self.state == self.EXPANSION:
            expansion = self.centroid + self.GAMMA*(self.reflected.coordinates - self.centroid)
            self.expanded = NelderMeadPoint(expansion, None)
            return self.expanded

        elif self.state == self.CONTRACTION:
            contraction = self.centroid + \
                          self.RHO*(self.points[self.n_points-1].coordinates-self.centroid)
                          
            self.contracted = NelderMeadPoint(contraction, None)
            return self.contracted

    def set_next_point(self, point):
        assert isinstance(point, NelderMeadPoint)

        if self.state == self.REFLECTION:
            self.reflected = point
            if point < self.points[self.n_points-2] and point > self.points[0]:
                self.points[self.n_points-1] = self.reflected
                self.points = sorted(self.points, reverse=self.REVERSE)
            elif point < self.points[0]:
                self.state = self.EXPANSION
            else:
                self.state = self.CONTRACTION

        elif self.state == self.EXPANSION:
            self.expanded = point
            if self.expanded < self.reflected:
                self.points[self.n_points-1] = self.expanded
            else:
                self.points[self.n_points-1] = self.reflected
            self.points = sorted(self.points, reverse=self.REVERSE)
            self.state = self.REFLECTION

        elif self.state == self.CONTRACTION:
            self.contracted = point
            if self.contracted < self.points[self.n_points-1]:
                self.points[self.n_points-1] = self.contracted
                self.points = sorted(self.points, reverse=self.REVERSE)
            else:
                for x in range (0, self.n_points):
                    self.points[x].coordinates = self.points[0].coordinates + \
                                                 self.THETA*(self.points[x].coordinates \
                                                 - self.points[0].coordinates)
            self.points = sorted(self.points, reverse=self.REVERSE)
            self.state = self.REFLECTION


