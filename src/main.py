import matplotlib.image as mpimg
from PIL import Image
import numpy as np
from scheme import Scheme

if __name__ == '__main__':
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

    #-------------------------------------
    #Convert image to numpy array
    img = mpimg.imread('../res/imag.jpg')
    print(img)

    # # Summarize shape
    # # print(img.shape)
    # a, b, c = img.shape
    # print(a, b, c)
    #
    # # Create Pillow image
    # image2 = Image.fromarray(img)
    #
    # # lists = (np.empty(shape=(1, b)) for i in range(3))
    # new_rows = [np.empty(shape=(1, 3)) for i in range(3)]
    # print(list(new_rows))
    # print(list(new_rows)[0][1])
    #-------------------------------------
