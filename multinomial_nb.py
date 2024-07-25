import pymysql
import pandas as pd
import numpy as np
import string
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='klasifikasi_nb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

query_training = "SELECT * FROM training"
query_kategori = "SELECT * FROM kategori"

df_training = pd.read_sql(query_training, connection)
df_kategori = pd.read_sql(query_kategori, connection)

# Menggabungkan tabel training dan kategori
df = pd.merge(df_training, df_kategori, left_on='id_kategori', right_on='id', how='left', suffixes=('', '_kategori'))

# Menghapus kolom
df.drop(columns=['id_kategori', 'id_kategori_kategori'], inplace=True)


# Menampilkan beberapa baris data
df.head(50)

# def polaritas(teks):
#     if teks =='Imposter Content':
#         return 1
#     elif teks =='Misleading Content':
#         return 2
#     elif teks =='Fabricated Content':
#         return 3
#     else:
#         return 4

    
# df['label'] = df['Kategori'].apply(polaritas)
# df


# X = df['Judul']
# y = df['label']


# from sklearn.feature_extraction.text import CountVectorizer
# count_vect = CountVectorizer()
# x_train_tf = count_vect.fit_transform(df.Judul)
# print(x_train_tf)
# x_train_tf.shape


# from sklearn.feature_extraction.text import TfidfTransformer

# tfidf_transformer = TfidfTransformer()
# x_train_tfidf = tfidf_transformer.fit_transform(x_train_tf)
# x_train_tfidf.shape


# from sklearn.feature_extraction.text import TfidfVectorizer

# tfidf = TfidfVectorizer()


# x_tfidf = tfidf.fit_transform(X).toarray()
# x_tfidf


# data_tfidf = pd.DataFrame(x_tfidf, columns=tfidf.get_feature_names_out())
# data_tfidf


# import pandas as pd
# import numpy as np
# import string
# import re

# data_testing = pd.read_csv('Hasil TP Data Testing.csv')
# data_testing.head(5)


# X_train = x_tfidf
# X_test = data_testing['Judul']
# y_train = df['Kategori']
# y_test = data_testing['Kategori']


# from imblearn.over_sampling import RandomOverSampler

# ros = RandomOverSampler(random_state=42)
# X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)


# from sklearn.naive_bayes import MultinomialNB

# nb = MultinomialNB().fit(X_train_resampled, y_train_resampled)


# X_test_tf = count_vect.transform(X_test)

# X_test_tfidf = tfidf_transformer.fit_transform(X_test_tf)
# predicted = nb.predict(X_test_tfidf)
# predicted


# from sklearn.metrics import confusion_matrix

# cm = confusion_matrix(y_test, predicted)
# print('Confusion matrix:\n', cm)


# from sklearn.metrics import classification_report

# print('Classification report:\n', classification_report(y_test, predicted, zero_division=1))


# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# acc = accuracy_score(y_test, predicted)
# pre = precision_score(y_test, predicted, average='weighted', zero_division=1)
# rec = recall_score(y_test, predicted, average='weighted', zero_division=1)
# f1 = f1_score(y_test, predicted, average='weighted', zero_division=1)

# print("Akurasi: ", acc)
# print("presisi: ", pre)
# print("Recall: ", rec)
# print("F1_score: ", f1)