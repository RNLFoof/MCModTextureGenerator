import os

# Replace these with your own values
from classes import Editor, Matcher
from classes.Rule import Rule

mc_root = r"C:\Users\Zach\Twitch\Minecraft\Instances\5 - 1.18.2"
resource_pack_name = r"StylizedResourcePack_x256.zip"
vanilla_mc_version_jar = r'C:\Users\Zach\AppData\Roaming\.minecraft\versions\1.18.2\1.18.2.jar'

rules = [
    Rule(
        Matcher.RegexMatcher(r"assets.quark.textures.block.+?corundum_cluster\.png"),
        Matcher.EndingMatcher("amethyst_cluster.png"),
        Editor.TransferPaletteEditor
    ),
    Rule(
        Matcher.RegexMatcher(r"assets.quark.textures.block.+?corundum\.png"),
        Matcher.EndingMatcher("amethyst_block.png"),
        Editor.TransferPaletteEditor
    ),
]

# Leave these alone
mc_mods = os.path.join(mc_root, "mods")
mc_resource_packs = os.path.join(mc_root, "resourcepacks")
mc_targeted_pack = os.path.join(mc_resource_packs, resource_pack_name)
mc_generated_pack = os.path.join(mc_resource_packs, "generated for mods")
mc_targeted_mod = os.path.join(mc_mods, "Quark-3.2-358.jar")
