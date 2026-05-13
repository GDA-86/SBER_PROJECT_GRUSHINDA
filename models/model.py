
import os
import sys

# Определяем путь к корню проекта (SBER_PROJECT_GRUSHINDA)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import pandas as pd

from my_functions2model import gda_main_proc

import pickle

from catboost import CatBoostClassifier

from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def load_model(name):
    # Десериализуем model из файла
    #with open('name', 'rb') as pkl_file:
    #    loaded_pipe = pickle.load(pkl_file)

    model = CatBoostClassifier()
    model.load_model(name)
    return model

def dump_model(name, model):
    # Сериализуем model и записываем результат в файл
    #with open(name, 'wb') as output:
    #    pickle.dump(model, output)
    model.save_model(name)


def train_model(X, y):
    cat_features = list(X.select_dtypes(include=['object', 'category']).columns)
    #cat_features = [str(col) for col in X.select_dtypes(include=['object', 'category']).columns]

    # Инициализация модели
    model = CatBoostClassifier(
        iterations=10,
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


    # собираем статистику на полном объеме 

    #Получаем предсказания
    preds = model.predict(X)          # Классы (0 или 1)
    probs = model.predict_proba(X)[:, 1] # Вероятности 

    # Выводим основные метрики 
    print("Отчет по классификации:")
    print(classification_report(y, preds))

    # Выводим AUC-ROC 
    auc = roc_auc_score(y, probs)
    print(f"ROC-AUC на тестовой выборке: {auc:.4f}")

    # Матрица ошибок 
    print("\nМатрица ошибок:")
    print(pd.crosstab(y, preds, rownames=['Actual'], colnames=['Predicted']))

    

    return model

def main_procces_start():
    lo_sessions = pd.read_csv('models/data/ga_sessions.csv')
    lo_hits = pd.read_csv('models/data/ga_hits.csv')

    lo_session = gda_main_proc(lo_sessions, lo_hits, mode=1)

    X = lo_session.drop(['target_is'], axis=1)
    y = lo_session['target_is']

    model = train_model(X, y)

    dump_model('models/model_v1.pkl',model)



if __name__ == "__main__":
    
  main_procces_start()