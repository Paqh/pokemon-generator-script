"""
Pokemon sprites from
https://msikma.github.io/pokesprite/
"""
from __future__ import annotations

import requests

from interfaces import Pokemon, PokemonDB


class PokespriteDB(PokemonDB):
    def __init__(self) -> None:
        self.base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
        self.data_endpoint = "data/pokemon.json"
        self.sprites_endpoint = "pokemon-gen8/"

        self.data = requests.get(self.base_url + self.data_endpoint).json()

    def __iter__(self) -> PokespriteDB:
        self.pokemon_data = iter(self.data.items())
        return self

    def __next__(self) -> Pokemon:
        next_pokemon_data = next(self.pokemon_data)[1]
        name = next_pokemon_data["name"]["eng"]
        ascii_name = next_pokemon_data["slug"]["eng"]
        return Pokemon(name, ascii_name)
