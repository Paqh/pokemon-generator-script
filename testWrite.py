import unittest
from unittest.mock import patch, mock_open
from main import write_to_file

class TestWriteToFile(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")  # Mocking os.makedirs to avoid creating directories
    def test_write_to_file(self, mock_makedirs, mock_open):
        filename = "test_pokemon"
        directory = "small/regular"
        small_unicode_sprite = "sprite_data"

        # Call the function with the mock data
        write_to_file(filename, directory, small_unicode_sprite)

        # Assert that os.makedirs was called with the correct directory
        mock_makedirs.assert_called_with(directory, exist_ok=True)

        # Assert that open was called with the correct file path and mode
        mock_open.assert_called_with(f"{directory}/{filename}", "w+")

        # Get the file handle that was passed to open() and check its write method
        mock_file = mock_open()
        mock_file().write.assert_called_with(small_unicode_sprite)


if __name__ == "__main__":
    unittest.main()
