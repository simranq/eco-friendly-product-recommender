import pandas as pd

# Load dataset
df = pd.read_csv("eco_friendly_products.csv")

# Remove duplicates & missing values
df.dropna(inplace=True)
df.drop_duplicates(subset=['product_name'], inplace=True)

# Convert text to lowercase
df['category'] = df['category'].str.lower()

# Save cleaned data
df.to_csv("cleaned_products.csv", index=False)

print("✅ Data preprocessing complete! Cleaned file saved as 'cleaned_products.csv'")
