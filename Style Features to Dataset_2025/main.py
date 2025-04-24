import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

from dataset import create_empty_dataframe, add_author_to_dataframe

# Инициализация интерфейса
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

# Основная процедура
df = create_empty_dataframe()

messagebox.showinfo('info', 'Начинаем создание датасета')
file_path, name = dialog()
df = add_author_to_dataframe(df, file_path, name)

messagebox.showinfo('info', 'Добавим второго автора')
file_path, name = dialog()
df = add_author_to_dataframe(df, file_path, name)

if messagebox.askquestion('Вопрос', 'Хотите добавить третьего автора?') == 'yes':
    file_path, name = dialog()
    df = add_author_to_dataframe(df, file_path, name)
    messagebox.showinfo('Response', 'Отлично, датасет сохранён')
else:
    messagebox.showinfo('Response', 'Отлично, датасет сохранён')

# Сохраняем результат
df.to_excel('Dataset_authors_3_exp2.xlsx', index=False)
