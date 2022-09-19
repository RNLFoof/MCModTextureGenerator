import os.path
import re
import zipfile
from io import BytesIO

from PIL import Image
import ZachsStupidImageLibrary.coolstuff as zsil_coolstuff
import ZachsStupidImageLibrary.colors as zsil_colors

mc_root = r"C:\Users\Zach\Twitch\Minecraft\Instances\5 - 1.18.2"
mc_resource_packs = os.path.join(mc_root, "resourcepacks")
mc_mods = os.path.join(mc_root, "mods")
mc_targeted_pack = os.path.join(mc_resource_packs, "StylizedResourcePack_x256.zip")
mc_generated_pack = os.path.join(mc_resource_packs, "generated for mods")
mc_targeted_mod = os.path.join(mc_mods, "Quark-3.2-358.jar")


def main() -> None:
    with zipfile.ZipFile(mc_targeted_pack, mode="r") as zip_f:
        with zipfile.ZipFile(mc_targeted_mod, mode="r") as mod_jar:
            for mod_filename in filter(lambda x: re.match(r"assets.quark.textures.block.+?corundum\.png", x.filename),
                                   mod_jar.filelist):
                mod_filename = mod_filename.filename
                print(mod_filename)
                with zip_f.open(fs(r"assets\minecraft\textures\block\amethyst_block.png")) as img_f:
                    with mod_jar.open(mod_filename) as mod_file:
                        # mod_image = Image.open(mod_file).convert("HSV")
                        # average_hue = zsil_colors.average_color(mod_image.getchannel("H"))
                        # zsil_coolstuff.shift_hue_towards(Image.open(img_f), average_hue).show()
                        mod_image = Image.open(mod_file).convert("HSV")
                        average_color = zsil_colors.average_color(mod_image)
                        tosave = zsil_coolstuff.shift_bands_towards(Image.open(img_f).convert("HSV"), average_color)
                        saveto = os.path.join(mc_generated_pack, mod_filename)
                        os.makedirs(os.path.split(saveto)[0], exist_ok=True)
                        tosave.convert("RGBA").save(saveto)

                        # with zipfile.ZipFile(mc_generated_pack, 'w') as myzip:
                        #     bio = BytesIO()
                        #     tosave.convert("RGB").save(bio, format="png")
                        #     myzip.writestr(mod_filename, bio.read())


def fs(path: str) -> str:
    """Replaces backslashes with forward slashes, because that's what zipfile likes."""
    return path.replace("\\", "/")


if __name__ == '__main__':
    main()
