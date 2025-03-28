import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import os

df = pd.read_csv("cleaned_products.csv", encoding="utf-8")

# Train separate models for each category
category_models = {}

for category in df["category"].unique():
    category_df = df[df["category"] == category]
    # if category_df.shape[0] < 5:  # Ensure at least 5 products exist
    #     continue
    
    X = category_df[["eco_friendly_score"]]
    knn = NearestNeighbors(n_neighbors=min(5, X.shape[0]), metric="euclidean")
    knn.fit(X)
    
    model_filename = f"knn_model_{category}.pkl"
    joblib.dump(knn, model_filename)
    print(model_filename)
    category_models[category] = model_filename

print("Training complete. Models saved per category.")
