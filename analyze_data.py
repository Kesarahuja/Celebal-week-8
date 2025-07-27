import pandas as pd

def analyze_data(file_path):
    df = pd.read_csv(file_path)
    print(f"\n--- Data Analysis for {file_path} ---")
    print("Shape:", df.shape)
    print("\nColumns and their data types:")
    df.info(verbose=True, show_counts=True)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nDescriptive statistics:")
    print(df.describe(include='all'))
    print("\nUnique values for categorical columns:")
    for column in df.select_dtypes(include='object').columns:
        print(f"{column}: {df[column].unique()}")

analyze_data("/home/ubuntu/upload/TrainingDataset.csv")
analyze_data("/home/ubuntu/upload/TestDataset.csv")

