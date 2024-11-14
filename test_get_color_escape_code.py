import unittest
from ansi import get_color_escape_code  # Replace with the actual module name

class TestGetColorEscapeCode(unittest.TestCase):

    # def test_foreground_color(self):
    #     # Test foreground color with RGB values (255, 0, 0)
    #     r, g, b = 255, 0, 0
    #     expected_output = "\x1b[38;2;255;0;0m"
    #     result = get_color_escape_code(r, g, b)
    #     print(repr(result))
    #     self.assertEqual(result, expected_output)

    # def test_background_color(self):
    #     # Test background color with RGB values (0, 255, 0)
    #     r, g, b = 0, 255, 0
    #     expected_output = "\x1b[48;2;0;255;0m"
    #     result = get_color_escape_code(r, g, b, background=True)
    #     print(repr(result))
    #     self.assertEqual(result, expected_output)

    # def test_black_foreground(self):
    #     # Test foreground color with RGB values (0, 0, 0) for black
    #     r, g, b = 0, 0, 0
    #     expected_output = "\x1b[38;2;0;0;0m"
    #     result = get_color_escape_code(r, g, b)
    #     print(repr(result))
    #     self.assertEqual(result, expected_output)

    def test_white_background(self):
        # Test background color with RGB values (255, 255, 255) for white
        r, g, b = 255, 255, 255
        expected_output = "\x1b[48;2;255;255;255m"
        result = get_color_escape_code(r, g, b, background=True)
        print(repr(result))
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
