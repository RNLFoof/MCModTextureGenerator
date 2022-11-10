import os.path
import re
import zipfile
from dataclasses import dataclass
from io import BytesIO
from typing import Callable

from PIL import Image
import ZachsStupidImageLibrary.coolstuff as zsil_coolstuff
import ZachsStupidImageLibrary.colors as zsil_colors

mc_root = r"C:\Users\Zach\Twitch\Minecraft\Instances\5 - 1.18.2"
mc_resource_packs = os.path.join(mc_root, "resourcepacks")
mc_mods = os.path.join(mc_root, "mods")
mc_targeted_pack = os.path.join(mc_resource_packs, "StylizedResourcePack_x256.zip")
mc_generated_pack = os.path.join(mc_resource_packs, "generated for mods")
mc_targeted_mod = os.path.join(mc_mods, "Quark-3.2-358.jar")


@dataclass
class Matcher:
    def test(self, source: str, target: str):
        pass


class CrystalMatcher(Matcher):
    def test(self, mod_file: str, pack_file: str):
        return re.match(r"assets.quark.textures.block.+?corundum\.png", mod_file) is not None and pack_file.endswith(
            "amethyst_block.png")


@dataclass
class Editor:
    rule: "Rule"

    def edit(self, mod_file_info, pack_file_info, mod_file, pack_file):
        pass


class MatchHueEditor(Editor):

    def edit(self, mod_file_info, pack_file_info, mod_file, pack_file):
        mod_image = Image.open(mod_file).convert("HSV")
        average_color = zsil_colors.average_color(mod_image)
        tosave = zsil_coolstuff.shift_bands_towards(Image.open(pack_file).convert("HSV"), average_color)
        # print(average_color, zsil_colors.average_color(tosave))
        saveto = os.path.join(mc_generated_pack, mod_file_info.filename)
        os.makedirs(os.path.split(saveto)[0], exist_ok=True)
        tosave.convert("RGBA").save(saveto)


class Rule:
    def __init__(self, matcher: Matcher, editor: type(Editor)):
        self.matcher = matcher
        self.editor = editor(self)

    def run(self):
        with zipfile.ZipFile(mc_targeted_pack, mode="r") as pack_jar:
            with zipfile.ZipFile(mc_targeted_mod, mode="r") as mod_jar:
                for mod_file_info in mod_jar.filelist:
                    for pack_file_info in pack_jar.filelist:
                        if self.matcher.test(mod_file_info.filename, pack_file_info.filename):
                            with pack_jar.open(pack_file_info.filename) as pack_file:
                                with mod_jar.open(mod_file_info.filename) as mod_file:
                                    self.editor.edit(mod_file_info, pack_file_info, mod_file, pack_file)


rules = [
    Rule(CrystalMatcher(), MatchHueEditor)

]


# def gen_textures(source: str, target: str, process: Callable):


def main() -> None:
    for rule in rules:
        rule.run()
    exit()


def fs(path: str) -> str:
    """Replaces backslashes with forward slashes, because that's what zipfile likes."""
    return path.replace("\\", "/")


if __name__ == '__main__':
    main()
