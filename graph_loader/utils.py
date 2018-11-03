import pickle


def save_object(obj, filename):
    with open(filename, 'wb') as file_out:
        pickle.dump(obj, file_out, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as file_in:
        return pickle.load(file_in)
