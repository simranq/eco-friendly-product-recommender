import streamlit as st
import pandas as pd
import joblib

# Load dataset and trained models
df = pd.read_csv("cleaned_products.csv")
cosine_sim = joblib.load("cosine_sim.pkl")

# Define recommendation function
def recommend_products(product_name, eco_level):
    if product_name not in df['product_name'].values:
        return pd.DataFrame()

    idx = df[df['product_name'] == product_name].index[0]
    similar_products = list(enumerate(cosine_sim[idx]))
    sorted_products = sorted(similar_products, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = df.iloc[[i[0] for i in sorted_products]][['product_name', 'category', 'eco_friendly_score', 'image_url', 'product_description']]
    return recommendations[recommendations['eco_friendly_score'] >= eco_level]

# Streamlit UI Configuration
st.set_page_config(page_title="Eco-Friendly Product Recommender", layout="wide")

# Apply Custom Styling with Perfect Margins & Elegant Typography
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Playfair+Display:wght@600&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
        }
        .stApp {
            background-color: #F5F1E3;
            padding: 40px;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: #A7C7A4;
            color: #2E5733;
            font-size: 42px;
            font-weight: 600;
            font-family: 'Playfair Display', serif;
            border-radius: 12px;
            margin-bottom: 40px;
        }
        .product-container {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
            justify-content: center;
            padding: 20px;
        }
        .product-card {
            background: #FFFFFF;
            padding: 25px;
            border-radius: 18px;
            text-align: center;
            box-shadow: 2px 4px 12px rgba(0,0,0,0.12);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            width: 280px;
            margin-bottom: 20px;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 4px 6px 18px rgba(0,0,0,0.15);
        }
        .product-card img {
            width: 160px;
            height: auto;
            display: block;
            margin: 15px auto;
            border-radius: 12px;
        }
        .product-title {
            font-size: 22px;
            font-weight: 600;
            color: #3B5D3A;
            margin-bottom: 5px;
        }
        .product-category {
            font-size: 14px;
            color: #6B6B6B;
            margin-bottom: 10px;
        }
        .eco-score {
            font-size: 16px;
            font-weight: bold;
            color: #2E5733;
            background-color: #E6EFE9;
            padding: 6px 12px;
            border-radius: 10px;
            display: inline-block;
            margin-top: 5px;
        }
        .sidebar .block-container {
            background: #E6EFE9;
            padding: 20px;
            border-radius: 12px;
        }
        .stButton>button {
            background-color: #6F9868;
            color: white;
            padding: 10px 18px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
            border: none;
        }
        .stButton>button:hover {
            background-color: #4E7D57;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# Title with Elegant Font
st.markdown('<div class="header">🌿 Eco-Friendly Product Recommendation</div>', unsafe_allow_html=True)
st.write("Find the best sustainable alternatives that fit your eco-conscious lifestyle.")

# Sidebar for Filters
st.sidebar.header("🔎 Filters")
search_term = st.sidebar.text_input("Search for a product:")
filtered_products = df[df['product_name'].str.contains(search_term, case=False, na=False)]

# Product Selection & Eco Score
product_name = st.sidebar.selectbox("Select a product:", filtered_products['product_name'].values)
eco_level = st.sidebar.slider("Minimum Eco-Friendliness Score:", 1, 10, 5)

# Display Recommendations
if st.sidebar.button("Get Recommendations"):
    recommendations = recommend_products(product_name, eco_level)

    if recommendations.empty:
        st.warning("No products match the selected eco-friendliness level.")
    else:
        st.success(f"🌱 Top sustainable alternatives for **{product_name}**:")

        # Display Products in a Flexbox Layout
        st.markdown('<div class="product-container">', unsafe_allow_html=True)
        for idx, row in recommendations.iterrows():
            st.markdown(f"""
                <div class="product-card">
                    <img src="{row['image_url']}" alt="{row['product_name']}">
                    <p class="product-title">{row['product_name']}</p>
                    <p class="product-category">{row['category']}</p>
                    <p class="eco-score">🌎 Eco Score: {row['eco_friendly_score']}/10</p>
                    <p>{row['product_description']}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
