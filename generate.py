import os

from interfaces import ImageToUnicodeConverter, PokemonDB


def generate_sprites(
    db: PokemonDB, converter: ImageToUnicodeConverter, output_dir: str
):
    for pokemon in db:
        for sprite in pokemon.sprites:
            sprite_name = pokemon.ascii_name
            if sprite.form != "regular":
                sprite_name += f"-{sprite.form}"

            unicode_sprite = converter.convert_image_to_unicode(sprite.image)
            print(sprite_name)
            print(unicode_sprite)

            subdir = "shiny" if sprite.is_shiny else "regular"
            dir = f"{output_dir}/{subdir}"
            write_to_file(sprite_name, dir, unicode_sprite)


def write_to_file(filename: str, directory: str, text: str):
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/{filename}", "w+") as fout:
        fout.write(text)
