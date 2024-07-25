import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:root@localhost/klasifikasi_nb')

query_training = "SELECT * FROM training"
query_kategori = "SELECT * FROM kategori"

df_training = pd.read_sql(query_training, engine)
df_kategori = pd.read_sql(query_kategori, engine)

# Menampilkan beberapa baris data
print(df_training.head(5))
print(df_kategori['id'])

count_vect = CountVectorizer()
x_train_tf = count_vect.fit_transform(df_training.Judul)
print(x_train_tf)
x_train_tf.shape

tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_tf)
x_train_tfidf.shape

tfidf = TfidfVectorizer()


x_tfidf = tfidf.fit_transform(df_training.Judul).toarray()
print(x_tfidf)


data_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names_out())
print(data_tfidf)
