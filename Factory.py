from Utilities import Utilities as util
from typing import(
    Dict,
    Any
)


class Factory:

    def __init__(self, n: str, cache: Dict) -> None:
        self.n = n
        self.cache = cache

    def __call__(self, *args, **kwargs):
        if self.n == "btn": return util.btn_builder(*args, **self.cache, **kwargs)
        elif self.n == "lbl": return util.btn_builder(*args, **self.cache, **kwargs)
        elif self.n == "lne": return util.btn_builder(*args, **self.cache, **kwargs)
        if self.n == "wdg": return util.btn_builder(*args, **self.cache, **kwargs)