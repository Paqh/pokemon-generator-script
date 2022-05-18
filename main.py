#!/usr/bin/env python3
import argparse
import asyncio
import os

import unicode_converter as converter
from image import PokemonImage
from pokesprite_db import PokespriteDB


async def main() -> None:
    args = parse_cli_arguments()
    async with PokespriteDB() as db:
        await db.fetch_data()
        sprites = await db.fetch_sprites(args.include_forms)
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
                print(sprite.name)
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
