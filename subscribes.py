from datetime import date, timedelta
from constants import *

class Subscribe():
    def __init__(self, category:str, days:int, free=False):
        self.__category = category
        self.__days = days
        self.__start = str(date.today()).replace('-', '.')
        self.__end = str(date.today() + timedelta(days=days)).replace('-', '.')
        self.__gotFree = False

    def __str__(self) -> str:
        return self.__category

    def get_info(self) -> dict:
        return {
            "lenght_days" : self.__days,
            "start_sub" : self.__start,
            "end_sub" : self.__end,
            "type_sub" : self.get_type_sub(),
        }

    def get_type_sub(self) -> str:
        for type_sub in CONVERT_MONTH:
            if CONVERT_MONTH.get(type_sub) == self.__days:
                return type_sub
        return 'Бесплатная подписка'

class SimplePermissionSubscribe(Subscribe):
    def __init__(self, category:str, days:int, free:bool):
        super().__init__(category, days, free)

class AllPermisionSubscribe(Subscribe):
    def __init__(self, category:str, days:int, free:bool):
        super().__init__(category, days, free)
        ''' Дальнейшая проверка на ifinstance() и валидация на все преимущества '''
