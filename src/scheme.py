import numpy as np
import matplotlib.pyplot as plt

from random import randint


class Scheme(object):
    """
    Implementation of Shamir's Secret Sharing scheme,
    """

    def __init__(self, s, n, k, p):
        """
        S: secret
        n: total number of shares
        k: recovery threshold
        p: prime, where p > n
        """

        self.s = s
        self.n = n
        self.k = k
        self.p = p

        # Generate random coefficients
        self.coefs = [randint(1, self.s) for i in range(1, k)]

    def construct_shares(self):
        pass

    def reconstruct_secret(self, shares):
        pass
        # if len(shares) < self.k:
        #    raise Exception("Need more participants") ili generisi neku neprepoznatljivu sliku


class LagrangePoly:

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


# -----------------------------------------------------
X = [-9, -4, -1, 7]
Y = [5, 2, -2, 9]

plt.scatter(X, Y, c='k')

lp = LagrangePoly(X, Y)

xx = np.arange(-100, 100) / 10
# plt.plot(xx, lp.basis(xx, 0))
# plt.plot(xx, lp.basis(xx, 1))
# plt.plot(xx, lp.basis(xx, 2))
# plt.plot(xx, lp.basis(xx, 3))
plt.plot(xx, lp.interpolate(xx), linestyle=':')
plt.show()
# -----------------------------------------------------
