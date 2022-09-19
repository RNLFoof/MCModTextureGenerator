from abc import ABC


class Checker(ABC):
    def check(self, tocheck):
        pass


class RegexChecker(Checker):
    regex: str

    def check(self, tocheck):
        pass
