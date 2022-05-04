from generator import SpritesGenerator
from pokesprite import PokespriteDB
from unicode_converters import LargeSizeConverter, SmallSizeConverter


def main() -> None:
    db = PokespriteDB()
    # converter_small = SmallSizeConverter()
    converter_large = LargeSizeConverter()
    # generator = SpritesGenerator(db, converter_small)
    generator = SpritesGenerator(db, converter_large)
    generator.generate()


if __name__ == "__main__":
    main()
