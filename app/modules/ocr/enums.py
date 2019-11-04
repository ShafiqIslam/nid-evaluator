from enum import Enum


class Preprocess(Enum):
    THRESHOLD = 'thresh'
    BLUR = 'blur'


class Lang(Enum):
    ENG = 'eng'
    BN = 'ben'
