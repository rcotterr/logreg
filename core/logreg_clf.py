import pandas as pd
import numpy as np
from tqdm import tqdm
import config
from core.stat_function import min_, max_


class LogisticRegression:
    def __init__(self):
        self.classes_name = ['Ravenclaw', 'Slytherin',
                             'Gryffindor', 'Hufflepuff']
        self.num_classes = len(self.classes_name)
        self.classes = [i for i in range(self.num_classes)]

    @staticmethod
    def _read_csv(file_name: str):
        df = pd.read_csv(file_name)
        return df

    @staticmethod
    def _sigmoid(logit):
        z = 1 / (1 + np.exp(-logit))
        return z

    @staticmethod
    def _get_x(df, features=config.features):
        df = df[features].copy(deep=True)
        for col in features:
            df[col] = (df[col] - min_(df[col]))\
                      / (max_(df[col]) - min_(df[col]))
        df = df.fillna(0)
        x = df[features].values
        n, k = x.shape
        x = np.concatenate((np.ones((n, 1)), x), axis=1)
        return x

    def _get_y(self, df):
        y_name = df['Hogwarts House']
        y = y_name.apply(lambda i: self.classes_name.index(i))
        y = y.values
        return y

    def train(self, file_name, n_epoch=config.n_epoch, lr=config.lr):
        df = self._read_csv(file_name)
        x = self._get_x(df)
        y = self._get_y(df)
        n, k = x.shape
        weight = pd.DataFrame(columns=self.classes)
        bar = tqdm(total=n_epoch * self.num_classes)
        for i in self.classes:
            w = np.zeros(k)
            y_tmp = np.where(y == i, 1, 0)
            for _ in range(n_epoch):
                logit = np.dot(x, w)
                z = self._sigmoid(logit)
                grad = (x.T @ (z - y_tmp)) / self.num_classes
                w -= grad * lr
                bar.update(1)
            weight[i] = w
        bar.close()
        df_w = pd.DataFrame(weight)
        df_w.to_csv('weights.csv', index=False)

    def predict(self, file_name, weight):
        w = self._read_csv(weight).values
        df = self._read_csv(file_name)
        x = self._get_x(df)
        list_houses = []
        for xi in x:
            logit = np.dot(xi, w)
            z = self._sigmoid(logit)
            i = int(np.argmax(z))
            class_ = self.classes_name[i]
            list_houses.append(class_)
        df_new = pd.DataFrame(list_houses, columns=['Hogwarts House'])
        df_new.index.name = 'Index'
        df_new.to_csv('houses.csv')
