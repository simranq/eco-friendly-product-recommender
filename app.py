import streamlit as st
import pandas as pd
import joblib

# Load dataset and trained models
df = pd.read_csv("cleaned_products.csv")
cosine_sim = joblib.load("cosine_sim.pkl")

# Set page config with favicon
st.set_page_config(
    page_title="Eco-Friendly Product Recommender",
    page_icon="proj-favicon.jpg",  # Set favicon
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Playfair+Display:wght@600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        .stApp { background-color: #F5F1E3; padding: 40px; }
        .header-container { text-align: center; margin-bottom: 40px; }
        .header { 
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            padding: 30px;
            background: #A7C7A4;
            color: #2E5733;
            font-size: 42px;
            font-weight: 600;
            font-family: 'Playfair Display', serif;
            border-radius: 12px;
        }
        .header img { width: 50px; height: 50px; border-radius: 50%; }
    </style>
""", unsafe_allow_html=True)

# Display Logo and Header
st.markdown("""
    <div class="header-container">
        <div class="header">
            <img src="proj-favicon.jpg" alt="logo">
            🌿 Eco-Friendly Product Recommendation
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("Find the best sustainable alternatives that fit your eco-conscious lifestyle.")
