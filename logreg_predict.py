from core.logreg_clf import LogisticRegression
from core.my_exeption import LogisticRegressionException
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for predict')
    parser.add_argument('dataset_test', action='store',
                        help='Dataset for test in .csv')
    parser.add_argument('weights', action='store', help='Weights in .csv')
    args = parser.parse_args()
    try:
        model = LogisticRegression()
        model.predict(args.dataset_test, args.weights)
    except LogisticRegressionException as e:
        print('Logistic Regression Exception: ', str(e))
