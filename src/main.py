from pic import *

if __name__ == '__main__':

    # ------------------------------------------------------------
    path = browse_img()
    name, ext = os.path.splitext(path)
    t1 = datetime.now()
    TK = tk.Tk()
    TK.withdraw()
    n = int(input("Number of shares  >>"))
    k = int(input("Number of needed shares for reconstruction (TWO IS MIN)   >>"))
    # # split_parts(5, 3, 255, load_img(path), path)
    # img = mpimg.imread(path)
    # image = Image.open(path)
    pic = Image.open(path)
    matrix = np.array(pic)
    sharesRGB = split_parts_list(n, k, 257, matrix, path)
    print((datetime.now() - t1).seconds)
    unos = sd.askinteger("Number of shares for reconstruction of secret?",
                        "Input in range (" + str(k) + "-" + str(n) + ")",
                        initialvalue=k, minvalue=k, maxvalue=n)
    imgs = []
    for i in range(unos):
        imgs.append(browse_img())
    # print("+++++++++++++++++++++++++++SVE PODJELE++++++++++++++++++++++++++++")
    # imgslst = [mpimg.imread(i) for i in imgs]
    # j = 0
    # for i in imgslst:
    #     print("***********************"+str(j)+". slika**********************")
    #     print(i)
    #     print("**************************************************************")
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print("__________________________________________________________________")
    # print(imgslst[0])
    #reconstruct_image(imgs, n, k, unos)
    # ------------------------------------------------------------

    matrix = reconstruct_image(imgs, k, 257, sharesRGB)
    new_img = Image.fromarray(np.array(matrix), 'RGB')  # kreiranje shares - slika od novonastalih matrica
    new_img.save("SECRET_RESTORED" + ext)

    # ------------------------------------------------------------
    # secret = int(input("Unesite broj kao sifru: "))
    # s = Scheme(secret, 5, 3, 104729)
    # shares = s.construct_shares()
    #
    # inputs = []
    # while True:
    #     pokusaj = input("Unesi deo sifre (za kraj unosa x): ")
    #     if pokusaj == 'x':
    #         break
    #     inputs.append(int(pokusaj))
    #
    # returned_secret = s.reconstruct_secret(shares, inputs, 5, 3)
    # print(returned_secret)
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Summarize shape
    # print(img.shape)
    # a, b, c = img.shape
    # print(a, b, c)
    #
    # Create Pillow image
    # image2 = Image.fromarray(img)
    #
    # lists = (np.empty(shape=(1, b)) for i in range(3))
    # new_rows = [np.empty(shape=(1, 3)) for i in range(3)]
    # print(list(new_rows))
    # print(list(new_rows)[0][1])
    # ------------------------------------------------------------
