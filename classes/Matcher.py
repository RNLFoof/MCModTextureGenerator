import re
from dataclasses import dataclass
import dataclasses
from itertools import chain
import zipfile

from tqdm import tqdm

import settings


class Matcher:
    def test(self, file_info: zipfile.ZipInfo) -> bool:
        pass

    def vanilla_prep(self, file_info, file):
        pass

    def mod_prep(self, file_info, file):
        pass

    def pack_prep(self, file_info, file):
        pass

    def prep_end(self):
        pass

    @classmethod
    def get_all_matches(cls, matchers):
        matchers = set(matchers)  # Prevents dupes

        # Prep
        for zip_dir, method_name in [
            (settings.vanilla_mc_version_jar, "vanilla_prep"),
            (settings.mc_targeted_mod, "mod_prep"),
            (settings.mc_targeted_pack, "pack_prep"),
        ]:
            with zipfile.ZipFile(zip_dir, mode="r") as zip_file:
                for file_info in tqdm(zip_file.filelist, desc=f'Doing {method_name.replace("_", " ")}'):
                    with zip_file.open(file_info.filename) as file:
                        for matcher in matchers:
                            getattr(matcher, method_name)(file_info, file)

        # Matching
        matches = []

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items(), key=lambda x: x[0])))


class RegexMatcher(Matcher):
    def __init__(self, regex: str) -> None:
        self.regex = regex

    def test(self, file_info: zipfile.ZipInfo) -> bool:
        return re.match(self.regex, file_info.filename) is not None


class EndingMatcher(Matcher):
    def __init__(self, end: str) -> None:
        self.end = end

    def test(self, file_info: zipfile.ZipInfo) -> bool:
        return file_info.filename.endswith(self.end)
