import requests
import pandas as pd
import os

url = "https://docs.google.com/spreadsheets/d/1a4iZPf93nLejpL7d7LYnF9JliV10etsJS8ia-bw1MXg/export?format=csv"
output_path = r"c:\Users\HP\Desktop\Bootcamp AMA\ckd_dataset.csv"

try:
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Successfully downloaded dataset to {output_path}")
    
    df = pd.read_csv(output_path)
    print("--- DATASET PREVIEW ---")
    print(df.head())
    print("\n--- DATASET INFO ---")
    print(df.info())
except Exception as e:
    print(f"Error: {e}")
