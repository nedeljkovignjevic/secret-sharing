from image_processing import browse_img, datetime, Image, np, split_parts_list, reconstruct_image
from os import path
from tkinter import Tk
from tkinter import simpledialog as sd
from scheme import Scheme

if __name__ == '__main__':

    # Text encryption
    # TODO: popraviti \x - LicmMa metodom: kod construct ako je ispod 32 dodaj 32 i sacuvaj share
    # TODO:  kod reconstruct za  32 < x < 63 naci originalno konstruisani znak
    # ------------------------------------------------------------------
    k = 2
    secret = input("Unesite sifru: ")
    text = [ord(c) for c in secret]

    shares, lista = [], []
    for el in text:
        s = Scheme(el, 4, k, 127)
        shares = s.construct_shares()
        lista.append(shares)

    print(lista)
    for dic in lista:
        dict_variable = {key: chr(value) for (key, value) in dic.items()}
        print(dict_variable)

    glavna_lista = []
    while True:
        word = input("Input word: (x for exit): ")
        if word == "x": break
        rec = [int(ord(el)) for el in word]
        glavna_lista.append(rec)

    print(glavna_lista)
    reconstructed_secret = ""
    b = 0
    for dic in lista:
        reconstructed_secret += chr(int(Scheme.reconstruct_secret(dic, glavna_lista[b], k, 127)))
        b += 1

    print(f'**** RECONSTRUTED **** \n{reconstructed_secret}\n')
    # ------------------------------------------------------------------

    # Image encryption
    # ------------------------------------------------------------------
    # path_img = browse_img()
    # _, ext = path.splitext(path_img)
    #
    # t1 = datetime.now()
    # TK = Tk()
    # TK.withdraw()
    # n = int(input("Number of shares  >>"))
    # k = int(input("Number of needed shares for reconstruction (TWO IS MIN)   >>"))
    #
    # pic = Image.open(path_img)
    # matrix = np.array(pic, np.int32)
    # sharesRGB = split_parts_list(n, k, 257, matrix, path_img)
    # print((datetime.now() - t1).seconds)
    #
    # unos = sd.askinteger("Number of shares for reconstruction of secret?",
    #                      "Input in range (" + str(k) + "-" + str(n) + ")",
    #                      initialvalue=k, minvalue=k, maxvalue=n)
    # imgs = []
    # for i in range(unos):
    #     imgs.append(browse_img())
    #
    # matrix = reconstruct_image(imgs, k, 257, sharesRGB)
    # new_img = Image.fromarray(matrix.astype('uint8'), 'RGB')
    # new_img.save("../res/SECRET" + ext)
    # ------------------------------------------------------------------
