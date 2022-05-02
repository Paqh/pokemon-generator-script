from generator import SpritesGenerator
from pokesprite import PokespriteDB


def main() -> None:
    db = PokespriteDB()
    generator = SpritesGenerator(db)
    generator.generate()


if __name__ == "__main__":
    main()
