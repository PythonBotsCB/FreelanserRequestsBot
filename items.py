from constants import *

class Prices():
    def __init__(self, category:int) -> None:
        self.name = category

    def get_prices(self) -> dict:
        ''' возвращает словарь с ценами '''

        self.__prices = PRICES.get(self.name)
        return self.__prices

    def get_needprice(self, month:str) -> int:
        ''' возвращает нужную цену в зависимости от месяца'''

        return self.get_prices().get(month)