#!/usr/bin/env python3
import argparse
import asyncio
import os
from typing import List

import aiohttp

import unicode_converter as converter
from image import PokemonImage
from sprite import Sprite


async def main() -> None:
    args = parse_cli_arguments()
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
            forms: List[str] = []
            if args.include_forms:
                form_data = pokemon_details["gen-8"]["forms"]
                for form_name, form_info in form_data.items():
                    if "is_alias_of" in form_info:
                        continue
                    forms.append("regular" if form_name == "$" else form_name)
            else:
                forms.append("regular")
            for form in forms:
                for color in colors:
                    sprite = Sprite(name, color == "shiny", form)
                    sprites.append(sprite)
                    sprite_fetch_tasks.append(
                        asyncio.create_task(sprite.fetch_image(session))
                    )

        print("Fetching sprites. Might take a few seconds...")
        await asyncio.gather(*sprite_fetch_tasks)
        for sprite in sprites:
            image = PokemonImage(sprite.image)
            image.convert_to_rgba()
            image.crop_to_content()
            small_converter = converter.SmallConverter()
            large_converter = converter.LargeConverter()
            small_unicode_sprite = small_converter.convert_image_to_unicode(image.image)
            large_unicode_sprite = large_converter.convert_image_to_unicode(image.image)
            color_dir = "shiny" if sprite.is_shiny else "regular"
            write_to_file(sprite.name, f"large/{color_dir}", large_unicode_sprite)
            write_to_file(sprite.name, f"small/{color_dir}", small_unicode_sprite)
            if not args.silent:
                print(large_unicode_sprite)
                print(small_unicode_sprite)


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--include-forms",
        help="generate the different forms of the pokemon. Regional, megas, gmax etc.",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--silent",
        help="don't print out sprites as they are being generated",
        action="store_true",
    )
    return parser.parse_args()


def write_to_file(filename: str, directory: str, text: str) -> None:
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/{filename}", "w+") as fout:
        fout.write(text)


if __name__ == "__main__":
    asyncio.run(main())
