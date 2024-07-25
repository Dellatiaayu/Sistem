import pymysql
import pandas as pd
import numpy as np
import string
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

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