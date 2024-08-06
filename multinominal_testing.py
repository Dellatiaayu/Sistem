import pymysql
import pandas as pd
import numpy as np
import string
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import sqlalchemy
from sqlalchemy import create_engine, text
from imblearn.over_sampling import RandomOverSampler
from sklearn.naive_bayes import MultinomialNB
import sys
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Create the engine
engine = create_engine('mysql+pymysql://root:root@localhost/klasifikasi_nb')

# Load data
query_training = "SELECT * FROM training"
query_kategori = "SELECT * FROM kategori"

df_training = pd.read_sql(query_training, engine)
df_kategori = pd.read_sql(query_kategori, engine)

# Display some data
print(df_training.head(5))
print(df_kategori['id'])

# Prepare training data
count_vect = CountVectorizer()
x_train_tf = count_vect.fit_transform(df_training.Judul)
tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_tf)
tfidf = TfidfVectorizer()
x_tfidf = tfidf.fit_transform(df_training.Judul).toarray()

# Resample training data
X_train = x_tfidf
y_train = df_training['id_kategori']
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

# Train model
nb = MultinomialNB().fit(X_train_resampled, y_train_resampled)

# Get testing data
id = sys.argv[1]
data_testing = pd.read_sql(f"SELECT * FROM testing WHERE id = {id}", engine)

# Ensure data_testing['Judul'] is not empty
if data_testing.empty or data_testing['Judul'].isnull().all():
    raise ValueError("The testing data is empty or contains no valid 'Judul' entries.")

# Transform testing data using the same vectorizer and transformer
X_test_tf = count_vect.transform(data_testing['Judul'])
X_test_tfidf = tfidf_transformer.transform(X_test_tf)

# Extract y_test from data_testing
y_test = data_testing['id_kategori']

# Predict
predicted = nb.predict(X_test_tfidf)

# Calculate metrics
acc = accuracy_score(y_test, predicted)
pre = precision_score(y_test, predicted, average='weighted', zero_division=1)
rec = recall_score(y_test, predicted, average='weighted', zero_division=1)
f1 = f1_score(y_test, predicted, average='weighted', zero_division=1)

# Print metrics
print(acc)
print(pre)
print(rec)
print(f1)

# Update database
update_query = text("UPDATE testing SET akurasi = :acc, presisi = :pre, recall = :rec, f1_score = :f1 WHERE id = :id")
with engine.connect() as connection:
    connection.execute(update_query, {"acc": acc, "pre": pre, "rec": rec, "f1": f1, "id": id})
    connection.commit()
