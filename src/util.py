import csv
import json
import os
import pickle

import pandas as pd
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

