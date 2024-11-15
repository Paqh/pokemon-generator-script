import unittest
from unittest.mock import patch
from main import parse_cli_arguments

class TestParseCliArguments(unittest.TestCase):

    def test_no_arguments(self):
        # Simulate running with no arguments
        with patch('sys.argv', ['program_name']):
            args = parse_cli_arguments()
            print(args)
            self.assertFalse(args.include_forms)
            self.assertFalse(args.silent)

    def test_include_forms_argument(self):
        # Simulate running with the `--include-forms` argument
        with patch('sys.argv', ['program_name', '--include-forms']):
            args = parse_cli_arguments()
            print(args)
            self.assertTrue(args.include_forms)
            self.assertFalse(args.silent)

    def test_silent_argument(self):
        # Simulate running with the `--silent` argument
        with patch('sys.argv', ['program_name', '--silent']):
            args = parse_cli_arguments()
            print(args)
            self.assertFalse(args.include_forms)
            self.assertTrue(args.silent)

    def test_both_arguments(self):
        # Simulate running with both `--include-forms` and `--silent` arguments
        with patch('sys.argv', ['program_name', '--include-forms', '--silent']):
            args = parse_cli_arguments()
            print(args)
            self.assertTrue(args.include_forms)
            self.assertTrue(args.silent)

if __name__ == "__main__":
    unittest.main()
