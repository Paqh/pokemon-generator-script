import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
import numpy as np
from image import PokemonImage

class TestPokemonImage(unittest.TestCase):
    @patch.object(PokemonImage, 'convert_to_rgba')
    
    def test_crop_to_content(self, mock_convert_to_rgba):
        # Stub convert_to_rgba to simulate an RGBA image
        mock_convert_to_rgba.return_value = None

        # Create a mock image with alpha channel
        mock_image_data = np.zeros((10, 10, 4), dtype=np.uint8)
        # Set some pixels in the center to be non-transparent
        mock_image_data[2:8, 2:8, 3] = 255
        
        mock_image = Image.fromarray(mock_image_data)

        # Instantiate PokemonImage with the mock image
        pokemon_image = PokemonImage(mock_image)

        # Perform the crop_to_content test
        pokemon_image.crop_to_content()

        # Get the modified image array
        result_array = np.array(pokemon_image.image)
        
        # Check if the resulting image has been cropped correctly
        self.assertEqual(result_array.shape[0], 6)  # Height should be 6 pixels (8 - 2)
        self.assertEqual(result_array.shape[1], 6)  # Width should be 6 pixels (8 - 2)

        # Ensure that the stubbed method (convert_to_rgba) was called
        mock_convert_to_rgba.assert_called_once()

if __name__ == '__main__':
    unittest.main()
