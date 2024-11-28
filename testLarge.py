import unittest
from unittest.mock import MagicMock
import numpy as np
from PIL import Image
from unicode_converter import LargeConverter
from image import PokemonImage 

class TestLargeConverter(unittest.TestCase):

    def setUp(self):
        # Create a mock image with alpha channel (RGBA format)
        self.image_data = np.array([
            [[255, 0, 0, 255], [0, 255, 0, 255]],  # Red and Green
            [[0, 0, 255, 255], [255, 255, 0, 0]],  # Blue and transparent
        ], dtype=np.uint8)
        self.mock_image = Image.fromarray(self.image_data, 'RGBA')
        self.large_converter = LargeConverter()
        
        # Mock PokemonImage and crop_to_content
        self.mock_pokemon_image = PokemonImage(self.mock_image)
        self.mock_pokemon_image.crop_to_content = MagicMock()

    def test_convert_image_to_unicode(self):
        # Test conversion without needing to call crop_to_content
        result = self.large_converter.convert_image_to_unicode(self.mock_pokemon_image.image)
        
        # Ensure it returns a non-empty string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        # Print the result for visualization (optional)
        print(result)

if __name__ == '__main__':
    unittest.main()