'''
На входе: корпус текстов одного автора в папке.
На выходе: характерные черты авторского стиля:
- средняя длина предложения
- среднее количество предложений в абзаце
- удельная доля скобок в тексте
- неповторяемость слов
- средняя доля прилагательных в текстах корпуса;
- средняя длина предложения;
- среднее количество причастий (т.е. причастных оборотов)
- среднее количество оборотов "который"
Результат выводится в свежесозданную таблицу Эксель в той же папке

'''
import os
import nltk
import gensim
from gensim.utils import simple_preprocess
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from statistics import mean
import textract
import pymorphy2
import xlsxwriter
import numpy as np

import pandas as pd

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
root = tk.Tk()
root.withdraw()

morph = pymorphy2.MorphAnalyzer()

def Styl_for_author(text, name, filename):

    def lemmat_ru(file):
        '''Принимает текст, разбивает на слова, нормализирует каждое слово.
        Выделяет "который", полные прилагательные, краткие прил. и причастия
        На выходе - их удельная доля в тексте в процентах.
        '''
        list_adj=[]
        list_gerund=[]
        list_particle=[]
        list_pri4=[]
        counter=0
    
        words1=simple_preprocess(file)
        a=len(words1)
        for word in words1:
            p=morph.parse(word)[0]
            if p.normal_form=='который':
                counter=counter+1
            elif 'ADJF' in p.tag or 'ADJS' in p.tag:
                list_adj.append(p.normal_form)
            elif 'GRND' in p.tag:
                list_gerund.append(p.normal_form)
            elif 'PRTF' in p.tag:
                list_pri4.append(p.normal_form)
        b=len(list_adj)
        c=len(list_gerund)
        d=len(list_pri4)
        share_adj=float("{:0.2f}".format(b/a*100))
        share_grn=float("{:0.2f}".format(c/a*100))
        share_kotor=float("{:0.2f}".format(counter/a*100))
        share_pri4=float("{:0.2f}".format(d/a*100))
        uniq=len(list(set(words1)))
        share_uniq= float("{:0.2f}".format(uniq/a*100))
        return share_adj, share_grn, share_kotor, share_pri4, share_uniq

    def length(file):
        '''Вычисляем среднюю длину предложения в файле -
        число слов в тексте делим на количество предложений.
        Затем вычисляем стандартное отклонение (разброс) длин предложений'''
        list1=[]
        words1=simple_preprocess(file)
        a=len(words1)
        sent=sent_tokenize(file)
        b=len(sent)
        mean_sent=float("{:0.2f}".format(a/b))

        lis=[]
        for ele in sent:
            words=word_tokenize(ele)
            a=len(words)
            lis.append(a)
        b=np.array(lis)
        std_len_sent1=np.std(b)
        std_len_sent=float("{:0.2f}".format(std_len_sent1))
        return(mean_sent, std_len_sent)

    def count_brack(file):
        '''вычисляет удельное кол-во скобок'''
        words=file.split(' ')
        a=len(words)
        count=0
        for elem in text:
            if elem=='(' or elem==')':
                count+=1
        share_brack=float("{:0.2f}".format(count/a*100))
        return share_brack

    def quotes(file):
        '''вычисляет удельное кол-во кавычек'''
        words=file.split(' ')
        a=len(words)
        count=0
        for elem in text: # Заметь, в тексте, а не в токенизированных словах
            if elem=='«' or elem=='»' or elem=='"':
                count+=1
        share_quotes=float("{:0.2f}".format(count/a*100))
        return share_quotes

    def dash(file):
        '''вычисляет удельное кол-во тире (dash)
        Прим: есть три типа dash:
        в ascii - дефис с кодом 45 (тире в ascii нет вообще)
        в html - тире с кодом 8212 и  дефис с кодом 8211'''
        words=file.split(' ')
        a=len(words)
        count=0
        for elem in words:
            if elem==chr(8212) or elem==chr(8211) or elem==chr(45):
                count+=1
        share_dash=float("{:0.2f}".format(count/a*100))
        return share_dash

    def ellipsis(file):
        '''вычисляет удельное кол-во троеточий
        decimal code для троеточия Ворда - 8230'''
        words=file.split(' ')
        a=len(words)
        count=0
        for elem in words:
            if '...' in elem or '…' in elem:
                count+=1
        share_ellipsis=float("{:0.2f}".format(count/a*100))
        return share_ellipsis
    
    def verb_2(text):
        sent=sent_tokenize(text)
        a=len(sent)
        count=0
        for ele in sent:
            words=word_tokenize(ele)
            try:
                p=morph.parse(words[1])[0]
                if 'VERB' in p.tag:
                    count +=1
            except IndexError:
                print(' ')
        share_verb2=float("{:0.2f}".format(count/a*100))
        return share_verb2

    def paragr(text):
        count=0
        para=str.splitlines(text) # splits text by '\n'
        for ele in para:
            if ele != '':
                count +=1
        b=count # number of non-empty paragraphs

        sent=sent_tokenize(text)
        a=len(sent)
        c=float("{:0.2f}".format(a/b))
        return c

#    def stylometr(text, name, filename):
        '''вычисляем долю прил., прич., дееприч., 'который' функцией lemmat_ru,
        добавляем это число в соответствующий список shares,
        '''
    share_brack=count_brack(text)
    share_adj, share_grn, share_kotor, share_pri4, share_uniq=lemmat_ru(text)
    share_verb2=verb_2(text)
    len_paragr=paragr(text)
    mean_len, std_len_sent=length(text)
    sh_quotes=quotes(text)
    sh_dash=dash(text)
    sh_ellipsis=ellipsis(text)
    name_a=name

    lst_param=[filename, name, mean_len, share_adj, share_grn, share_kotor,
                share_pri4,share_brack,share_uniq, share_verb2,
                len_paragr, std_len_sent, sh_quotes, sh_dash, sh_ellipsis]
    return lst_param

''' Идея в том, чтобы теперь эти данные записывать построчно в датасет,
вместо того, чтобы формировать списки и записывать столбцами
'''

def new_author(file_path, name_a):
    '''Открываем каждый из файлов в папке, читаем текст,
    составляем строку ключевых параметров, дописываем ее в датасет'''

    for filename in os.listdir(file_path):
        #abs_filenames.append(os.path.normpath(os.path.join(file_path, filename))) 
        #filenames.append(filename)
        extension = os.path.splitext(filename)[1][1:] # Extract the extension from the filename
        if extension == "txt":
            with open(os.path.join(file_path, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                lst=Styl_for_author(text, name_a, filename)
                df.loc[len(df)]=lst
        elif extension == "docx": # use the textract library to open it. 
            text = textract.process(os.path.join(file_path, filename))
            text = text.decode("utf8")
            lst=Styl_for_author(text, name_a, filename)
            df.loc[len(df)]=lst
        else:
            continue

    return df

# Создаем пустой датафрейм с названиями столбцов
df = pd.DataFrame(columns=['Назв.файла', 'Имя автора', 'Ср. длина предл',
       'Доля прилагательных','Доля деепричастий',
       'Оборот "который"', 'Доля причастий',
       'Доля скобок', 'Неповторяемость слов',
       'Глагол на 2 месте', 'Ср. длина абзаца',
       'Станд.отклон. длин предложений',
       'Доля кавычек',
       'Доля тире',
       'Доля троеточий'])

# Начинаем процедуру создания датасета
messagebox.showinfo('info',
                        'Начинаем процедуру создания датасета')
name = simpledialog.askstring("Input", "Введите имя автора",
                                parent=root)
while name=='':
    messagebox.showinfo('Info', 'Таки введите автора')
    name = simpledialog.askstring("Input", "Введите имя автора")

messagebox.showinfo('info',
                        'Соберите файлы этого автора в отдельную папку и нажмите ок')
file_path = filedialog.askdirectory()

df=new_author(file_path, name)

# Добавим тексты второго автора
messagebox.showinfo('info',
                        'Добавим второго автора')

name = simpledialog.askstring("Input", "Введите имя автора",
                                parent=root)
while name=='':
    messagebox.showinfo('Info', 'Таки введите автора')
    name = simpledialog.askstring("Input", "Введите имя автора")

messagebox.showinfo('info',
                        'Соберите файлы этого автора в отдельную папку и нажмите ок')
file_path = filedialog.askdirectory()

df=new_author(file_path, name)

# popup Хотите добавить еще автора? да\нет
a = messagebox.askquestion('Вопрос', 'Хотите добавить третьего автора?')
if a == 'yes':
    name = simpledialog.askstring("Input", "Введите имя автора",
                                parent=root)
    while name=='':
        messagebox.showinfo('Info', 'Таки введите автора')
        name = simpledialog.askstring("Input", "Введите имя автора")

    messagebox.showinfo('info',
                        'Соберите файлы этого автора в отдельную папку и нажмите ок')
    file_path = filedialog.askdirectory()

    df_res=new_author(file_path, name)

    messagebox.showinfo('Response',
                        'Отлично, датасет лежит в файле Dataset_authors_3_exp.xlsx')
else:
    df_res=df
    messagebox.showinfo('Response',
                        'Отлично, датасет лежит в файле Dataset_authors_3_exp.xlsx')

df_res.to_excel('Dataset_authors_3_exp1.xlsx', index=False)   
