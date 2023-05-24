def load_pickle(filepath):
    import pickle

    with open(filepath, "rb") as f:
        data = pickle.load(f)
    return data


def save_pickle(data, filepath):
    import pickle

    with open(filepath, "wb") as f:
        pickle.dump(data, f)


def get_filename(file):
    return file.split(".")[0]
