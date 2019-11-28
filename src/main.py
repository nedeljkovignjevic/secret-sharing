# import matplotlib.image as mpimg
# from PIL import Image
from scheme import Scheme

if __name__ == '__main__':
    secret = int(input("Unesite broj kao sifru: "))
    s = Scheme(secret, 5, 3, 104729)
    shares = s.construct_shares()

    inputs = []
    while True:
        pokusaj = input("Unesi deo sifre (za kraj unosa x): ")
        if pokusaj == 'x':
            break
        inputs.append(int(pokusaj))

    returned_secret = s.reconstruct_secret(shares, inputs)
    print(returned_secret)

    # -------------------------------------
    # Convert image to numpy array
    # img = mpimg.imread('../res/imag.jpg')
    # print(img)
    #
    # # Summarize shape
    # print(img.shape)
    #
    # # Create Pillow image
    # image2 = Image.fromarray(img)
    # -------------------------------------
