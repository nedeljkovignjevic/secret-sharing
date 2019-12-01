import numpy as np
from random import randint

from lagrange_polynomial import LagrangePolynomial


class Scheme(object):
    """
    Implementation of Shamir's Secret Sharing scheme,
    """
    def __init__(self, s, n, k, p):
        """
        s: secret
        n: total number of shares
        k: recovery threshold
        p: prime, where p > n
        """
        self.s = s
        self.n = n
        self.k = k
        self.p = p
        # Generate random coefficients
        self.coefs = list(dict.fromkeys([randint(1, 65000) for i in range(1, k)]))

    def construct_shares(self):
        self.coefs.append(self.s)
        values = np.polyval(self.coefs, [i for i in range(1, self.n + 1)]) % self.p
        shares = {i: values[i - 1] for i in range(1, self.n + 1)}
        # print(shares)
        return shares

    @staticmethod
    def reconstruct_secret(shares: dict, inputs: list, k, p):
        if len(shares) < k:
            raise Exception("More shares needed")

        for el in inputs:
            if el not in shares.values():
                raise Exception("Inadequate share")

        indeksi = []
        for i in range(len(inputs)):
            indeksi.append(int(list(shares.keys())[list(shares.values()).index(inputs[i])]))

        # print(indeksi)
        # print([shares[ind] for ind in indeksi])
        lp = LagrangePolynomial(indeksi, [shares[ind] for ind in indeksi])

        # plt.scatter(indeksi, [shares[ind] for ind in indeksi], c='k')
        # plt.plot(indeksi, lp.interpolate(indeksi) % self.p, linestyle=':')

        secret = lp.interpolate(0) % p
        # plt.show()
        return secret
