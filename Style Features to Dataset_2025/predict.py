import tkinter as tk
from tkinter import filedialog, messagebox
from classifier import train_model_from_excel, predict_author
from reader import read_text_from_file

# Инициализация окна
root = tk.Tk()
root.withdraw()

# Загружаем модель
excel_path = filedialog.askopenfilename(
    title="Выберите Excel-файл с обучающим датасетом",
    filetypes=[("Excel Files", "*.xlsx")]
)
model, feature_cols = train_model_from_excel(excel_path)

# Выбор файла для анализа
messagebox.showinfo("Инфо", "Теперь выберите файл неизвестного автора")
text_path = filedialog.askopenfilename(
    title="Выберите текстовый файл",
    filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx")]
)
text = read_text_from_file(text_path)

# Предсказание
author = predict_author(text, model, feature_cols)
messagebox.showinfo("Результат", f"Этот текст, скорее всего, написал: {author}")
