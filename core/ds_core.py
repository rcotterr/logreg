import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from colorama import Fore, Style
from core.data_parser import DataParser
from core.stat_function import count_, mean_, std_, min_, max_, percentile_
import warnings

warnings.filterwarnings('ignore')


class DataAnalyzer:
    __HISTOGRAM_DIRECTORY = 'Histograms/'
    __SCATTERPLOT_DIRECTORY = 'ScatterPlots/'
    __PAIRPLOT_DIRECTORY = 'PairPlots/'
    __TRANSPARENCY = 0.5

    def __init__(self, filename):
        parser = DataParser(filename)
        self.headers = parser.headers
        self.data = np.array(parser.data, dtype=object)

        self.num_fichas = self.extracy_num_fichas()

    def extracy_num_fichas(self):
        num_fichas = []
        for i, name in enumerate(self.headers):
            if self.check_num_fichas(i):
                num_fichas.append(i)
        return num_fichas

    def check_num_fichas(self, column_ind):
        for c in self.data[:, column_ind]:
            if type(c) == float or type(c) == int:
                return True
        return False

    def describe(self):
        print(
            f'{"":15} |{"Count":>12} |{"Mean":>12} |{"Std":>12} |{"Min":>12}'
            f'|{"25%":>12} |{"50%":>12} |{"75%":>12} |{"Max":>12}')
        for i in self.num_fichas:
            print(f'{self.headers[i]:15.15}', end=' |')
            data_v = np.array(self.data[:, i], dtype=float)
            data_v = data_v[~np.isnan(data_v)]
            print(f'{count_(data_v):>12.4f}', end=' |')
            print(f'{mean_(data_v):>12.4f}', end=' |')
            print(f'{std_(data_v):>12.4f}', end=' |')
            print(f'{min_(data_v):>12.4f}', end=' |')
            print(f'{percentile_(data_v, 25):>12.4f}', end=' |')
            print(f'{percentile_(data_v, 50):>12.4f}', end=' |')
            print(f'{percentile_(data_v, 75):>12.4f}', end=' |')
            print(f'{max_(data_v):>12.4f}')
        print()

    def distribute_per_house(self):
        res = {}
        if 'Hogwarts House' not in self.headers:
            raise Exception(Style.BRIGHT + Fore.RED +
                            "Column 'Hogwarts House' not in columns list")
        houses = self.data[:, list(self.headers).index('Hogwarts House')]
        for ficha_ind in self.num_fichas:
            values_per_house = {}
            for i in range(len(self.data[:, ficha_ind])):
                current_house = houses[i]
                if current_house in values_per_house:
                    values_per_house[current_house].append(
                        self.data[:, ficha_ind][i])
                else:
                    values_per_house[current_house] = \
                        [self.data[:, ficha_ind][i]]
            res[self.headers[ficha_ind]] = values_per_house
        return res

    def __generate_histogram(self, ax, ficha_name,
                             ficha_data, bins=None):
        for faculte_name in ficha_data.keys():
            ax.hist(ficha_data[faculte_name], label=faculte_name, fill=True,
                    bins=bins, alpha=DataAnalyzer.__TRANSPARENCY)
        ax.set_ylabel(ficha_name)
        ax.set_xlabel('Count')
        ax.set_title('Distribution of ' + ficha_name)
        ax.legend(loc='upper right')

    def plot_histograms(self):
        distribute_per_house = self.distribute_per_house()
        if os.path.exists(self.__HISTOGRAM_DIRECTORY):
            shutil.rmtree(self.__HISTOGRAM_DIRECTORY)
        os.mkdir(self.__HISTOGRAM_DIRECTORY)
        for ficha_name in distribute_per_house.keys():
            fig, ax = plt.subplots()
            self.__generate_histogram(
                ax, ficha_name=ficha_name,
                ficha_data=distribute_per_house[ficha_name]
            )
            filename = \
                self.__HISTOGRAM_DIRECTORY + \
                '%s' % (ficha_name) + '.png'
            fig.savefig(filename)
            print('Saved histogram at ' + Fore.BLUE + filename + Fore.RESET)

    def __scatter_plot(self, ax, ficha_name_1, ficha_name_2,
                       ficha_data_1, ficha_data_2):
        if set(ficha_data_1.keys()) != set(ficha_data_2.keys()):
            raise Exception(Style.BRIGHT + Fore.RED +
                            "Different count of fuculte")
        for faculte_name in ficha_data_1.keys():
            ax.scatter(ficha_data_1[faculte_name],
                       ficha_data_2[faculte_name], label=faculte_name,
                       alpha=DataAnalyzer.__TRANSPARENCY)
        ax.set_xlabel(ficha_name_1)
        ax.set_ylabel(ficha_name_2)
        ax.set_title("{} vs {}".format(ficha_name_1, ficha_name_2))
        ax.legend(loc='upper right')
        return plt

    def plot_scatter_plots(self):
        distribute_per_house = self.distribute_per_house()
        if os.path.exists(self.__SCATTERPLOT_DIRECTORY):
            shutil.rmtree(self.__SCATTERPLOT_DIRECTORY)
        os.mkdir(self.__SCATTERPLOT_DIRECTORY)
        for ficha_name_1 in distribute_per_house.keys():
            for ficha_name_2 in distribute_per_house.keys():
                if ficha_name_1 != ficha_name_2:
                    fig, ax = plt.subplots()
                    self.__scatter_plot(
                        ax, ficha_name_1=ficha_name_1,
                        ficha_name_2=ficha_name_2,
                        ficha_data_1=distribute_per_house[ficha_name_1],
                        ficha_data_2=distribute_per_house[ficha_name_2])
                    filename = \
                        self.__SCATTERPLOT_DIRECTORY + \
                        '%s - %s' % (ficha_name_1, ficha_name_2) + '.png'
                    fig.savefig(filename)
                    print('Saved scatter_plot at ' + Fore.BLUE +
                          filename + Fore.RESET)

    def plot_pair_plot(self):
        distribute_per_house = self.distribute_per_house()
        if os.path.exists(self.__PAIRPLOT_DIRECTORY):
            shutil.rmtree(self.__PAIRPLOT_DIRECTORY)
        os.mkdir(self.__PAIRPLOT_DIRECTORY)
        n = len(distribute_per_house.keys())
        fig, ax = plt.subplots(nrows=n, ncols=n, figsize=(70, 70))
        for i, ficha_name_1 in enumerate(distribute_per_house.keys()):
            for j, ficha_name_2 in enumerate(distribute_per_house.keys()):
                if ficha_name_1 != ficha_name_2:
                    self.__scatter_plot(
                        ax[i, j], ficha_name_1=ficha_name_1,
                        ficha_name_2=ficha_name_2,
                        ficha_data_1=distribute_per_house[ficha_name_1],
                        ficha_data_2=distribute_per_house[ficha_name_2]
                    )
                else:
                    self.__generate_histogram(
                        ax[i, j],
                        ficha_name=ficha_name_1,
                        ficha_data=distribute_per_house[ficha_name_1]
                    )
        filename = self.__PAIRPLOT_DIRECTORY + 'pair_plot.png'
        fig.savefig(filename)
        print('Saved pair_plot at ' + Fore.BLUE + filename + Fore.RESET)
