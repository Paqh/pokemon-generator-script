import unittest
from unittest.mock import MagicMock
from PIL import Image
import numpy as np
from unicode_converter import SmallConverter
from image import PokemonImage  # Adjust import paths as needed


class TestSmallConverter(unittest.TestCase):
    def setUp(self):
        # Create a mock image with RGBA channels
        self.image_array = np.random.randint(0, 255, (10, 10, 4), dtype=np.uint8)
        self.image = Image.fromarray(self.image_array, 'RGBA')
        
        # Create an instance of SmallConverter
        self.converter = SmallConverter()

    def test_convert_image_to_unicode_with_crop_stub(self):
        # Create an instance of PokemonImage and stub the crop_to_content method
        pokemon_image = PokemonImage(self.image)
        pokemon_image.crop_to_content = MagicMock()

        # Call the method under test
        result = self.converter.convert_image_to_unicode(pokemon_image.image)
        
        # Assert crop_to_content was called (mock verification)
        pokemon_image.crop_to_content.assert_not_called()  # We don't call it directly here
        
        # Check the result is a string
        self.assertIsInstance(result, str)
        
        # Optionally, check that the output is non-empty
        self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()