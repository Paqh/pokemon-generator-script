import generate
from pokesprite import PokespriteDB
from unicode_converters import LargeSizeConverter, SmallSizeConverter


def main() -> None:
    db = PokespriteDB()
    db.include_forms = False
    converter_small = SmallSizeConverter()
    converter_large = LargeSizeConverter()

    generate.generate_sprites(db, converter_small, "small")
    generate.generate_sprites(db, converter_large, "large")


if __name__ == "__main__":
    main()
