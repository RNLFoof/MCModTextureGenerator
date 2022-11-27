import zipfile
from typing import Optional

from typing.io import IO

from classes.Matcher import Matcher


class Rule:
    from classes.Editor import Editor, ChangelessEditor

    def __init__(self, mod_matcher: Matcher, pack_matcher: Matcher, editor: type(Editor),
                 editor_n: type(Editor) = ChangelessEditor, editor_s: type(Editor) = ChangelessEditor):
        self.mod_matcher = mod_matcher
        self.pack_matcher = pack_matcher
        self.editor = editor(self)
        self.editor_n = editor_n(self)
        self.editor_s = editor_s(self)

    def run(self):
        import settings
        with zipfile.ZipFile(settings.mc_targeted_mod, mode="r") as mod_jar, zipfile.ZipFile(settings.mc_targeted_pack,
                                                                                             mode="r") as pack_zip:
            for mod_file_info in mod_jar.filelist:
                for pack_file_info in pack_zip.filelist:
                    if self.mod_matcher.test(mod_file_info) and self.pack_matcher.test(pack_file_info):
                        for suffix, editor in [
                            ("", self.editor),
                            ("_n", self.editor_n),
                            ("_s", self.editor_s),
                        ]:
                            with ImagesContextManager(mod_file_info, pack_file_info, mod_jar, pack_zip, suffix) as (
                                    mod_filename, pack_filename, mod_file, pack_file):
                                editor.edit(mod_filename, pack_filename, mod_file, pack_file)

    @staticmethod
    def process_all(rules):
        from classes.Matcher import Matcher

        Matcher.get_all_matches(
            [rule.pack_matcher for rule in rules] +
            [rule.mod_matcher for rule in rules]
        )

        for rule in rules:
            rule.run()


class ImagesContextManager:
    def __init__(self, mod_file_info: zipfile.ZipInfo, pack_file_info: zipfile.ZipInfo, mod_jar: zipfile,
                 pack_zip: zipfile, suffix: str):
        self.mod_jar = mod_jar
        self.pack_zip = pack_zip

        self.mod_file: Optional[IO] = None
        self.pack_file: Optional[IO] = None

        self.mod_filename = mod_file_info.filename.removesuffix(".png") + suffix + ".png"
        self.pack_filename = pack_file_info.filename.removesuffix(".png") + suffix + ".png"

    def __enter__(self):
        self.mod_file = self.mod_jar.open(self.mod_filename) \
            if self.mod_filename in self.mod_jar.namelist() \
            else None
        self.pack_file = self.pack_zip.open(self.pack_filename) \
            if self.pack_filename in self.pack_zip.namelist() \
            else None
        return self.mod_filename, self.pack_filename, self.mod_file, self.pack_file

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.mod_file is not None:
            self.mod_file.close()
        if self.pack_file is not None:
            self.pack_file.close()
