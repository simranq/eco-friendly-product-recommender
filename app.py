import streamlit as st
import pandas as pd
import joblib

# Load dataset and trained models
df = pd.read_csv("cleaned_products.csv")
cosine_sim = joblib.load("cosine_sim.pkl")

# Set page config with favicon
st.set_page_config(
    page_title="Eco-Friendly Product Recommender",
    page_icon="proj-favicon.jpg",  # Add favicon
    layout="wide"
)

# Display logo at the top
st.image("proj-favicon.jpg", width=100)

# Define recommendation function
def recommend_products(product_name, eco_level):
    if product_name not in df['product_name'].values:
        return pd.DataFrame()

    idx = df[df['product_name'] == product_name].index[0]
    similar_products = list(enumerate(cosine_sim[idx]))
    sorted_products = sorted(similar_products, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = df.iloc[[i[0] for i in sorted_products]][['product_name', 'category', 'eco_friendly_score', 'image_url', 'product_description']]
    return recommendations[recommendations['eco_friendly_score'] >= eco_level]

# Title with Elegant Font
st.markdown('<div class="header"><img src="proj-favicon.jpg" width="50"> Eco-Friendly Product Recommendation</div>', unsafe_allow_html=True)
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
