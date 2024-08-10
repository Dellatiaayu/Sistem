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
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import sys

# Create the engine
engine = create_engine('mysql+pymysql://root:@localhost/klasifikasi_nb')

# Get the ID from the first parameter
id = sys.argv[1]

# Load data
query_training = "SELECT * FROM training"
df_training = pd.read_sql(query_training, engine)

# Prepare training data
count_vect = CountVectorizer()
x_train_tf = count_vect.fit_transform(df_training.Judul)
tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_tf)
tfidf = TfidfVectorizer()
x_tfidf = tfidf.fit_transform(df_training.Judul).toarray()

# Membagi data menjadi data latih (80%) dan data validasi (20%)
y = df_training['id_kategori']
X_train, X_val, y_train, y_val = train_test_split(x_tfidf, y, test_size=0.2, random_state=42)

# Resample training data
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

# Train model
nb = MultinomialNB().fit(X_train_resampled, y_train_resampled)

# Predict on validation data
predicted_val = nb.predict(X_val)

# Calculate metrics on validation data
acc = accuracy_score(y_val, predicted_val)
pre = precision_score(y_val, predicted_val, average='weighted', zero_division=1)
rec = recall_score(y_val, predicted_val, average='weighted', zero_division=1)
f1 = f1_score(y_val, predicted_val, average='weighted', zero_division=1)

# Print validation metrics
print("Validation Accuracy:", acc)
print("Validation Precision:", pre)
print("Validation Recall:", rec)
print("Validation F1 Score:", f1)

# Tampilkan prediksi kategori dan nilai aktual sebelum update
print("\nPrediksi Kategori vs Kategori Aktual:")
for pred, actual in zip(predicted_val, y_val):
    print(f"Prediksi: {pred}, Aktual: {actual}")

# Get testing data from the database
query_testing = f"SELECT * FROM testing WHERE id = {id}"
df_testing = pd.read_sql(query_testing, engine)

# Ensure testing data is not empty
if df_testing.empty:
    raise ValueError("No testing data found with the provided ID.")

# Transform testing data using the same vectorizer and transformer
X_test_tf = count_vect.transform(df_testing['Judul'])
X_test_tfidf = tfidf_transformer.transform(X_test_tf)

# Predict the category for the testing data
predicted_test = nb.predict(X_test_tfidf)

# Print the predicted category
print("\nPredicted Category for Testing Data:")
for idx, pred in enumerate(predicted_test):
    print(f"Data Testing ID {df_testing['id'].iloc[idx]}: Prediksi Kategori = {pred}")

# Update database with the predicted category and metrics
update_query = text("""
    UPDATE testing 
    SET akurasi = :acc, presisi = :pre, recall = :rec, f1_score = :f1, id_kategori = :pred 
    WHERE id = :id
""")
with engine.connect() as connection:
    connection.execute(update_query, {
        "acc": acc, 
        "pre": pre, 
        "rec": rec, 
        "f1": f1, 
        "pred": predicted_test[0],  # Assuming single record update
        "id": id
    })
    connection.commit()

print(f"\nDatabase updated with the predicted category for ID {id}.")