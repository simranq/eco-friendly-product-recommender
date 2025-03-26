import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the cleaned dataset
df = pd.read_csv("cleaned_products.csv")

# Convert text data (product descriptions) into numerical format using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['product_description'])

# Compute similarity scores using cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Save the trained model and vectorizer
joblib.dump(cosine_sim, "cosine_sim.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model training complete! Files saved: 'cosine_sim.pkl' and 'vectorizer.pkl'")
