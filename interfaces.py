"""Defines standard interfaces for the necessary pokemon data. Using interfaces
so that multiple databases and sprite generation techniques
can potentially be used."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import List

from PIL.Image import Image


class PokemonDB(ABC):
    """An interface for defining any database from which pokemon information
    can be fetched. Must be able to be iterated over to get Pokemon objects"""

    def __iter__(self) -> PokemonDB:
        """Returns a database iterator"""

    def __next__(self) -> Pokemon:
        """Returns the next pokemon in the database"""


class Pokemon(ABC):
    @property
    def name(self) -> str:
        """Get the name of the pokemon. Can include any unicode characters"""

    @property
    def ascii_name(self) -> str:
        """The name of the pokemon limited to the ASCII character set"""

    @property
    def sprites(self) -> List[Sprite]:
        """Get sprites for all forms of the pokemon"""


@dataclass
class Sprite:
    image: Image
    is_shiny: bool
    form: str = "regular"


class ImageToUnicodeConverter(ABC):
    """An interface for some conversion of an RGBA image to a unicode sprite"""

    def convert_image_to_unicode(self, image: Image) -> str:
        """Returns the unicode converted of the image"""
