import pickle

import pandas as pandas
from sklearn import linear_model

MODEL_PATH = "LinearModel.pkl"


def train_model():
    df = pandas.read_csv("C:\\Users\\Jan\\Downloads\\TData.csv")
    X = df[['Base64', 'Length', 'BCount']]
    y = df['IsEmpty']
    regr = linear_model.LinearRegression()
    regr.fit(X, y)


def load_model(file_path):
    with open(file_path, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model


def save_model(file_path, model):
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)


def base64_to_int(base64):
    count = 0
    for c in base64.replace("\n", ""):
        count = count + ord(c)
    return count


def get_predict_data(base64):
    return [base64_to_int(base64), len(base64), base64.count("A")]
