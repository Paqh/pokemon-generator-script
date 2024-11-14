#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
from typing import List

import unicode_converter as converter
from image import PokemonImage
from pokemon import Pokemon
from pokesprite_db import PokespriteDB


async def main() -> None:
    args = parse_cli_arguments() #1
    async with PokespriteDB() as db:
        pokemons: List[Pokemon] = [] 
        await db.fetch_data() #2
        for pokemon in db:
            pokemons.append(pokemon)
        generate_pokemon_json(pokemons) #3

        sprites = await db.fetch_sprites(args.include_forms) #4
        for sprite in sprites:
            image = PokemonImage(sprite.image) #5
            image.convert_to_rgba() #6
            image.crop_to_content() #7
            small_converter = converter.SmallConverter() #8
            large_converter = converter.LargeConverter() #9
            small_unicode_sprite = small_converter.convert_image_to_unicode(image.image) #10
            large_unicode_sprite = large_converter.convert_image_to_unicode(image.image) #11
            color_dir = "shiny" if sprite.is_shiny else "regular"
            write_to_file(sprite.name, f"large/{color_dir}", large_unicode_sprite)
            write_to_file(sprite.name, f"small/{color_dir}", small_unicode_sprite)
            if not args.silent:
                print(sprite.name)
                print(large_unicode_sprite)
                print(small_unicode_sprite)


def generate_pokemon_json(pokemons: List[Pokemon]) -> None:
    print("Generating pokemon JSON...")
    pokemon_json = []
    for pokemon in pokemons:
        pokemon_entry = {"name": pokemon.name, "forms": pokemon.forms}
        pokemon_json.append(pokemon_entry)
    with open("pokemon.json", "w+") as fout:
        json.dump(pokemon_json, fout, indent=2)


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
