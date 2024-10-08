import pandas as pd
import numpy as np
import string
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

query = "SELECT * FROM training"
df = pd.read_sql(query, engine)
print(df.columns)

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
# Menampilkan hasil proses cleanning
df['Judul'] = df['Judul'].apply(clean_text)

# Proses Case Folding
def case_folding(Judul):
    # Mengubah Menjadi Huruf Kecil
    Judul = Judul.lower()
    return Judul

# Menampilkan hasil proses case folding
df['Judul'] = df['Judul'].apply(case_folding)

# Proses Tokenizing

# Mengubah kalimat menjadi kata
regexp = RegexpTokenizer(r'\w+|$[0-9]+|\S+')
df['Judul'] = df['Judul'].apply(regexp.tokenize)

# Proses Filtering

def stopword_removal(Judul):
    # filtering = stopwords.words('indonesian','english')
    # x = []
    # data = []
    # def myFunc(x):
    #     if x in filtering:
    #         return False
    #     else:
    #         return True
    # fit = filter(myFunc, Judul)
    # for x in fit:
    #     data.append(x)
    # return data
    filtering = stopwords.words('indonesian') + stopwords.words('english')
    return [word for word in Judul if word not in filtering]

df['Judul'] = df['Judul'].apply(stopword_removal)


# Proses Stemming

# Proses Stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stemming(Judul):
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    # do = []
    # for w in Judul:
    #     dt = stemmer.stem(w)
    #     do.append(dt)
    # d_clean = []
    # d_clean = " ".join(do)
    # print (d_clean)
    # return d_clean
    return " ".join([stemmer.stem(word) for word in Judul])

df['Judul'] = df['Judul'].apply(stemming)

# data.to_csv('data_clean.csv', index=False)
# data_clean = pd.read_csv('data_clean.csv',encoding='latin')
# data_clean.head(50)


# update tabel training
update_table_training = "UPDATE training SET Judul = :judul WHERE id = :id"
cleaned_data = [{'judul': row['Judul'], 'id': row['id']} for index, row in df.iterrows()]

# Debug: Cetak data yang akan dikirim ke query
print(cleaned_data[:5]) 

# Eksekusi query update
with engine.connect() as connection:
    for data in cleaned_data:
        print(f"Updating id {data['id']} with judul {data['judul']}")  # Debug statement sebelum update
        connection.execute(sqlalchemy.text(update_table_training), data)
        print(f"Updated id {data['id']}")  # Debug statement setelah update
    connection.commit()