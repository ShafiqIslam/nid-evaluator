from enum import Enum as BaseEnum


class Enum(BaseEnum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
