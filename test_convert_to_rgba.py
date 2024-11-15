import unittest
from PIL import Image
from image import PokemonImage

class TestConvertToRGBA(unittest.TestCase):

    def test_convert_to_rgba_from_rgb(self):
        initial_image = Image.new("RGB", (10, 10), color="red")
        self.obj = PokemonImage(initial_image)
        # Ensure the initial image is in RGB mode
        self.assertEqual(self.obj.image.mode, "RGB")
        print("Before: " + self.obj.image.mode)
        
        self.obj.convert_to_rgba()
        print("After: " + self.obj.image.mode)
        # Check if the image mode has changed to RGBA
        self.assertEqual(self.obj._image.mode, "RGBA")

    def test_no_conversion_needed(self):
        initial_image = Image.new("RGBA", (10, 10), color=(255, 0, 0, 255))
        self.obj = PokemonImage(initial_image)
        # Ensure the initial image is in RGBA mode
        self.assertEqual(self.obj.image.mode, "RGBA")
        print("Before: " + self.obj.image.mode)
        
        self.obj.convert_to_rgba()
        print("After: " + self.obj.image.mode)
        # Check if the image remains in RGBA mode
        self.assertEqual(self.obj.image.mode, "RGBA")

if __name__ == "__main__":
    unittest.main()
