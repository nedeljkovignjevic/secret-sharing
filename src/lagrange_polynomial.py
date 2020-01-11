import numpy as np


class LagrangePolynomial:

    def __init__(self, X, Y):
        self.n = len(X)
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.temp = []

    def basis(self, x, i):
        L = [(x - self.X[j]) / (self.X[i] - self.X[j]) for j in range(self.n) if j != i]
        return np.prod(L, axis=0) * self.Y[i]

    def interpolate(self, x):
        p = [self.basis(x, i) for i in range(self.n)]
        return np.sum(p, axis=0)

    def interpolate_img(self, x):
        p = [self.basis_img(x, i) for i in range(self.n)]
        return np.sum(p, axis=0)

    def basis_img(self, x, i):
        L = []
        temp = []
        done = False
        skip = 0
        for k in range(len(self.X[i])):
            if self.X[i][k] in self.temp:
                skip += 1
        for j in range(self.n):
            if j != i:
                cont = False
                for k in range(len(self.X[i])):
                    k += skip
                    if k > len(self.X[i]):
                        done = True
                        break
                    self.temp.append(self.X[i][k])
                    for m in range(len(self.X[j])):
                        try:
                            if self.X[j][m] in temp or self.X[j][m] == self.X[i][k]:
                                continue
                            calc = (x-self.X[j][m])/(self.X[i][k]-self.X[j][m])
                            temp.append(self.X[j][m])
                            L.append(calc)
                            cont = True
                            if len(L) == self.n-1:
                                done = True
                                break
                        except ZeroDivisionError:
                            continue
                        if done:
                            break
                        if cont:
                            break
                    if done:
                        break
                    if cont:
                        break
            if done:
                break
        return np.prod(L, axis=0) * self.Y[i]
