from random import randint
from lagrange_polynomial import LagrangePolynomial, np

spec_chars = {
    0: 'Ç', 1: 'ü', 2: 'é', 3: 'â', 4: 'ä', 5: 'à', 6: 'å', 7: 'ç', 8: 'ê', 9: 'ë', 10: 'è', 11: 'ï', 12: 'î',
    13: 'ì', 14: 'æ', 15: 'Æ', 16: 'ô', 17: 'ö', 18: 'ò', 19: 'û', 20: 'ù', 21: 'ÿ', 22: '¢', 23: '£', 24: '¥',
    25: 'Ñ', 26: 'ƒ', 27: 'á', 28: 'í', 29: 'ó', 30: 'ú', 31: 'ñ'
}

spec_chars_key = {
    'Ç': 0, 'ü': 1, 'é': 2, 'â': 3, 'ä': 4, 'à': 5, 'å': 6, 'ç': 7, 'ê': 8, 'ë': 9, 'è': 10, 'ï': 11, 'î': 12,
    'ì': 13, 'æ': 14, 'Æ': 15, 'ô': 16, 'ö': 17, 'ò': 18, 'û': 19, 'ù': 20, 'ÿ': 21, '¢': 22, '£': 23, '¥': 24,
    'Ñ': 25, 'ƒ': 26, 'á': 27, 'í': 28, 'ó': 29, 'ú': 30, 'ñ': 31
}

def printToFile(fileWrite, data):
    with open(fileWrite, 'w') as outfile:
        outfile.write('# Array shape: {0}\n'.format(data.shape))

        for data_slice in data:
            np.savetxt(outfile, data_slice, fmt='%-10.2f')
            outfile.write('# New slice\n')


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
        return shares

    def construct_shares_image(self):
        self.coefs.append(self.s)
        values = np.polyval(self.coefs, [i for i in range(1, self.n + 1)]) % self.p
        shares = {}
        for i in range(1, self.n + 1):
            if int(values[i - 1]) != 256:
                if int(values[i - 1]) == 0:
                    shares[self.n + 1] = 256
                shares[i] = int(values[i - 1])
            else:
                shares[i] = 0
                shares[self.n + 1] = 256

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

        lp = LagrangePolynomial(indeksi, [shares[ind] for ind in indeksi])
        secret = lp.interpolate(0) % p

        return secret

    @staticmethod
    def reconstruct_secret_img(shares: dict, inputs: list, k, p):
        if len(shares) < k:
            raise Exception("More shares needed")

        for el in inputs:
            if el not in shares.values():
                raise Exception("Inadequate share")

        indeksi = []
        vals = np.array(list(shares.values()))
        for i in range(len(inputs)):
            search = inputs[i]
            if inputs[i] == 256:
                search = 0
            ii = np.where(vals == search)[0]
            lii = [list(shares.keys())[i] for i in ii]
            indeksi.append(lii)

        lp = LagrangePolynomial(indeksi, [shares[ind[0]] for ind in indeksi])

        secret = lp.interpolate_img(0) % p
        return secret
