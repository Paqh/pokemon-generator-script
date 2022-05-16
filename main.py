import asyncio
from io import BytesIO
from typing import List

import aiohttp
import numpy as np
from PIL import Image


async def main() -> None:
    base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
    data_endpoint = "data/pokemon.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + data_endpoint) as response:
            pokemon_json = await response.json(content_type="text/plain")

    async with aiohttp.ClientSession() as session:
        tasks: List[asyncio.Task] = []
        for entry in pokemon_json.items():
            pokemon_details = entry[1]
            # name = pokemon_details["name"]["eng"]
            ascii_name = pokemon_details["slug"]["eng"]
            sprite_endpoint = f"pokemon-gen8/regular/{ascii_name}.png"
            tasks.append(
                asyncio.create_task(get_sprite(session, base_url + sprite_endpoint))
            )

        sprites = await asyncio.gather(*tasks)
        for sprite in sprites:
            rgba_sprite = convert_to_rgba(sprite)
            cropped_sprite = crop_to_content(rgba_sprite)
            unicode_sprite = convert_image_to_unicode(cropped_sprite)
            print(unicode_sprite)


def convert_to_rgba(image: Image.Image) -> Image.Image:
    if image.mode != "RGBA":
        rgba_image = image.convert("RGBA")
        return rgba_image
    else:
        return image


def crop_to_content(image: Image.Image) -> Image.Image:
    """remove padding around the image"""
    # using numpy as this is easier and also faster
    image_array = np.array(image)

    alpha_channel = image_array[:, :, 3]
    non_zero_x_values, non_zero_y_values = alpha_channel.nonzero()
    top, left = np.min(non_zero_x_values), np.min(non_zero_y_values)
    bottom, right = np.max(non_zero_x_values), np.max(non_zero_y_values)
    cropped_image = image_array[top : bottom + 1, left : right + 1]

    return Image.fromarray(cropped_image)


async def get_sprite(session: aiohttp.ClientSession, url: str) -> Image.Image:
    async with session.get(url) as response:
        image_data = await response.read()
        image = Image.open(BytesIO(image_data))
        return image


def convert_image_to_unicode(image: Image.Image) -> str:
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
                escape_code = get_color_escape_code(r, g, b)
                unicode_sprite += escape_code
                unicode_sprite += lower_block
            elif lower_pixel[3] == 0:
                r, g, b = upper_pixel[:3]
                escape_code = get_color_escape_code(r, g, b)
                unicode_sprite += escape_code
                unicode_sprite += upper_block
            else:
                r_f, g_f, b_f = upper_pixel[:3]
                r_b, g_b, b_b = lower_pixel[:3]
                foreground_escape = get_color_escape_code(r_f, g_f, b_f)
                background_escape = get_color_escape_code(
                    r_b, g_b, b_b, background=True
                )
                unicode_sprite += foreground_escape
                unicode_sprite += background_escape
                unicode_sprite += upper_block
                unicode_sprite += background_reset_code
        unicode_sprite += "\n"

    return unicode_sprite


def get_color_escape_code(r, g, b, background=False) -> str:
    """
    Given rgb values give the escape sequence for printing out the
    color to the terminal
    """
    return "\033[{};2;{};{};{}m".format(48 if background else 38, r, g, b)


if __name__ == "__main__":
    asyncio.run(main())
