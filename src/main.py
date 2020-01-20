from pic import browse_img, datetime, Image, np, split_parts_list, reconstruct_image
from os import path
from tkinter import Tk
from tkinter import simpledialog as sd

if __name__ == '__main__':

    path_img = browse_img()
    name, ext = path.splitext(path_img)
    t1 = datetime.now()
    TK = Tk()
    TK.withdraw()
    n = int(input("Number of shares  >>"))
    k = int(input("Number of needed shares for reconstruction (TWO IS MIN)   >>"))
    pic = Image.open(path_img)
    matrix = np.array(pic, np.int32)
    sharesRGB = split_parts_list(n, k, 257, matrix, path_img)
    print((datetime.now() - t1).seconds)
    unos = sd.askinteger("Number of shares for reconstruction of secret?",
                         "Input in range (" + str(k) + "-" + str(n) + ")",
                         initialvalue=k, minvalue=k, maxvalue=n)
    imgs = []
    for i in range(unos):
        imgs.append(browse_img())

    matrix = reconstruct_image(imgs, k, 257, sharesRGB)
    new_img = Image.fromarray(matrix.astype('uint8'), 'RGB')
    new_img.save("SECRET_RESTORED" + ext)
