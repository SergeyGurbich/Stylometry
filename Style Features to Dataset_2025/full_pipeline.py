import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

from dataset import create_empty_dataframe, add_author_to_dataframe
from classifier import train_model_from_dataframe, predict_author
from reader import read_text_from_file

# Инициализация GUI
root = tk.Tk()
root.withdraw()

def dialog():
    '''Запрашивает имя автора и путь к его папке'''
    name = simpledialog.askstring("Input", "Введите имя автора", parent=root)
    while not name:
        messagebox.showinfo('Info', 'Таки введите имя автора')
        name = simpledialog.askstring("Input", "Введите имя автора")

    messagebox.showinfo('info', 'Соберите файлы автора в отдельной папке и нажмите ОК')
    file_path = filedialog.askdirectory()
    return file_path, name

# Шаг 1: сбор данных для обучения
df = create_empty_dataframe()

messagebox.showinfo('info', 'Выберите первую папку с текстами')
path1, name1 = dialog()
df = add_author_to_dataframe(df, path1, name1)

messagebox.showinfo('info', 'Выберите вторую папку с текстами')
path2, name2 = dialog()
df = add_author_to_dataframe(df, path2, name2)

if messagebox.askquestion('Вопрос', 'Добавить третьего автора?') == 'yes':
    path3, name3 = dialog()
    df = add_author_to_dataframe(df, path3, name3)

# Шаг 2: обучение модели
model, feature_cols = train_model_from_dataframe(df)

# Шаг 3: выбор текста для анализа
messagebox.showinfo("Анализ", "Теперь выберите текст для анализа")
text_path = filedialog.askopenfilename(
    title="Выберите файл спорного текста",
    filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx")]
)
text = read_text_from_file(text_path)

# Шаг 4: предсказание
author = predict_author(text, model, feature_cols)
messagebox.showinfo("Результат", f"Этот текст, скорее всего, написал: {author}")
