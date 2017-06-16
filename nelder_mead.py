
class Point:
    def __init__(self, coordinates, cost):
        self.coordinates = coordinates
        self.cost = cost
    def __lt__(a,b):
        return a.cost < b.cost
    def __gt__(a,b):
        return a.cost > b.cost
    def __str__(self):
        return "Cost: " + str(self.cost) + " / Coords: " + str(self.coordinates)
    def __repr__(self):
        return self.__str__()

class VectorOps:
    @staticmethod
    def vecadd(X,Y):
        assert (len(X) == len(Y)), "error : vectors of unequal length"
        return [x + y for x,y in zip(X,Y)]

    @staticmethod
    def veckadd(X,k):
        ret = []
        for x in X:
            ret.append(x+k)
        return ret

    @staticmethod
    def veckmul(X,k):
        ret = []
        for x in X:
            ret.append(x*k)
        return ret

    @staticmethod
    def vecsub(X, Y):
        assert (len(X) == len(Y)), "error : vectors of unequal length"
        return [x - y for x,y in zip(X,Y)]

class NelderMead:
    REFLECTION = 0
    EXPANSION = 1
    CONTRACTION = 2
    REVERSE = False

    def __init__(self, dimension, points,
                 alpha=1.0, gamma=2.0, rho=0.5, theta=0.5):
        assert isinstance(points, list), "Points must be a list of points"
        assert all(isinstance(point, Point) for point in points), "Points must be Nelder-Mead points"
        assert all(len(point.coordinates) == dimension for point in points), "Points must have appropriate dimensionality"
        assert (len(points) == dimension+1 and dimension >= 1), "Number of initial points must equal dimensionality + 1"

        # Reflection, Expansion, Contraction, and Shrink coefficients:
        self.ALPHA = alpha
        self.GAMMA = gamma
        self.RHO = rho
        self.THETA = theta

        self.state = NelderMead.REFLECTION
        self.dimension = dimension
        self.n_points = dimension+1
        self.centroid = None
        self.expanded = None
        self.reflected = None
        self.contracted = None
        self.points = list(points)
        self.points = sorted(self.points, reverse=NelderMead.REVERSE) # SHOULD BE ASCENDING COST!!

    def __str__(self):
        retval = ""
        if self.state == NelderMead.REFLECTION: retval += "REFLECTION\n"
        elif self.state == NelderMead.EXPANSION: retval += "EXPANSION\n"
        elif self.state == NelderMead.CONTRACTION: retval += "CONTRACTION\n"
        for x in range (0, self.n_points):
            retval += str(self.points[x])+"\n"
        return retval

    def get_next_point(self):
        VO=VectorOps
        if self.state == NelderMead.REFLECTION:
            self.centroid = [0.0]*self.dimension
            for point in self.points:
                self.centroid = VO.vecadd(self.centroid, point.coordinates)
            self.centroid = VO.veckmul(self.centroid,(1.0/(self.n_points)))
            reflection = VO.vecadd(VO.veckmul(self.centroid,(self.ALPHA+1.0)),
                                          VO.veckmul(self.points[self.n_points-1].coordinates,-self.ALPHA))
            self.reflected = Point(reflection, None)
            return self.reflected

        elif self.state == NelderMead.EXPANSION:
            expansion = VO.vecadd(self.centroid,
                                         VO.veckmul(VO.vecsub(self.reflected.coordinates, self.centroid),
                                                    self.GAMMA))
            self.expanded = Point(expansion, None)
            return self.expanded

        elif self.state == NelderMead.CONTRACTION:
            contraction = VO.vecadd(self.centroid,
                                    VO.veckmul(VO.vecsub(self.points[self.n_points-1].coordinates,self.centroid),
                                               self.RHO))

            self.contracted = Point(contraction, None)
            return self.contracted

    def set_next_point(self, point):
        assert isinstance(point, Point)

        VO=VectorOps
        if self.state == NelderMead.REFLECTION:
            self.reflected = point
            if point < self.points[self.n_points-2] and point > self.points[0]:
                self.points[self.n_points-1] = self.reflected
                self.points = sorted(self.points, reverse=NelderMead.REVERSE)
            elif point < self.points[0]:
                self.state = NelderMead.EXPANSION
            else:
                self.state = NelderMead.CONTRACTION

        elif self.state == NelderMead.EXPANSION:
            self.expanded = point
            if self.expanded < self.reflected:
                self.points[self.n_points-1] = self.expanded
            else:
                self.points[self.n_points-1] = self.reflected
            self.points = sorted(self.points, reverse=NelderMead.REVERSE)
            self.state = NelderMead.REFLECTION

        elif self.state == NelderMead.CONTRACTION:
            self.contracted = point
            if self.contracted < self.points[self.n_points-1]:
                self.points[self.n_points-1] = self.contracted
                self.points = sorted(self.points, reverse=NelderMead.REVERSE)
            else:
                for x in range (0, self.n_points):
                    self.points[x].coordinates = VO.vecadd(self.points[0].coordinates, \
                                                        VO.veckmul(
                                                            VO.vecsub(self.points[x].coordinates, self.points[0].coordinates),
                                                            self.THETA
                                                            )
                                                        )
            self.points = sorted(self.points, reverse=NelderMead.REVERSE)
            self.state = NelderMead.REFLECTION


