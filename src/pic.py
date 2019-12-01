from PIL import Image
import matplotlib.image as mpimg

from tkinter import filedialog as fd
from datetime import datetime
import random
import functools
import os

from scheme import Scheme, np

_PRIME = 2 ** 127 - 1
_RINT = functools.partial(random.SystemRandom().randint, 0)


def browse_img():
    while True:
        pname = fd.askopenfilename(
            filetypes=[("Image format", ".tif .tiff .jpg .jpeg .gif .png .bmp .eps .raw .cr2 .nef .orf .sr2")])
        print(pname)
        if pname is not None:
            break
    return pname


def split_parts_list(n, k, prime, img, path):
    h, w, rgb = img.shape
    name, ext = os.path.splitext(path)
    np_lists = [[] for i in range(n)]
    t1 = datetime.now()
    for row in img:
        new_rows = [[] for j in range(n)]
        r, g, b = row[0][0], row[0][1], row[0][2]
        if len(row[0]) > 3:
            r, g, b = row[0][1], row[0][2], row[0][3]
        for pix in row:
            p1, p2, p3 = Scheme(r, n, k, prime), Scheme(g, n, k, prime), Scheme(b, n, k, prime)
            sh1, sh2, sh3 = p1.construct_shares(), p2.construct_shares(), p3.construct_shares()
            for i in range(n):
                new_rows[i].append([sh1[i + 1], sh2[i + 1], sh3[i + 1]])

        v = 0
        for el in range(n):
            np_lists[el].append(new_rows[el])
            v += 1
    i = 0
    for image in np_lists:
        new_img = Image.fromarray(np.array(image), 'RGB')
        new_img.save(name + "_share" + str(i) + ext)
        i += 1


def reconstruct_image(images, n, k, unos):
    imgs = [mpimg.imread(i) for i in images]
    row_count = 0
    for row in imgs[0]:
        rec_pix = [[] for i in range(n)]
        pix_count = 0
        for pix in row:
            shares_r = {}
            shares_g = {}
            shares_b = {}
            for j in range(unos):
                shares_r[j] = imgs[j][row_count][pix_count][0]
                shares_g[j] = imgs[j][row_count][pix_count][1]
                shares_b[j] = imgs[j][row_count][pix_count][2]
            [r, g, b] = [rec_secret(shares_r)]


def rec_secret(shares):
    pass

# -------------------------------------------------------------------------------------------------------------
# sa numpy array
# def split_parts(n, k, prime, img, path):
#     h, w, rgb = img.shape
#     name, ext = os.path.splitext(path)
#     np_lists = [np.empty(shape=(h, w, 3)) for i in range(n)]
#     t1 = datetime.now()
#     for row in img:
#         new_rows = [np.empty(shape=(1, w, 3)) for i in range(n)]
#         j = 0
#         for pix in row:
#             r, g, b = pix[0], pix[1], pix[2]
#             if len(pix) > 3:
#                 r, g, b = pix[1], pix[2], pix[3]
#             p1, p2, p3 = Scheme(r, n, k, prime), Scheme(g, n, k, prime), Scheme(b, n, k, prime)
#             sh1, sh2, sh3 = p1.construct_shares(), p2.construct_shares(), p3.construct_shares()
#             for i in range(n):
#                 new_rows[i][0][j] = [sh1[i+1], sh2[i+1], sh3[i+1]]
#             j += 1
#         v = 0
#         for el in range(n):
#             np_lists[el][v] = new_rows[el][0]
#             v += 1
#     print(datetime.now() - t1)
#     i = 0
#     for image in np_lists:
#         new_img = Image.fromarray(image, 'RGB')
#         new_img.save(name + "_share" + str(i) + ext)
#         i += 1
# -------------------------------------------------------------------------------------------------------------
