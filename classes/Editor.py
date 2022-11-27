from PIL import Image
from ZachsStupidImageLibrary import colors as zsil_colors
from ZachsStupidImageLibrary import coolstuff as zsil_coolstuff
import os


class Editor:
    def __init__(self, rule: "Rule"):
        self.rule = rule

    def edit(self, mod_filename: str, pack_filename: str, mod_file, pack_file) -> None:
        pass

    @staticmethod
    def save_image(mod_filename: str, image: Image) -> None:
        import settings
        save_to = os.path.join(settings.mc_generated_pack, mod_filename)
        os.makedirs(os.path.split(save_to)[0], exist_ok=True)
        image.convert("RGBA").save(save_to)


class MatchHueEditor(Editor):
    def edit(self, mod_filename: str, pack_filename: str, mod_file, pack_file) -> None:
        mod_image = Image.open(mod_file)
        mod_image_alpha = mod_image.getchannel("A")
        mod_image = mod_image.convert("HSV")
        average_color = zsil_colors.average_color(mod_image, alpha=mod_image_alpha)
        pack_image = Image.open(pack_file)
        a = pack_image.getchannel("A")
        to_save = zsil_coolstuff.shift_bands_towards(pack_image.convert("HSV"), average_color)
        to_save = to_save.convert("RGBA")
        to_save.putalpha(a)
        self.save_image(mod_filename, to_save)


class TransferPaletteEditor(Editor):
    def edit(self, mod_filename: str, pack_filename: str, mod_file, pack_file) -> None:
        mod_image = Image.open(mod_file)
        pack_image = Image.open(pack_file)
        self.save_image(mod_filename, zsil_coolstuff.transfer_palette(mod_image, pack_image))


class ChangelessEditor(Editor):
    def edit(self, mod_filename: str, pack_filename: str, mod_file, pack_file) -> None:
        pack_image = Image.open(pack_file)
        self.save_image(mod_filename, pack_image)
