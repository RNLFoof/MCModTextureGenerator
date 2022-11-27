import re
from dataclasses import dataclass
import dataclasses
import zipfile


@dataclass
class Matcher:
    def test(self, file_info: zipfile.ZipInfo) -> bool:
        pass

    def vanilla_prep(self, filename, file):
        pass

    def mod_prep(self, filename, file):
        pass

    def pack_prep(self, filename, file):
        pass

    def prep_end(self):
        pass

    def __hash__(self):
        return tuple(getattr(self, field.name) for field in dataclasses.fields(type(self)))


@dataclass
class RegexMatcher(Matcher):
    regex: str

    def test(self, file_info: zipfile.ZipInfo) -> bool:
        return re.match(self.regex, file_info.filename) is not None


@dataclass
class EndingMatcher(Matcher):
    end: str

    def test(self, file_info: zipfile.ZipInfo) -> bool:
        return file_info.filename.endswith(self.end)
