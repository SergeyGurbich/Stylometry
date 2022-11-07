'''
Программа имеет на входе датасет из 7 параметров для 32 текстов двух авторов
Разделяет его на обучающую и тестовую часть
Обучается по первой и тестируется по второй
На выходе она дает точность предсказания на тестовом наборе данных
Кроме того, она считывает новые 7 параметров, рассчитанные для нового текста
и дает предсказание - кому он принадлежит

Программа реализована с помощью модели маш.обуч. "Логистическая регрессия",
использована для классификации НА 3 группы (полиномиальная классификация)
На тестовом сете точность предсказания - 0.50
'''
import os
import textract
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from gensim.utils import simple_preprocess
import pandas as pd
from sklearn.utils import Bunch
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression
import numpy as np
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

def open_file():
    '''   Открываем тестовый файл для чтения, по запросу - txt или docx'''
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), # getcwd() returns current working directory of a process
                               title="Choose Input File",
                               filetypes = (("Word Documents","*.docx"),("Text Files","*.txt"))
                               )
    if not filename:
        return

    extension = os.path.splitext(filename)[1][1:] # Extract the extension from the filename
    if extension == "txt": # If it is a .txt file just open the file and read the contents
        with open(filename, "r", encoding="utf-8") as input_file:
            text = input_file.read()

    elif extension == "docx": # if it is a .docx use the docx library to open it. Подробно - здесь
        text = textract.process(filename)
        text = text.decode("utf8")
    else:
        text="" # If the filename does not have a .txt. or .docx extension, return an empty string
    return text

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
    '''Вычисляем среднюю длину предложения в файле'''
    list1=[]
    words1=simple_preprocess(file)
    a=len(words1)
    sent=sent_tokenize(file)
    b=len(sent)
    mean_sent=float("{:0.2f}".format(a/b))
    return(mean_sent)

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


df_test = pd.read_excel('Dataset_authors.xlsx', usecols = [1,2,3,4,5,6,7]) # он игнорирует строку заголовка
x=pd.DataFrame.to_numpy(df_test)

df_target=pd.read_excel('Dataset_authors.xlsx', usecols = [8])
y=pd.DataFrame.to_numpy(df_target)

my_own_dataset = Bunch(data =x, target=y)

X_train, X_test, y_train, y_test = train_test_split( 
    my_own_dataset ['data'], my_own_dataset ['target'], random_state=0) 
 
logisticRegr = LogisticRegression(multi_class='multinomial') 
logisticRegr.fit(X_train, y_train) #(X_train, np.ravel(y_train))

print("Правильность на обучающем наборе: {:.2f}".format(logisticRegr.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(logisticRegr.score(X_test, y_test)))
#print(X_test, y_test)

#X_new = np.array([[26.04, 16.69, 0.15, 0.74, 0.74]])

'''Часть 2: Запрашиваем файл для анализа,
прогоняем его фрагментом программы стилометрии
и выдаем 6 параметров прямо в X_new, памятуя о том, что они д.б. в виде
[[16.17 12.77  0.94  0.67  1.48]]
'''

text=open_file() #Запрашиваем файл для анализа, на выходе - текст

mean_len=length(text)
share_adj, share_grn, share_kotor, share_pri4, share_uniq=lemmat_ru(text)
share_brack=count_brack(text)

X_new=np.array([[mean_len, share_adj, share_grn, share_kotor,
                 share_pri4, share_brack, share_uniq]])
#print(X_new)

prediction = logisticRegr.predict(X_new)
print('This text was written by:', prediction)

