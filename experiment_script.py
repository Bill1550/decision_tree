#!/usr/bin/env python

from ModelsML.DecisionTreeEstimators import ClassicDecisionTreeClassifier
from ModelsML.util import create_synthetic_data_function
from ModelsML.defined_params import *

import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


classifiers = {'ClassicDecisionTreeClassifier': ClassicDecisionTreeClassifier}

datasets = {'xor': create_synthetic_data_function(type_p='xor'),
            'donut': create_synthetic_data_function(type_p='donut')}

split_types = ['holdout']  # TODO: Add implementation beyond holdout


def main(args):
    """run experiments"""

    # extract hparams for experiment
    hparams = ParamsContainers.experiment_params[args.experiment_hparams]

    # create dataset
    dataset_x, dataset_y, data_types = datasets[hparams.dataset](seed=hparams.seed, n=500)

    # instantiate estimator
    basic_tree = classifiers[hparams.model]()

    # Only Holdout implemented
    # TODO: Add functionality for cross validation in Hparams
    x_train, x_test, y_train, y_test = train_test_split(dataset_x, dataset_y,
                                                        test_size=hparams.prop_test, random_state=hparams.seed)

    # train estimator
    basic_tree_fitted = basic_tree.train(x_train, y_train, data_types=data_types)

    # predict
    probabilities_train, predictions_train = basic_tree_fitted.predict(x_train)
    probabilities_test, predictions_test = basic_tree_fitted.predict(x_test)

    # print results
    print(f"Train Accuracy: {accuracy_score(y_train, predictions_train)}")
    print(f"Test Accuracy: {accuracy_score(y_test, predictions_test)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='experiment runner')

    parser.add_argument('--experiment_hparams', type=str, default='classic_xor',
                        help='ParamContainer for experiment hyper-parameters')

    parser.add_argument('--hparams_update', type=str, default=None,
                        help='Comma separated key-value pairs to update Hparams object')

    parser.add_argument('--uci_data', type=str, default="ICI/data/breast-cancer-wisconsin.data",
                        help='path to dataset')

    args = parser.parse_args()
    main(args)
