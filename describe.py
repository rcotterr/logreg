from core.ds_core import DataAnalyzer
from core.my_exeption import ParserException
from colorama import Fore, Style
import sys


def main():
    if len(sys.argv) != 2:
        print('usage: ' + Fore.RED + 'python' + Fore.BLUE +
              ' describe.py ' + Fore.RESET + 'data_file.csv')
        sys.exit(-1)
    data_file = sys.argv[1]
    try:
        data_analyzer = DataAnalyzer(data_file)
        data_analyzer.describe()
    except IOError as e:
        print(Style.BRIGHT + Fore.RED + 'I/O Error: ' +
              Style.RESET_ALL + Fore.RESET + str(e))
    except ParserException as e:
        print(Style.BRIGHT + Fore.RED + 'ParserException: ' +
              Style.RESET_ALL + Fore.RESET + str(e))


if __name__ == '__main__':
    main()
