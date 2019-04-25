import sys

from PIL import Image

class EncryptImage:
    """
    Class used for hidding or retriving hidden data from an image.
    Each pixel in the image can store 6 bits of data. 4 pixels are grouped in
    order to store 3 characters. Pixels are grouped horizontally, starting at
    the top left of the image.
    """
    def __init__(self, input_image, output_image=None):
        image = Image.open(input_image)
        pixels = image.load()

        self.image = image
        self.raw_pixel_store = pixels
        self.input_image = input_image
        self.output_image = output_image
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
        Returns the number of pixels the data is stored in if image contains
        meta data about data hidden within it. None otherwise.
        If an image has had data hidden in it already, the last 60 pixels of the
        image contain meta data. If not meta data exists then the image has no
        data hidden in it.
        """
        # get the last 60 pixels of the image
        if self.x_size >= 60:
            pixels_rgb = []
            for i in range(self.x_size-1, self.x_size-61, -1):
                pixels_rgb.append(self.raw_pixel_store[i, self.y_size-1])
        else: #TODO: if image width less than 60 px
            return False

        binary = ''
        for pixel in pixels_rgb:
            for byte in self.rgb_to_binary(pixel):
                binary += byte[6:]

        # check for meta data in the image
        meta_data = self.binary_to_data(binary)
        if meta_data[:9] == '$$$$$$$$$':
            n = 9
            length = ''
            while (meta_data[n:n+1] != '$'):
                length += meta_data[n:n+1]
                n += 1
            return length
        return

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

        # split the binary 6 bits and add data to image
        x = 0
        y = 0
        count = 0
        tenth = int(data_size / 10)
        milestones = [tenth, tenth*2, tenth*3, tenth*4, tenth*5, tenth*6,
                      tenth*7, tenth*8, tenth*9]

        while (binary_data != ''):
            temp_data = binary_data[:6]
            binary_data = binary_data[6:]
            self.set_pixel_value(x, y, temp_data)

            count += 1
            if x == (self.x_size - 1):
                x = 0
                y += 1
            else:
                x += 1

            # log to the console the progress made
            if count in milestones:
                print(str(milestones.index(count)+1) + "0% complete")

        # add the meta data to the end of the image
        pixels_used = y * self.x_size + x
        self.add_meta_data(pixels_used)

        # save the image
        self.image.save(self.output_image)
        return True

    def add_meta_data(self, pixels_used):
        """
        Add some infomation to the image about the data that has been hidden
        inside of it. Uses the last 60 pixels of the image, starting at the
        bottom right pixel and moving horizontally left. Not all of the 60
        pixels may be used.
        """
        meta_string = '$$$$$$$$$' + str(pixels_used) + '$$$$$$$$$'
        meta_binary = self.data_to_binary(meta_string)

        # split the binary into 6 bits and add data to end of image
        x = self.x_size - 1
        y = self.y_size - 1
        while (meta_binary != ''):
            temp_binary = meta_binary[:6]
            meta_binary = meta_binary[6:]
            self.set_pixel_value(x, y, temp_binary)

            if x == 0:
                x = self.x_size - 1
                y -= 1
            else:
                x -= 1

    def retrive_data(self):
        """
        Retrive the hidden data from the image
        """
        # get the num of pixels the data is in. If None, no meta data in image
        meta_data = self.has_data_hidden()
        if meta_data is None:
            return

        # get the pixels the data is hidden in
        pixels = []
        n = x = y = 0
        while (n != int(meta_data)):
            pixels.append(self.raw_pixel_store[x, y])

            n += 1
            if x == (self.x_size - 1):
                x = 0
                y += 1
            else:
                x += 1

        # get the last 2 bits from the rgb values and convert to a string
        binary = ''
        for pixel in pixels:
            for byte in self.rgb_to_binary(pixel):
                binary += byte[6:]

        return self.binary_to_data(binary)

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

    def binary_to_data(self, binary):
        """
        Convert and return binary into a string of data.
        """
        data = ''
        while binary != '':
            temp = binary[:8]
            if len(temp) < 8:
                break
            binary = binary[8:]
            ascii = int(temp, 2)
            data += chr(ascii)

        return data

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

if len(sys.argv) == 4:
    image = EncryptImage(sys.argv[2], sys.argv[3])
    print("\nThe image can encrypt " + str(int(image.get_character_capacity())) + " characters of text.")
    with open(sys.argv[1], "r") as file:
        data = file.read()#.replace('\n', ' ')
    print("The data you are encrypting is " + str(len(data)) + " characters of text.")
    print("\n...")
    encryption_successful = image.hide_data(data)
    if encryption_successful:
        print("\nData successfully encrypted into image.")
    else:
        print("\nData not successfully encrypted into image. Text file too large.")
elif len(sys.argv) == 2:
    image = EncryptImage(sys.argv[1])
    print(image.retrive_data())
else:
    print("Incorrect number of arguements passed.")
    print("> python test.py <text file to encrypt> <input image> <output image>")

# image2 = EncryptImage('test.png')
# print(image2.retrive_data())
