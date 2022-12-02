import os
from functools import cached_property



# Replace these with your own values
from typing import List

from cachetools import cached

mc_root = r"C:\Users\Zach\Twitch\Minecraft\Instances\5 - 1.18.2"
resource_pack_name = r"StylizedResourcePack_x256.zip"
vanilla_mc_version_jar = r'C:\Users\Zach\AppData\Roaming\.minecraft\versions\1.18.2\1.18.2.jar'


def rules():
    print("hey")
    from classes.Source import Source
    from classes import Editor, Matcher
    from classes.Rule import Rule

    return [
        Rule(
            (
                Matcher.RegexMatcher(Source.MOD, r"assets.quark.textures.block.+?corundum_cluster\.png"),
                Matcher.EndingMatcher(Source.PACK, "amethyst_cluster.png"),
            ),
            Editor.TransferPaletteEditor
        ),
        Rule(
            (
                Matcher.RegexMatcher(Source.MOD, r"assets.quark.textures.block.+?corundum\.png"),
                Matcher.EndingMatcher(Source.PACK, "amethyst_block.png"),
            ),
            Editor.TransferPaletteEditor
        ),
        # When mod matches vanilla, transfer from mod to pack
        Rule(
            (
                Matcher.RegexMatcher(Source.MOD, r"assets.quark.textures.block.+?corundum\.png"),
                Matcher.EndingMatcher(Source.PACK, "amethyst_block.png"),
            ),
            Editor.TransferPaletteEditor
        ),
    ]


# Leave these alone
mc_mods = os.path.join(mc_root, "mods")
mc_resource_packs = os.path.join(mc_root, "resourcepacks")
mc_targeted_pack = os.path.join(mc_resource_packs, resource_pack_name)
mc_generated_pack = os.path.join(mc_resource_packs, "generated for mods")
mc_targeted_mod = os.path.join(mc_mods, "Quark-3.2-358.jar")
