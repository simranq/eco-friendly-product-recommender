import streamlit as st
import pandas as pd
import joblib
import os
from stylesheet import custom_stylesheet
st.set_page_config(page_title="Eco-Friendly Product Recommendation", page_icon="logo.jpeg")
st.markdown(custom_stylesheet,unsafe_allow_html=True)
st.markdown("<div class='header'>🌱 Eco-Friendly Product Recommendations</div>", unsafe_allow_html=True)

st.markdown("<p style='color: #2E5733;'>Find sustainable products based on your preferences.</p>", unsafe_allow_html=True)

# Load dataset
if os.path.exists("cleaned_products.csv"):
    df = pd.read_csv("cleaned_products.csv")  # Ensure dataset has necessary columns
else:
    st.error("Error: cleaned_products.csv not found!")
    df = pd.DataFrame()


# Sidebar UI
# st.sidebar.image("logo.jpeg", width=50)  
st.sidebar.header("Filters")
product_type = st.sidebar.selectbox("Select Product Type:", df['category'].unique() if not df.empty else [])
eco_level = st.sidebar.slider("Minimum Eco-Friendly Score:", min_value=1, max_value=10, value=5)

def recommend_products(product_type, eco_level):
    model_filename = f"./models/knn_model_{product_type}.pkl"
    
    if not os.path.exists(model_filename):
        return pd.DataFrame()
    
    knn_model = joblib.load(model_filename)
    
    filtered_df = df[df['category'] == product_type]
    if filtered_df.empty:
        return pd.DataFrame()

    numeric_features = ['eco_friendly_score']
    features = filtered_df[numeric_features]
    
    if features.empty or features.shape[0] < knn_model.n_neighbors:
        return pd.DataFrame()

    distances, indices = knn_model.kneighbors(features)
    recommendations = filtered_df.iloc[indices[0]]
    
    return recommendations[recommendations['eco_friendly_score'] >= eco_level]

if not df.empty:
    if st.sidebar.button("Get Recommendations"):
        recommended_products = recommend_products(product_type, eco_level)
        
        if recommended_products.empty:
            st.warning("No suitable recommendations found.")
        else:
            st.markdown("<div class='product-container'>", unsafe_allow_html=True)

            for _, row in recommended_products.iterrows():
                st.markdown(f"""
                    <div class='product-card'>
                        <img src="{row['image_url']}" alt="Product Image">
                        <p class='product-title'>{row['product_name']}</p>
                        <p class='product-category'><b>Category:</b> {row['category']}</p>
                        <p class='eco-score'>🌱 Eco-Friendly Score: {row['eco_friendly_score']}</p>
                        <p>{row['product_description']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("No dataset available to display.")
   