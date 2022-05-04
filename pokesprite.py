"""
Pokemon sprites from
https://msikma.github.io/pokesprite/
"""
from __future__ import annotations

from io import BytesIO
from typing import List

import numpy as np
import requests
from PIL import Image

from interfaces import Pokemon, PokemonDB, Sprite


class PokespriteDB(PokemonDB):
    def __init__(self) -> None:
        self.base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
        self.data_endpoint = "data/pokemon.json"
        self.data = requests.get(self.base_url + self.data_endpoint).json()
        # set to false if you only need regular forms
        self.include_forms = True

    def __iter__(self) -> PokespriteDB:
        self.pokemon_data = iter(self.data.items())
        return self

    def __next__(self) -> Pokemon:
        next_pokemon_data = next(self.pokemon_data)[1]
        name = next_pokemon_data["name"]["eng"]
        ascii_name = next_pokemon_data["slug"]["eng"]
        form_data = next_pokemon_data["gen-8"]["forms"]
        forms: List[str] = []
        for form_name, form_info in form_data.items():
            # Avoid duplicate items with aliases. One main name will do
            if "is_alias_of" in form_info:
                continue
            # Replacing ambiguos name from API with a more human readable name
            if form_name == "$":
                forms.append("regular")
            else:
                forms.append(form_name)

        sprites: List[Sprite] = []
        for form_name in forms:
            if not self.include_forms and form_name != "regular":
                continue
            sprite_name = ascii_name
            if form_name != "regular":
                sprite_name += f"-{form_name}"

            normal = Sprite(
                PokespriteSprite(sprite_name, shiny=False).get_image(), False, form_name
            )
            shiny = Sprite(
                PokespriteSprite(sprite_name, shiny=True).get_image(), True, form_name
            )
            sprites.append(normal)
            sprites.append(shiny)

        return Pokemon(name, ascii_name, sprites)


class PokespriteSprite:
    def __init__(self, sprite_name: str, shiny: bool) -> None:
        self.name = sprite_name

        self.base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
        self.sprites_endpoint = self.base_url + "pokemon-gen8"
        if shiny:
            self.endpoint = f"{self.sprites_endpoint}/shiny/{sprite_name}.png"
        else:
            self.endpoint = f"{self.sprites_endpoint}/regular/{sprite_name}.png"

    def fetch_sprite(self) -> None:
        response = requests.get(self.endpoint)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"couldn't fetch sprite for {self.name}", error)
            exit()

        self.image = Image.open(BytesIO(response.content))

    def crop_to_content(self) -> None:
        """remove padding around the image"""
        # using numpy as this is easier and also faster
        image_array = np.array(self.image)

        alpha_channel = image_array[:, :, 3]
        x_values, y_values = alpha_channel.nonzero()
        top, left = np.min(x_values), np.min(y_values)
        bottom, right = np.max(x_values), np.max(y_values)
        cropped_image = image_array[top:bottom, left:right]

        self.image = Image.fromarray(cropped_image)

    def convert_to_rgba(self) -> None:
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")

    def get_image(self) -> Image.Image:
        self.fetch_sprite()
        self.convert_to_rgba()
        self.crop_to_content()
        return self.image
