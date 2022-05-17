import asyncio
from io import BytesIO
from typing import List

import aiohttp
from PIL import Image

import unicode_converter as converter
from image import PokemonImage


async def main() -> None:
    base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
    data_endpoint = "data/pokemon.json"
    colors = ["regular", "shiny"]

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + data_endpoint) as response:
            pokemon_json = await response.json(content_type="text/plain")

    async with aiohttp.ClientSession() as session:
        tasks: List[asyncio.Task] = []
        for entry in pokemon_json.items():
            pokemon_details = entry[1]
            name = pokemon_details["slug"]["eng"]
            form_data = pokemon_details["gen-8"]["forms"]
            forms: List[str] = []
            for form_name, form_info in form_data.items():
                if "is_alias_of" in form_info:
                    continue
                forms.append("regular" if form_name == "$" else form_name)
            for form in forms:
                sprite_name = name
                if form != "regular":
                    sprite_name += f"-{form}"
                    for color in colors:
                        sprite_endpoint = f"pokemon-gen8/{color}/{sprite_name}.png"
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
