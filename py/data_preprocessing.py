import pandas as pd
import os

def process(inp):
    # Extract filename only (removes folder path)
    filename = os.path.basename(inp)

    # Load dataset with error handling
    df = pd.read_csv(inp, encoding="utf-8", engine="python")

    # Remove duplicates & missing values
    df.dropna(inplace=True)
    df.drop_duplicates(subset=['Product Name'], inplace=True)

    # Convert text to lowercase
    df['Category'] = df['Category'].str.lower()

    # Ensure output directory exists
    output_dir = "cleaned_data"
    os.makedirs(output_dir, exist_ok=True)  # ✅ Creates directory if missing

    # Save cleaned data
    output_path = os.path.join(output_dir, f"cleaned_{filename}")
    df.to_csv(output_path, index=False)

    print(f"✅ Data preprocessing complete! Cleaned file saved as '{output_path}'")

if __name__ == '__main__':
    list_of_raw_data = [
        "raw_data/eco_friendly_products_10k.csv",
        "raw_data/eco_friendly_products_20k.csv",
        "raw_data/eco_friendly_products_50k.csv",
        "raw_data/eco_friendly_products_100k.csv"
    ]
    for file in list_of_raw_data:
        process(file)
