import csv
import json
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.decomposition import FastICA
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split


class Utils:

    def read_json(self, filename):
        """
        This method loads a json from a file
        :param filename:
        :return: a json file
        """
        resources = {}
        if filename:
            with open(filename, 'r') as file:
                resources = json.load(file)
        return resources

    def write_json_to_directory(self, json_object, file_name, directory="resources"):
        """
        This method writes a python object to a json file
        """
        self.make_directory_if_not_exists(directory)
        filename = os.path.join(directory, file_name)
        with open(filename, 'w') as outfile:
            json.dump(json_object, outfile)

    @staticmethod
    def write_to_directory(path, content):
        """
        This method writes a python object to a json file
        """
        with open(path, "w") as text_file:
            print(content, file=text_file)

    @staticmethod
    def make_directory_if_not_exists(directory):
        """
        this method creates a directory if it does not exists
        :param directory:
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def read_csv(filename):
        """
        This method reads a CSV file to a list
        :param filename:
        :return: a list containing elements per line of CSV
        """
        with open(filename, 'r') as a_file:
            return list(csv.reader(a_file))

    @staticmethod
    def read_data_to_dataframe(path):
        print(os.path.abspath(__file__))
        return pd.read_csv(path)

    @staticmethod
    def split_data(df):
        data = df.to_numpy()
        X = data[:, :-1]
        y = data[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def read_pickle_from_file(file_name):
        with open(file_name, 'rb') as input:
            return pickle.load(input)

    @staticmethod
    def apply_rfe(df, clf, n_features_to_select):
        """
        This method applied recursive feature elimination on a model to
        select n_features_to_select of the most important features
        :param df: dataframe [X,y]
        :param clf: the model
        :param n_features_to_select:
        :return: [X,y]
        """
        labels_name = list(df.columns.values)[len(list(df.columns.values)) - 1]
        df_y = df.iloc[:, -1]
        data = df.to_numpy()
        np.random.shuffle(data)
        X = data[:, :-1]
        y = data[:, -1]
        selector = RFE(clf, n_features_to_select, step=1)
        selector = selector.fit(X, y)
        df = df[df.columns[np.where(selector.ranking_ == 1)[0]]]
        df[labels_name] = df_y
        return df

    @staticmethod
    def apply_fast_ica(df, number_of_components):
        """
        This method applied ICA to a data_frame providing the number of components
        :param df:
        :param number_of_components:
        :return:
        """
        transformer = FastICA(n_components=number_of_components)
        labels_name = list(df.columns.values)[len(list(df.columns.values)) - 1]
        df_y = df.iloc[:, -1]
        df = df.iloc[:, :-1]
        # df = df.drop(labels='age', axis=1)
        data_transformed = transformer.fit_transform(df)
        data_transformed_df = pd.DataFrame(data_transformed)
        data_transformed_df[labels_name] = df_y
        return data_transformed_df

    @staticmethod
    def remove_column_with_condition(df, condition):
        """
        this method removes rows from data frame based on some conditions
        :param df:
        :param condition:
        :return:
        """
        df = df[condition]
        return df

    @staticmethod
    def normalize_df(df):
        """
        this method normalizes a data_frame
        :param df:
        :return:
        """
        labels_name = list(df.columns.values)[len(list(df.columns.values)) - 1]
        df_y = df.iloc[:, -1]
        df = df.iloc[:, :-1]
        normalized_df = (df - df.mean()) / df.std()
        normalized_df[labels_name] = df_y
        return normalized_df

