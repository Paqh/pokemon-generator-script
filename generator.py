from interfaces import PokemonDB


class SpritesGenerator:
    def __init__(self, db: PokemonDB) -> None:
        self.db = db

    def generate(self) -> None:
        for pokemon in self.db:
            print(f"{pokemon.name} forms:{pokemon.forms}")
