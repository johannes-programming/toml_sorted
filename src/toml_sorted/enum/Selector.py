import enum

__all__ = ["Selector"]


class Selector(enum.Enum):
    ALL_KEYS = enum.auto()
    ALL_INDICES = enum.auto()
