import pandas as pd
import os

df = pd.read_csv(r"c:\Users\HP\Desktop\Bootcamp AMA\ckd_dataset.csv")
print("--- ALL COLUMNS ---")
print(list(df.columns))
print("\n--- DATA TYPES ---")
print(df.dtypes.to_string())
print("\n--- SAMPLE DATA (FIRST 3 ROWS) ---")
print(df.head(3).to_string())
print("\n--- MISSING VALUES SUMMARY ---")
print(df.isnull().sum().to_string())
