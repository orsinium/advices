import re

import attr


@attr.s
class StartsWith:
    pattern = attr.ib()

    def match(self, text):
        return text.startswith(self.pattern)


@attr.s
class EndsWith:
    pattern = attr.ib()

    def match(self, text):
        return text.endswith(self.pattern)


@attr.s
class Contains:
    pattern = attr.ib()

    def match(self, text):
        return self.pattern in text


@attr.s
class RegExp:
    pattern = attr.ib(converter=re.compile)

    def match(self, text):
        return bool(self.pattern.fullmatch(text))


mapping = dict(
    regexp=RegExp,
    startswith=StartsWith,
    endswith=EndsWith,
    contains=Contains,
)


def match(**kwargs):
    name, pattern = next(iter(kwargs.items()))
    return mapping[name](pattern)
