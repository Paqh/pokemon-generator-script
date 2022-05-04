import numpy as np
from PIL.Image import Image

from interfaces import ImageToUnicodeConverter


class SmallSizeConverter(ImageToUnicodeConverter):
    """Generattes sprites where one unicode character represents two image
    pixels vertically and one horizontally"""

    def convert_image_to_unicode(self, image: Image) -> str:
        # maps one pixel to half a character
        upper_block = "▀"
        lower_block = "▄"
        empty_block = " "

        unicode_sprite = ""

        image_array = np.array(image)

        height, width, _ = image_array.shape
        background_reset_code = "\033[0m"
        for i in range(0, height - 1, 2):
            for j in range(width):
                upper_pixel = image_array[i, j]
                lower_pixel = image_array[i + 1, j]
                # use foreground and background colors along with half blocks
                # to map two pixels to one character
                if upper_pixel[3] == 0 and lower_pixel[3] == 0:
                    unicode_sprite += empty_block
                elif upper_pixel[3] == 0:
                    r, g, b = lower_pixel[:3]
                    escape_code = self.get_color_escape_code(r, g, b)
                    unicode_sprite += escape_code
                    unicode_sprite += lower_block
                elif lower_pixel[3] == 0:
                    r, g, b = upper_pixel[:3]
                    escape_code = self.get_color_escape_code(r, g, b)
                    unicode_sprite += escape_code
                    unicode_sprite += upper_block
                else:
                    r_f, g_f, b_f = upper_pixel[:3]
                    r_b, g_b, b_b = lower_pixel[:3]
                    foreground_escape = self.get_color_escape_code(r_f, g_f, b_f)
                    background_escape = self.get_color_escape_code(
                        r_b, g_b, b_b, background=True
                    )
                    unicode_sprite += foreground_escape
                    unicode_sprite += background_escape
                    unicode_sprite += upper_block
                    unicode_sprite += background_reset_code
            unicode_sprite += "\n"

        return unicode_sprite

    @staticmethod
    def get_color_escape_code(r, g, b, background=False) -> str:
        """
        Given rgb values give the escape sequence for printing out the
        color to the terminal
        """
        return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


class LargeSizeConverter(ImageToUnicodeConverter):
    """Generates sprites where one image pixel is mapped to two unicode
    characters in width and one in height"""

    def convert_image_to_unicode(self, image: Image) -> str:
        # using two characters wide and one character high to maintain a near
        # 1 aspect ratio
        solid_block = "██"
        empty_block = "  "

        unicode_sprite = ""

        image_array = np.array(image)

        height, width, _ = image_array.shape
        prev_escape_code = ""
        for i in range(height):
            for j in range(width):
                alpha = image_array[i, j, 3]
                if alpha == 0:
                    unicode_sprite += empty_block
                    continue
                r, g, b = image_array[i, j, :3]
                escape_code = self.get_color_escape_code(r, g, b, background=False)
                # only add an escape code if the color changes
                if prev_escape_code != escape_code:
                    unicode_sprite += escape_code
                unicode_sprite += solid_block
                prev_escape_code = escape_code
            unicode_sprite += "\n"

        return unicode_sprite

    @staticmethod
    def get_color_escape_code(r, g, b, background=False) -> str:
        """
        Given rgb values give the escape sequence for printing out the
        color to the terminal
        """
        return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)
