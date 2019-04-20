from PIL import Image

class PixelStore:
    """
    Class used for storing pixels that make up an image.
    """
    def __init__(self, size):
        self.x_size = size[0]
        self.y_size = size[1]

    def add_pixel(self, pixel):
        pass

    def get_pixel(self, x, y):
        pass

class Pixel:
    """
    Class used for storing data of individual pixels from an image.
    """
    def __init__(self, x, y, rgb):
        """
        Set the x and y co-ordinates of the pixel in the image as well as its
        rgb colour value.
        """
        self.x = x
        self.y = y
        self.rgb = rgb

    def to_binary(self):
        """
        Convert the pixel's rgb values to binary. Returns a tuple of the binary
        values for the red, green and blue values in binary.
        """
        r = self.rgb[0]
        g = self.rgb[1]
        b = self.rgb[2]

        r_binary = int(format(r, 'b'))
        g_binary = int(format(g, 'b'))
        b_binary = int(format(b, 'b'))

        rgb_binary = (r_binary, g_binary, b_binary)

        return rgb_binary

    def next_right(self):
        pass

    def get_left(self):
        pass

    def get_above(self):
        pass

    def get_below(self):
        pass

im = Image.open('1.jpg')
pix = im.load(im)

pixel = Pixel(0, 0, pix[0, 0])

print(pixel.to_binary())

# print(im.size)  # Get the width and hight of the image for iterating over
# print(pix[0,0])  # Get the RGBA Value of the a pixel of an image
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
