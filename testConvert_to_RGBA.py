import unittest
import asyncio

from unittest.mock import AsyncMock
from PIL import Image
import numpy as np
from image import PokemonImage
from pokesprite_db import PokespriteDB

class TestPokemonImage(unittest.TestCase):
    def setUp(self):
        # Create a mock image (RGB initially) for testing
        self.rgb_image = Image.new("RGB", (100, 100), color="red")
        self.pokemon_image = PokemonImage(self.rgb_image)

    def test_convert_to_rgba(self):
        # Ensure image starts as RGB
        self.assertEqual(self.pokemon_image.image.mode, "RGB")
        
        # Run convert_to_rgba
        self.pokemon_image.convert_to_rgba()
        
        # Check that the image mode is now RGBA
        self.assertEqual(self.pokemon_image.image.mode, "RGBA")

    def test_fetch_sprites_stub(self):
        # Create a PokespriteDB instance and stub the fetch_sprites method
        db = PokespriteDB()
        db.fetch_sprites = AsyncMock(return_value=["sprite1", "sprite2"])

        # Run the mocked method and check results
        result = asyncio.run(db.fetch_sprites(include_forms=True))
        self.assertEqual(result, ["sprite1", "sprite2"])

if __name__ == "__main__":
    unittest.main()
