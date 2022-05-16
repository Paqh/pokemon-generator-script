import asyncio
from io import BytesIO
from typing import List

import aiohttp
from PIL import Image

from image import PokemonImage
import unicode_converter as converter

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
            sprite = PokemonImage(sprite)
            sprite.convert_to_rgba()
            sprite.crop_to_content()
            unicode_sprite = converter.convert_image_to_unicode(sprite.image)
            print(unicode_sprite)


async def get_sprite(session: aiohttp.ClientSession, url: str) -> Image.Image:
    async with session.get(url) as response:
        image_data = await response.read()
        image = Image.open(BytesIO(image_data))
        return image


if __name__ == "__main__":
    asyncio.run(main())
