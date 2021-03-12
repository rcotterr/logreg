import os
import pandas as pd
from core.my_exeption import ParserException
from colorama import Fore, Style


class DataParser:
    def __init__(self, filename, sep=','):
        self.headers = []
        self.sep = sep
        self.__line_number = 0
        if not os.path.exists(os.path.abspath(filename)):
            raise ParserException(Style.BRIGHT + Fore.RED +
                                  "File doesn't exist")
        self.data = pd.read_csv(os.path.abspath(filename), sep=self.sep)
        self.headers = self.data.columns
