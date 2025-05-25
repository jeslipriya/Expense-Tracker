import pandas as pd
import os

# Ensure the 'data' folder exists and the CSV file exists, if not, create one
def check_and_create_file(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Create an empty DataFrame and save it to the file
        df = pd.DataFrame(columns=['Category', 'Amount'])
        df.to_csv(file_path, index=False)

# Function to load expenses from CSV
def load_expenses_from_csv(file_path):
    check_and_create_file(file_path)  # Ensure the file exists
    return pd.read_csv(file_path)

# Function to save expenses to CSV
def save_expenses_to_csv(df, file_path):
    df.to_csv(file_path, index=False)