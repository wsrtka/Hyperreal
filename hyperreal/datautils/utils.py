import pickle


def dump(filename, obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def load(filename):
    result = None
    with open(filename, 'rb') as f:
        result = pickle.load(f)
    return result
