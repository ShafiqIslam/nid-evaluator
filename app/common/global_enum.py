from enum import Enum


class GlobalEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
