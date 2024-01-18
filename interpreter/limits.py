from json import load
from typing import Any
import data_structures as ds
from os import path

class Limits:

    def __init__(self) -> None:
        self.limits: dict[str, int | None] = {}
        with open(path.join(path.dirname(__file__), "default_limits.json")) as config_file:
            self.limits = load(config_file)

    def apply_config(self, config: dict[str, int | None]) -> None:
        for key in config:
            self.limits[key] = config[key]

    def __detect_limits(self, value: Any) -> list[str]:
        res: list[str] = []
        if isinstance(value, int | float):
            res.append("numbers")
        if isinstance(value, bool):
            res.append("booleans")
        if isinstance(value, str):
            res.append("strings")
        if value is None:
            res.append("nones")
        if isinstance(value, ds.LazyArray):
            res.append("lazy_arrays")
            res.append("data_structures")
        if isinstance(value, ds.StaticArray):
            res.append("static_arrays")
            res.append("data_structures")
        if isinstance(value, ds.DynamicArray):
            res.append("dynamic_arrays")
            res.append("data_structures")
        if isinstance(value, ds.Array):
            res.append("arrays")
            res.append("data_structures")
        if isinstance(value, ds.Dictionary):
            res.append("dictionaries_or_maps")
            res.append("data_structures")
        if isinstance(value, ds.Stack):
            res.append("stacks")
            res.append("data_structures")
        if isinstance(value, ds.Queue):
            res.append("queues")
            res.append("data_structures")
        if isinstance(value, ds.BinaryTree):
            res.append("binary_trees")
            res.append("data_structures")
        if isinstance(value, ds.Set):
            res.append("sets")
            res.append("data_structures")
        if isinstance(value, ds.Multiset):
            res.append("multisets")
            res.append("data_structures")
        if isinstance(value, ds.CustomStructure):
            res.append("custom_structures")
            res.append("data_structures")
        return list(set(res))

    def change_limit_by_value(self, value: Any, change: int) -> None:
        for key in self.__detect_limits(value):
            if self.limits[key] is not None:
                self.limits[key] += change
                if self.limits[key] < 0:
                    raise Exception(f"You have exceeded limit for \"{key}\"")

    def change_limit_by_name(self, name: str, change: int) -> None:
        if self.limits[name] is not None:
            self.limits[name] += change
            if self.limits[name] < 0:
                raise Exception(f"You have exceeded limit for \"{name}\"")

limits = Limits()