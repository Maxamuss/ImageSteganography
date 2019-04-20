from PIL import Image

class HiddenImage:
    """
    Class used for hidding or retriving hidden data from an image.
    """
    def __init__(self, image_name):
        image = Image.open('1.jpg')
        pixels = image.load()

        self.image_name = image_name
        self.image = image
        self.raw_pixel_store = pixels
        self.x_size = image.size[0]
        self.y_size = image.size[1]
        self.hidden_data = self.has_data_hidden()

    def has_data_hidden(self):
        """
        Returns True if image may contain a hidden data. False otherwise.
        If an image has had data hidden in it already, the last 60 pixels of the
        image contain meta data. If not meta data exists then the image has no
        data hidden in it.
        """
        # get the last 60 pixels of the image
        pixels_rgb = []
        for i in range(self.x_size-1, self.x_size-61, -1):
            pixels.append(self.raw_pixel_store[i, self.y_size-1])

        pixels_binary = []
        for pixel in pixels_rgb:
            pixels_binary.append()

        return False

    def add_hidden_data(self, data, fit_all=True):
        """
        Hide data in the image. By default, if the data to be hidden will not
        fit into the image, none of the data is hidden and False returned. If
        fit_all is set to True, then as much of the data will be hidden as
        possible, starting from the start.
        60 pixels are reserved at the end of the image for meta data. Data will
        be added horizontally to the left and start from the right on the row
        above if space on that row has run out. This will include the size of
        the data hiddena and a key for future retrivals of the hidden data.
        Due to the meta data, the image must be greater than 60 pixels. Much
        larger if meaningful amounts of data want to be hidden.
        """
        data = str(data)
        # check data will fit into the image (60 px reserved for meta data)
        image_pixels = self.x - self.y - 60
        size_available = int(image_pixels / 4)
        data_size = len(data)

        if fit_all and data_size > available_pixels:
            return False

        binary_data = self.data_to_binary(data)

    def data_to_binary(self, data):
        """
        Converts the given string of data to a binary. Each character in the
        string is converted to binary and added to a list, to be returned
        """
        # for char in data:
        pass

    def rgb_to_binary(self, rgb):
        """
        Convery
        """

    def retrive_hidden_data(self):
        """
        If the
        """
        possible_hidden_data = True if self.has_data_hidden else False

        # if no meta data in the image, ask user if they want to scrape all of
        # data from the image.
        if not possible_hidden_data:
            check = input("The image given may not contain any hidden data. Do you"
                  + "want to check the image anyway? [y/n]: ")
            if check != 'y':
                return None


class Pixel:
    """
    Class used for storing data of individual pixels from an image. Only created
    for pixels that are needed for the steganography.
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

    def get_next(self):
        """
        Returns a Pixel object of the pixel to the right of self. If no pixel is
        to the right, return the Pixel object of the first pixel on the next row
        down. None will be returned if this is the last pixel in the image.
        """
        pass

    def get_prev(self):
        """
        Returns a Pixel object of the pixel to the left of self. If no pixel is
        to the left, return the Pixel object of the last pixel on the row above.
        None will be returned uf this is the first pixel in the image.
        """
        pass

image = HiddenImage('1.jpg')

# print(pixel.to_binary())
# im = Image.open(
# pix = im.load(im)

# pixel = Pixel(0, 0, pix[0, 0])


# print(im.size)  # Get the width and hight of the image for iterating over
# print(pix[0,0])  # Get the RGBA Value of the a pixel of an image
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
