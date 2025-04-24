import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from features import extract_features
from reader import read_text_from_file

def train_model_from_excel(excel_path):
    '''
    Загружает датасет, обучает модель, возвращает модель и тестовые данные
    '''
    df = pd.read_excel(excel_path)

    # Выделяем только числовые признаки
    feature_cols = df.columns[2:]
    X = df[feature_cols].to_numpy()
    y = df['Имя автора'].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    model = MLPClassifier(solver='lbfgs', random_state=0, hidden_layer_sizes=[20])
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Точность на обучающем наборе: {train_score:.2f}")
    print(f"Точность на тестовом наборе: {test_score:.2f}")

    return model, feature_cols

def train_model_from_dataframe(df):
    '''
    Альтернатива предыдущей функции для случаев, когда процесс создания датасета и предсказания объединен
    Принимает готовый DataFrame, обучает модель, возвращает модель и названия признаков
    '''
    feature_cols = df.columns[2:]
    X = df[feature_cols].to_numpy()
    y = df['Имя автора'].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    model = MLPClassifier(solver='lbfgs', random_state=0, hidden_layer_sizes=[20])
    model.fit(X_train, y_train)

    print(f"Точность на обучающем наборе: {model.score(X_train, y_train):.2f}")
    print(f"Точность на тестовом наборе: {model.score(X_test, y_test):.2f}")

    return model, feature_cols

def predict_author(text, model, feature_cols):
    '''
    Делает предсказание для нового текста (в виде строки)
    '''
    features = extract_features(text, author_name="?", filename="?")
    # Убираем первые два элемента: filename и author_name
    x_new = np.array([features[2:]])  # Сохраняем формат [[...]]
    prediction = model.predict(x_new)
    return prediction[0]
