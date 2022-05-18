from io import BytesIO

import aiohttp
from PIL import Image


class Sprite:
    def __init__(self, pokemon: str, is_shiny: bool, form: str = "regular"):
        self._pokemon = pokemon
        self._form = form
        self._is_shiny = is_shiny

    def __repr__(self) -> str:
        return f"Sprite(pokemon = {self._pokemon}, is_shiny = {self.is_shiny}, form = {self._form})"

    @property
    def name(self) -> str:
        self._name = self._pokemon
        if self._form != "regular":
            self._name += f"-{self._form}"
        return self._name

    @property
    def is_shiny(self) -> bool:
        return self._is_shiny

    @property
    def image(self) -> Image.Image:
        return self._image

    async def fetch_image(self, http_session: aiohttp.ClientSession) -> None:
        base_url = "https://raw.githubusercontent.com/msikma/pokesprite/master/"
        color = "shiny" if self.is_shiny else "regular"
        sprite_endpoint = f"pokemon-gen8/{color}/{self.name}.png"

        async with http_session.get(base_url + sprite_endpoint) as response:
            image_data = await response.read()
            image = Image.open(BytesIO(image_data))
            self._image = image
