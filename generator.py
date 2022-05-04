import os
from dataclasses import dataclass
from typing import Iterator

from interfaces import ImageToUnicodeConverter, PokemonDB


@dataclass
class UnicodeSprite:
    name: str
    sprite: str
    is_shiny: bool


class SpritesGenerator:
    def __init__(
        self, db: PokemonDB, unicode_converter: ImageToUnicodeConverter
    ) -> None:
        self.db = db
        self.unicode_converter = unicode_converter

    def generate(self) -> Iterator[UnicodeSprite]:
        for pokemon in self.db:
            for sprite in pokemon.sprites:
                sprite_name = pokemon.ascii_name
                if sprite.form != "regular":
                    sprite_name += f"-{sprite.form}"

                unicode_sprite = self.unicode_converter.convert_image_to_unicode(
                    sprite.image
                )
                yield UnicodeSprite(sprite_name, unicode_sprite, sprite.is_shiny)

    def write_to_file(self, sprite: UnicodeSprite, directory: str):
        print(sprite.name)
        print(sprite.sprite)
        try:
            os.mkdir(directory)
            os.mkdir(os.path.join(directory, "regular"))
            os.mkdir(os.path.join(directory, "shiny"))
        except FileExistsError:
            pass
        if sprite.is_shiny:
            directory = f"{directory}/shiny"
        else:
            directory = f"{directory}/regular"
        with open(f"{directory}/{sprite.name}", "w+") as fout:
            fout.write(sprite.sprite)
