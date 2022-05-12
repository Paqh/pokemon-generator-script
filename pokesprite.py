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
        pokemon = PokespritePokemon(name, ascii_name)
        if self.include_forms:
            pokemon.fetch_sprites(forms)
        else:
            pokemon.fetch_sprites()
        return pokemon


class PokespritePokemon(Pokemon):
    def __init__(self, name: str, ascii_name: str) -> None:
        self._name = name
        self._ascii_name = ascii_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def ascii_name(self) -> str:
        return self._ascii_name

    @property
    def sprites(self) -> List[Sprite]:
        return self._sprites

    def fetch_sprites(self, forms=["regular"]):
        sprites_endpoint = (
            "https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8"
        )
        sprites: List[Sprite] = []
        for form in forms:
            sprite_name = self.get_sprite_name(form)
            sprite_types = ["regular", "shiny"]
            for sprite_type in sprite_types:
                url = f"{sprites_endpoint}/{sprite_type}/{sprite_name}.png"
                sprite_image = PokespriteImage(url)
                sprite_image.fetch()
                sprite_image.crop_to_content()
                # necessary as some sprites like unown are greyscale
                sprite_image.convert_to_rgba()
                sprite = Sprite(sprite_image.image, sprite_type == "shiny", form)
                sprites.append(sprite)
        self._sprites = sprites

    def get_sprite_name(self, form: str) -> str:
        sprite_name = self.ascii_name
        if form != "regular":
            sprite_name += f"-{form}"
        return sprite_name


class PokespriteImage:
    def __init__(self, url: str):
        self.url = url

    def fetch(self) -> None:
        response = requests.get(self.url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"couldn't fetch sprite from {self.url}", error)
            exit()
        self.image = Image.open(BytesIO(response.content))

    def crop_to_content(self) -> None:
        """remove padding around the image"""
        # using numpy as this is easier and also faster
        image_array = np.array(self.image)

        alpha_channel = image_array[:, :, 3]
        non_zero_x_values, non_zero_y_values = alpha_channel.nonzero()
        top, left = np.min(non_zero_x_values), np.min(non_zero_y_values)
        bottom, right = np.max(non_zero_x_values), np.max(non_zero_y_values)
        cropped_image = image_array[top : bottom + 1, left : right + 1]

        self.image = Image.fromarray(cropped_image)

    def convert_to_rgba(self) -> None:
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")
