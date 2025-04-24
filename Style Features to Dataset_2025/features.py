# Set of functions to extract specific features of the style for russian text
#  
from gensim.utils import simple_preprocess
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def count_brackets(text):
    return round((text.count('(') + text.count(')')) / len(text.split()) * 100, 2)

def count_quotes(text):
    return round(sum(text.count(q) for q in ['«', '»', '"']) / len(text.split()) * 100, 2)

def count_dashes(text):
    dashes = ['–', '—', '-']
    return round(sum(text.count(d) for d in dashes) / len(text.split()) * 100, 2)

def count_ellipsis(text):
    return round(sum(text.count(e) for e in ['...', '…']) / len(text.split()) * 100, 2)

def count_mean_sentence_length(text):
    sentences = sent_tokenize(text)
    lengths = [len(word_tokenize(s)) for s in sentences]
    mean_len = round(np.mean(lengths), 2)
    std_len = round(np.std(lengths), 2)
    return mean_len, std_len

def count_paragraph_length(text):
    paragraphs = [p for p in text.splitlines() if p.strip()]
    num_paragraphs = len(paragraphs)
    num_sentences = len(sent_tokenize(text))
    return round(num_sentences / num_paragraphs, 2) if num_paragraphs > 0 else 0

def verb_on_second_position(text):
    sentences = sent_tokenize(text)
    count = 0
    for s in sentences:
        words = word_tokenize(s)
        if len(words) > 1:
            p = morph.parse(words[1])[0]
            if 'VERB' in p.tag:
                count += 1
    return round(count / len(sentences) * 100, 2)

def lemmatized_ratios(text):
    words = simple_preprocess(text)
    total = len(words)
    adj = grnd = pri4 = kotor = 0
    lemmas = set()
    for word in words:
        p = morph.parse(word)[0]
        lemmas.add(p.normal_form)
        if p.normal_form == 'который':
            kotor += 1
        if 'ADJF' in p.tag or 'ADJS' in p.tag:
            adj += 1
        if 'GRND' in p.tag:
            grnd += 1
        if 'PRTF' in p.tag:
            pri4 += 1
    return (
        round(adj / total * 100, 2),
        round(grnd / total * 100, 2),
        round(kotor / total * 100, 2),
        round(pri4 / total * 100, 2),
        round(len(lemmas) / total * 100, 2),
    )

def extract_features(text, author_name, filename):
    mean_len, std_len = count_mean_sentence_length(text)
    adj, grnd, kotor, pri4, uniq = lemmatized_ratios(text)
    bracket = count_brackets(text)
    quote = count_quotes(text)
    dash = count_dashes(text)
    ellipsis = count_ellipsis(text)
    verb2 = verb_on_second_position(text)
    par_len = count_paragraph_length(text)

    return [
        filename, author_name, mean_len, adj, grnd, kotor,
        pri4, bracket, uniq, verb2, par_len,
        std_len, quote, dash, ellipsis
    ]
