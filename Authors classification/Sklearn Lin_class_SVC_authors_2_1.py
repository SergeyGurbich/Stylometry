'''
Программа имеет на входе датасет из 13 параметров для 48 текстов трех авторов
Разделяет его на обучающую и тестовую часть
Обучается по первой и тестируется по второй
На выходе она дает точность предсказания на тестовом наборе данных
Кроме того, она считывает новые 13 параметров, рассчитанные для нового текста
и дает предсказание - кому он принадлежит
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
from sklearn.svm import LinearSVC
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
    '''вычисляет удельное кол-во троеточий'''
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

df_test = pd.read_excel('Dataset_authors_3_new.xlsx',
                        usecols = [2,3,4,5,6,7,8,9,10,11,12,13,14]) # он игнорирует строку заголовка
x=pd.DataFrame.to_numpy(df_test)

df_target=pd.read_excel('Dataset_authors_3_new.xlsx', usecols = [1])
y=pd.DataFrame.to_numpy(df_target)

my_own_dataset = Bunch(data =x, target=y)

X_train, X_test, y_train, y_test = train_test_split( 
    my_own_dataset ['data'], my_own_dataset ['target'])#, random_state=0) 

'''
# Альтернативно, более простой способ чтения и формирования сета!!!
dataset = pd.read_excel('Dataset_authors_3_new.xlsx')
features=dataset.iloc[:,2:14]
labels=dataset.iloc[:,1]
x_train, x_test, y_train, y_test = train_test_split(features, labels)
'''
 
logreg = LinearSVC(multi_class='crammer_singer') #!!! когда классов больше двух
logreg.fit(X_train, np.ravel(y_train))  #(X_train, np.ravel(y_train))

print("Правильность на обучающем наборе: {:.2f}".format(logreg.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(logreg.score(X_test, y_test)))
#print(X_test, y_test)

#X_new = np.array([[26.04, 16.69, 0.15, 0.74, 0.74]])

'''Часть 2: Запрашиваем файл для анализа,
прогоняем его фрагментом программы стилометрии
и выдаем 6 параметров прямо в X_new, памятуя о том, что они д.б. в виде
[[16.17 12.77  0.94  0.67  1.48]]
'''

text=open_file() #Запрашиваем файл для анализа, на выходе - текст

mean_len, std_len_sent=length(text)
share_adj, share_grn, share_kotor, share_pri4, share_uniq=lemmat_ru(text)
share_brack=count_brack(text)
share_verb2=verb_2(text)
len_para=paragr(text)
sh_quotes=quotes(text)
sh_dash=dash(text)
sh_ellipsis=ellipsis(text)

X_new=np.array([[mean_len, share_adj, share_grn, share_kotor,
                 share_pri4, share_brack, share_uniq, share_verb2,
                 len_para, std_len_sent, sh_quotes, sh_dash, sh_ellipsis]])
#print(X_new)

prediction = logreg.predict(X_new)
print('This text was written by:', prediction)
#print(logreg.coef_)

