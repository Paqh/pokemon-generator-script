import asyncio
from typing import List

import aiohttp

import unicode_converter as converter
from image import PokemonImage
from sprite import Sprite


async def main() -> None:
    base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
    data_endpoint = "data/pokemon.json"
    colors = ["regular", "shiny"]

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + data_endpoint) as response:
            pokemon_json = await response.json(content_type="text/plain")

    async with aiohttp.ClientSession() as session:
        sprite_fetch_tasks: List[asyncio.task] = []
        sprites: List[Sprite] = []
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
                for color in colors:
                    sprite = Sprite(name, color == "shiny", form)
                    sprites.append(sprite)
                    sprite_fetch_tasks.append(asyncio.create_task(sprite.fetch_image(session)))

        print("Fetching sprites. Might take a few seconds...")
        await asyncio.gather(*sprite_fetch_tasks)
        for sprite in sprites:
            image = PokemonImage(sprite.image)
            image.convert_to_rgba()
            image.crop_to_content()
            unicode_sprite = converter.convert_image_to_unicode(image.image)
            print(unicode_sprite)


if __name__ == "__main__":
    asyncio.run(main())
