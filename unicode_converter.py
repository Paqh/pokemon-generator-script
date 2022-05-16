import numpy as np
from PIL.Image import Image

import ansi


def convert_image_to_unicode(image: Image) -> str:
    # maps one pixel to half a character
    upper_block = "▀"
    lower_block = "▄"
    empty_block = " "

    unicode_sprite = ""

    image_array = np.array(image)
    height, width, channels = image_array.shape

    # as we're mapping two pixels to one character, we need an even number
    # of pixels as height. So adding an empty row at the bottom for odd heights
    if height % 2:
        padded_array = np.zeros((height + 1, width, channels)).astype(np.uint8)
        padded_array[:height, :, :] = image_array
        height, width, channels = padded_array.shape
        image_array = padded_array

    background_reset_code = "\033[0m"
    for i in range(0, height, 2):
        for j in range(width):
            upper_pixel = image_array[i, j]
            lower_pixel = image_array[i + 1, j]
            # use foreground and background colors along with half blocks
            # to map two pixels to one character
            if upper_pixel[3] == 0 and lower_pixel[3] == 0:
                unicode_sprite += empty_block
            elif upper_pixel[3] == 0:
                r, g, b = lower_pixel[:3]
                escape_code = ansi.get_color_escape_code(r, g, b)
                unicode_sprite += escape_code
                unicode_sprite += lower_block
            elif lower_pixel[3] == 0:
                r, g, b = upper_pixel[:3]
                escape_code = ansi.get_color_escape_code(r, g, b)
                unicode_sprite += escape_code
                unicode_sprite += upper_block
            else:
                r_f, g_f, b_f = upper_pixel[:3]
                r_b, g_b, b_b = lower_pixel[:3]
                foreground_escape = ansi.get_color_escape_code(r_f, g_f, b_f)
                background_escape = ansi.get_color_escape_code(
                    r_b, g_b, b_b, background=True
                )
                unicode_sprite += foreground_escape
                unicode_sprite += background_escape
                unicode_sprite += upper_block
                unicode_sprite += background_reset_code
        unicode_sprite += "\n"

    return unicode_sprite
