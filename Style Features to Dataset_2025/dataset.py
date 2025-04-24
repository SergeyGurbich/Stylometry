import os
import pandas as pd
from features import extract_features
from reader import read_text_from_file

def create_empty_dataframe():
    return pd.DataFrame(columns=[
        'Назв.файла', 'Имя автора', 'Ср. длина предл',
        'Доля прилагательных', 'Доля деепричастий',
        'Оборот "который"', 'Доля причастий',
        'Доля скобок', 'Неповторяемость слов',
        'Глагол на 2 месте', 'Ср. длина абзаца',
        'Станд.отклон. длин предложений',
        'Доля кавычек', 'Доля тире', 'Доля троеточий'
    ])

def add_author_to_dataframe(df, file_path, author_name):
    '''
    Читает файлы в папке и добавляет извлечённые признаки в датафрейм
    '''
    for filename in os.listdir(file_path):
        full_path = os.path.join(file_path, filename)
        try:
            text = read_text_from_file(full_path)
        except ValueError:
            continue  # Пропускаем неподдерживаемые форматы

        features = extract_features(text, author_name, filename)
        df.loc[len(df)] = features

    return df
