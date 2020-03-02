from enum import Enum


class Preprocess(Enum):
    THRESHOLD = 'thresh'
    BLUR = 'blur'


class Language(Enum):
    ENG = 'eng'
    BN = 'ben'
