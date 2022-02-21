import os
import sys

from providers import DbConnect
from settings import DB_STRING

class DataMaker:

    def get_data(self, number):
        pass



if __name__ == '__main__':
    print("-" * 100)
    print("Start Database Worker")
    number = 10
    DataMaker().get_data(number)