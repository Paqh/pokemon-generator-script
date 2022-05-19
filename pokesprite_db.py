from __future__ import annotations

import asyncio
from typing import List

import aiohttp

from sprite import Sprite


class PokespriteDB:
    def __init__(self) -> None:
        self.base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
        self.data_endpoint = "data/pokemon.json"
        self.sprite_endpoint = "pokemon-gen8"
        self.colors = ["regular", "shiny"]

    async def __aenter__(self) -> PokespriteDB:
        # can reuse the same session for all requests inside the context manager
        self.http_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err) -> None:
        await self.http_session.close()

    async def fetch_data(self) -> None:
        async with self.http_session.get(
            self.base_url + self.data_endpoint
        ) as response:
            self.pokemon_json = await response.json(content_type="text/plain")

    async def fetch_sprites(self, include_forms: bool) -> List[Sprite]:
        self.sprites: List[Sprite] = []

        sprite_fetch_tasks: List[asyncio.task] = []
        for entry in self.pokemon_json.items():
            pokemon_details = entry[1]
            name = pokemon_details["slug"]["eng"]
            forms: List[str] = []
            if include_forms:
                form_data = pokemon_details["gen-8"]["forms"]
                for form_name, form_info in form_data.items():
                    if "is_alias_of" in form_info:
                        continue
                    forms.append("regular" if form_name == "$" else form_name)
            else:
                forms.append("regular")
            for form in forms:
                for color in self.colors:
                    sprite_name = name
                    if form != "regular":
                        sprite_name += f"-{form}"
                    sprite_url = f"{self.base_url}/{self.sprite_endpoint}/{color}/{sprite_name}.png"
                    sprite = Sprite(sprite_name, color == "shiny", sprite_url)
                    self.sprites.append(sprite)
                    task = asyncio.create_task(sprite.fetch_image(self.http_session))
                    sprite_fetch_tasks.append(task)

        print("Fetching sprites. Might take a few seconds...")
        await asyncio.gather(*sprite_fetch_tasks)
        print("Done fetching sprites")

        return self.sprites
