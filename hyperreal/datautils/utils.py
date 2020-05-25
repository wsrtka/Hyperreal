import pickle
import pandas as pd


def dump(filename, obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def load(filename):
    result = None
    with open(filename, 'rb') as f:
        result = pickle.load(f)
    return result


def get_data(filename):
    return pd.read_csv(filename)


def get_narkopedia(filename):
    return pd.read_json(filename)
