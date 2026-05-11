import pandas as pd

from models.my_functions2model import gda_main_proc

import pickle

from catboost import CatBoostClassifier


def load_model(name):
    # Десериализуем pipeline из файла
    with open('name', 'rb') as pkl_file:
        loaded_pipe = pickle.load(pkl_file)



def dump_model(name, model):
    # Сериализуем pipeline и записываем результат в файл
    with open(name, 'wb') as output:
        pickle.dump(model, output)


def train_model(X, y):
    cat_features = list(X.select_dtypes(include=['object', 'category']).columns)

    # Инициализация модели
    model = CatBoostClassifier(
        iterations=500,
        learning_rate=0.05,
        depth=6,
        eval_metric='AUC', 
        random_seed=42,
        verbose=100,
        auto_class_weights='Balanced',
        early_stopping_rounds=100,
    )

    # Обучение
    model.fit(
        X, y,
        cat_features=cat_features
    )


    return model

def main_procces_start():
    lo_sessions = pd.read_csv('data/ga_sessions.csv')
    lo_hits = pd.read_csv('data/ga_hits.csv')

    lo_session = gda_main_proc(lo_sessions, lo_hits)

    X = lo_session.drop(['target_is'], axis=1)
    y = lo_session['target_is']

    train_model(X, y)



if __name__ == "__main__":
    
  main_procces_start()