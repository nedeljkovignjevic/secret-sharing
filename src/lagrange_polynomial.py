import numpy as np


class LagrangePolynomial:

    def __init__(self, X, Y):
        self.n = len(X)
        self.X = np.array(X)
        self.Y = np.array(Y)

    def basis(self, x, i):
        L = [(x - self.X[j]) / (self.X[i] - self.X[j])
             for j in range(self.n) if j != i]
        return np.prod(L, axis=0) * self.Y[i]

    def interpolate(self, x):
        p = [self.basis(x, i) for i in range(self.n)]
        return np.sum(p, axis=0)
