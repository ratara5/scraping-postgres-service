from enum import Enum


class Month(Enum):
    JANUARY = ("January", "enero")
    FEBRUARY = ("February", "febrero")
    MARCH = ("March", "marzo")
    APRIL = ("April", "abril")
    MAY = ("May", "mayo")
    JUNE = ("June", "junio")
    JULY = ("July", "julio")
    AUGUST = ("August", "agosto")
    SEPTEMBER = ("September", "septiembre")
    OCTOBER = ("October", "octubre")
    NOVEMBER = ("November", "noviembre")
    DECEMBER = ("December", "diciembre")

    def __init__(self, english_name, spanish_name):
        self.english_name = english_name
        self.spanish_name = spanish_name

    @classmethod
    def get_spanish_name(cls, english_name):
        for month in cls:
            if month.english_name == english_name:
                return month.spanish_name
        return None
    
    @classmethod
    def get_english_name(cls, spanish_name):
        for month in cls:
            if month.spanish_name == spanish_name:
                return month.english_name
        return None