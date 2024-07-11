import pandas as pd
import numpy as np
import string
import re

# Menampilkan Data Training
data= pd.read_csv('Data Training.csv')
data.head(50)

# Tahapan Text Prepocessing

# Proses Cleanning
def clean_text(Judul):
    # Menghilangkan Tanda Baca
    Judul = Judul.translate(str.maketrans(' ',' ',string.punctuation))
    # Mempertimbangkan Huruf dan Angka
    Judul = re.sub('[^a-zA-Z]',' ',Judul)
    # Menghapus single char
    Judul = re.sub(r"\b[a-zA-Z]\b"," ",Judul)
    # Memisahkan dan menggabungkan kata
    Judul = ' '.join(Judul.split())
    return Judul

# Proses Case Folding
def case_folding(Judul):
    # Mengubah Menjadi Huruf Kecil
    Judul = Judul.lower()
    return Judul

# Proses Tokenizing

# Mengubah kalimat menjadi kata
from nltk.tokenize import RegexpTokenizer
regexp = RegexpTokenizer(r'\w+|$[0-9]+|\S+')
data['Judul'] = data['Judul'].apply(regexp.tokenize)

# Proses Filtering

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def stopword_removal(Judul):
    filtering = stopwords.words('indonesian','english')
    x = []
    data = []
    def myFunc(x):
        if x in filtering:
            return False
        else:
            return True
    fit = filter(myFunc, Judul)
    for x in fit:
        data.append(x)
    return data
data['Judul'] = data['Judul'].apply(stopword_removal)

# Proses Stemming

from sklearn.pipeline import Pipeline
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming(Judul):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    do = []
    for w in Judul:
        dt = stemmer.stem(w)
        do.append(dt)
    d_clean = []
    d_clean = " ".join(do)
    print (d_clean)
    return d_clean
data['Judul'] = data['Judul'].apply(stemming)

data.to_csv('data_clean.csv', index=False)
data_clean = pd.read_csv('data_clean.csv',encoding='latin')
data_clean.head(50)