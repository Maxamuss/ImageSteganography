from PIL import Image

class HiddenImage:
    """
    Class used for hidding or retriving hidden data from an image.
    Each pixel in the image can store 6 bits of data. 4 pixels are grouped in
    order to store 3 characters. Pixels are grouped horizontally, starting at
    the top left of the image.
    """
    def __init__(self, image_name):
        image = Image.open('1.jpg')
        pixels = image.load()

        self.image = image
        self.raw_pixel_store = pixels
        self.image_name = image_name
        self.x_size = image.size[0]
        self.y_size = image.size[1]

    def get_character_capacity(self):
        """
        Return the number of characters that can be stored in the image.
        """
        pixels = (self.x_size * self.y_size) - 60
        characters = pixels * 0.75
        return characters

    def has_data_hidden(self):
        """
        Returns True if image may contain a hidden data. False otherwise.
        If an image has had data hidden in it already, the last 60 pixels of the
        image contain meta data. If not meta data exists then the image has no
        data hidden in it.
        """
        # get the last 60 pixels of the image
        if self.x_size >= 60:
            pixels_rgb = []
            for i in range(self.x_size-1, self.x_size-61, -1):
                pixels.append(self.raw_pixel_store[i, self.y_size-1])
        else: #TODO: if image width less than 60 px
            return False

        pixels_binary = []
        for pixel in pixels_rgb:
            pixels_binary.append()

        return False

    def hide_data(self, data, fit_all=True):
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
        # check data will fit into the image (60 px reserved for meta data)
        data_size = len(data)
        size_available = self.get_character_capacity()

        if fit_all and data_size > size_available:
            return False

        # convert the data to a string of binary
        binary_data = self.data_to_binary(data)

        # split the binary into groups of 6 digits and add data to image
        x = 0
        y = 0
        while (binary_data != ''):
            temp_data = binary_data[:6]
            binary_data = binary_data[6:]
            self.set_pixel_value(x, y, temp_data)

            if x == self.x_size:
                x = 0
                y += 1
            else:
                x += 1

        self.image.save('test.jpg', 'JPEG')
        # add the meta data to the end
        # self.add_meta_data(self)

    def data_to_binary(self, data):
        """
        Converts the given string of data to a binary. Each character in the
        string is converted to binary and added to a list. A string is returned.
        """
        # convert the string to ascii values then binary
        data_ascii = [ord(c) for c in data]
        data_binary = [format(a, '08b') for a in data_ascii]

        binary_string = ''
        for byte in data_binary:
            binary_string += byte

        return binary_string

    def rgb_to_binary(self, rgb_list):
        """
        Returns the a list of the rgb values of the pixel in binary given a
        tuple of rgb colours.
        """
        colours_binary = []
        for colour in rgb_list:
            colours_binary.append(format(colour, '08b'))

        return colours_binary

    def set_pixel_value(self, x, y, data):
        """
        Change the binary rgb values of a pixel to store the given data.
        """
        pixel = self.raw_pixel_store[x, y]
        pixel_binary = self.rgb_to_binary(pixel)

        r = pixel_binary[0]
        g = pixel_binary[1]
        b = pixel_binary[2]
        # change the last 2 digits of the binary number and convert to an int
        r_adj = int((r[:6] + data[:2]), 2)
        g_adj = int((g[:6] + data[2:4]), 2)
        b_adj = int((b[:6] + data[4:6]), 2)
        # set the next rgb value for the pixel
        self.raw_pixel_store[x, y] = (r_adj, g_adj, b_adj)

    def add_meta_data(self):
        """
        Add some infomation to the image about the data that has been hidden
        inside of it. Uses the last 60 pixels of the image, starting at the
        bottom right pixel and moving horizontally left.
        """
        # for i in range(self.x_size, ):
        pass

    def retrive_hidden_data(self):
        """
        Retrive the hidden data from the image
        """
        pass

image = HiddenImage('1.jpg')
# image.hide_data("My name is Max Wilkinson.")
image.get_character_capacity()

# print(pixel.to_binary())
# im = Image.open(
# pix = im.load(im)

# pixel = Pixel(0, 0, pix[0, 0])


# print(im.size)  # Get the width and hight of the image for iterating over
# print(pix[0,0])  # Get the RGBA Value of the a pixel of an image
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png
