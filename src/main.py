import matplotlib.image as mpimg
from PIL import Image


if __name__ == '__main__':
    # Convert image to numpy array
    img = mpimg.imread('../res/imag.jpg')
    print(img)

    # Summarize shape
    print(img.shape)

    # Create Pillow image
    image2 = Image.fromarray(img)
