from core.logreg_clf import LogisticRegression
from core.my_exeption import LogisticRegressionException
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for train')
    parser.add_argument('dataset_train', action='store',
                        help='Dataset for train in .csv')
    args = parser.parse_args()
    try:
        model = LogisticRegression()
        model.train(args.dataset_train)
    except LogisticRegressionException as e:
        print('Logistic Regression Exception: ', str(e))
