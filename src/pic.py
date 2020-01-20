from PIL import Image
from tkinter import filedialog as fd
from datetime import datetime
from os import path
from math import sqrt
from scheme import Scheme, np


def browse_img():
    while True:
        pname = fd.askopenfilename(
            filetypes=[("Image format", ".tif .tiff .jpg .jpeg .gif .png .bmp .eps .raw .cr2 .nef .orf .sr2")])
        print(pname)
        if pname is not None:
            break
    return pname


def split_parts_list(n, k, prime, img, path_pic):
    h, w, rgb = img.shape  # visina, sirina slike
    name, ext = path.splitext(path_pic)  # putanja slike, odvajanje ekstenzije
    np_lists = np.zeros(shape=(n, h, w, 3))
    # np_lists = [[] for i in range(n)]  # prazne liste, za shares - slike
    shrs = [[[[] for j in range(w)] for i in range(h)],
            [[[] for j in range(w)] for i in range(h)],
            [[[] for j in range(w)] for i in
             range(h)]]  # shares vrijednosti za svaki piksel RGB : shrs[0] je crvena ...
    t1 = datetime.now()  # slika je matrica = niz nizova(redova) piksela
    row_count = 0
    for row in img:  # za svaki red u nizu redova
        new_rows = np.zeros(shape=(n, w, 3))
        # new_rows = [[] for j in range(n)]  # pravimo nove redove tj onoliko redova koliko imamo podjela = n
        pix_count = 0
        for pix in row:
            if len(pix) == 3:
                r, g, b = pix[0], pix[1], pix[2]  # provjera da li je piksel obicni => tri vrijednosti => RGB
            else:  # ili ima 4 vrijednosti, gdje je indikator alfa prva vrijednost
                r, g, b = pix[1], pix[2], pix[3]
            p1, p2, p3 = Scheme(r, n, k, prime), Scheme(g, n, k, prime), Scheme(b, n, k,
                                                                                prime)  # svaku vrijednost boja u pikselu dijelimo SSSA-om na n vrijednosti
            sh1, sh2, sh3 = p1.construct_shares_image(), p2.construct_shares_image(), p3.construct_shares_image()
            for i in range(n):
                new_rows[i][pix_count] = [sh1[i + 1], sh2[i + 1],
                                          sh3[i + 1]]  # u postojece nizove novih slika dodajemo novonastale piksele
            shrs[0][row_count][pix_count] = sh1
            shrs[1][row_count][pix_count] = sh2
            shrs[2][row_count][pix_count] = sh3
            pix_count += 1
        row_count += 1
        v = 0
        for el in range(n):
            np_lists[el][row_count - 1] = new_rows[el]  # dodavanje citavog reda u matrice shares - slika
            v += 1
    i = 0
    for image in np_lists:
        new_img = Image.fromarray(image.astype('uint8'))  # kreiranje shares - slika od novonastalih matrica
        cuvanje = name + "_share" + str(i)
        cuvanje += ".png"
        new_img.save(cuvanje)
        i += 1
    return shrs


def reconstruct_image(images, k, prime, shares):
    imgs = [np.array(Image.open(i)) for i in images]
    row_count = 0
    mat_len, row_len, rgb = imgs[0].shape
    len_imgs = len(imgs)
    matrix = [[] for i in range(mat_len)]
    need_calc = []
    img_dict = {}
    rec_info = {}
    counter = 0
    for row in imgs[0]:
        rec_pix = [[] for i in range(row_len)]
        pix_count = 0
        for pix in row:
            shares_r = []
            shares_g = []
            shares_b = []
            save = False
            num = 0
            for j in range(len_imgs):
                red, green, blue = imgs[j][row_count][pix_count][0], imgs[j][row_count][pix_count][1], \
                                   imgs[j][row_count][pix_count][2]
                if (red == 0 or blue == 0 or green == 0) and ([row_count, pix_count] not in need_calc):
                    need_calc.append([row_count, pix_count])
                    img_dict[counter] = [red, green, blue]
                    save = True
                    num = j
                shares_r.append(red)
                shares_g.append(green)
                shares_b.append(blue)
            if save:
                rec_info[counter] = [num, shares_r, shares_g, shares_b]
                counter += 1
            r, g, b = int(Scheme.reconstruct_secret_img(shares[0][row_count][pix_count], shares_r, k, prime)), \
                      int(Scheme.reconstruct_secret_img(shares[1][row_count][pix_count], shares_g, k, prime)), \
                      int(Scheme.reconstruct_secret_img(shares[2][row_count][pix_count], shares_b, k, prime))
            if r == 256:
                r = 0
            if g == 256:
                g = 0
            if b == 256:
                b = 0
            rec_pix[pix_count] = [r, g, b]
            pix_count += 1
        matrix[row_count] = rec_pix
        row_count += 1
    matrix = np.asarray(matrix)
    for i in range(len(need_calc)):
        [red, green, blue] = img_dict[i]
        [row_count, pix_count] = need_calc[i]
        [r, g, b] = matrix[row_count][pix_count]
        R, G, B = euclidean_dist(i, need_calc[i][0], need_calc[i][1], [r, g, b], [red, green, blue], rec_info, matrix,
                                 shares, k, prime)
        matrix[need_calc[i][0]][need_calc[i][1]] = [R, G, B]
    return matrix


def euclidean_dist(cnt, row, col, pix, sh_pix, rec_info, rec_pic, shares, k, prime):
    h, w = len(rec_pic), len(rec_pic[0])
    dist1 = 0
    dist2 = 0
    R = sh_pix[0]
    G = sh_pix[1]
    B = sh_pix[2]
    if R == 0:
        R = 256
    if G == 0:
        G = 256
    if B == 0:
        B = 256

    adjacent = []
    sec_adj = []
    temp_rec = rec_pic
    [num, shares_r, shares_g, shares_b] = rec_info[cnt]
    shares_r[num], shares_g[num], shares_b[num] = R, G, B
    r, g, b = Scheme.reconstruct_secret_img(shares[0][row][col], shares_r, k, prime), \
              Scheme.reconstruct_secret_img(shares[1][row][col], shares_g, k, prime), \
              Scheme.reconstruct_secret_img(shares[2][row][col], shares_b, k, prime)
    temp_rec[row][col] = [r, g, b]
    R, G, B = r, g, b

    for j in range(row - 1, row + 2):
        for i in range(col - 1, col + 2):
            if 0 <= i < w and 0 <= j < h and not (j == row and i == col):
                adjacent.append(rec_pic[j][i])
                sec_adj.append(temp_rec[j][i])

    for a in range(len(adjacent)):
        cR = pix[0] - adjacent[a][0]
        cR2 = R - sec_adj[a][0]
        cG = pix[1] - adjacent[a][1]
        cG2 = G - sec_adj[a][1]
        cB = pix[2] - adjacent[a][2]
        cB2 = B - sec_adj[a][2]
        uR = (pix[0] + adjacent[a][0]) / 2
        uR2 = (R + sec_adj[a][0]) / 2
        dist1 += sqrt(cR * cR * (2 + uR / 256) + cG * cG * 4 + cB * cB * (2 + (255 - uR) / 256))
        # racunanje reconstruct_secret preko prethodne vrijednosti, tj. ako piksel stavimo na 256 ( prethodno u ekripciji postavljen na 0)
        dist2 += sqrt(cR2 * cR2 * (2 + uR2 / 256) + cG2 * cG2 * 4 + cB2 * cB2 * (2 + (255 - uR2) / 256))

    if dist1 < dist2:
        R, G, B = pix[0], pix[1], pix[2]
    return [R, G, B]
