from interfaces import ImageToUnicodeConverter, PokemonDB


class SpritesGenerator:
    def __init__(
        self, db: PokemonDB, unicode_converter: ImageToUnicodeConverter
    ) -> None:
        self.db = db
        self.unicode_converter = unicode_converter

    def generate(self) -> None:
        for pokemon in self.db:
            print(pokemon.name)
            for sprite in pokemon.sprites:
                print(sprite.form)
                unicode_sprite = self.unicode_converter.convert_image_to_unicode(
                    sprite.image
                )
                print(unicode_sprite)
