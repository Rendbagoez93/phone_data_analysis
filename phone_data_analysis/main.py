# Step 1: Connect to preprocess.py
# Step 2: Connect to data_process.py
# Step 3: Connect to visualization.py
# Step 4: Connect to mobile_prediction.py
# Step 5: Connect to main.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.preprocess import preprocess_mobile_data
from src.data_process import process_launched_data
from src.visualization import visualize_launched_phones
from src.mobile_prediction import analyze_mobile_trends

def main():
    # Step 1: Preprocess mobile data
    raw_path = 'data/raw/mobile.csv'
    preprocess_dir = 'data/preprocess'
    preprocess_mobile_data(raw_path, preprocess_dir)

    # Step 2: Process launched data
    launched_input_path = f'{preprocess_dir}/mobile_launched.csv'
    launched_output_path = f'{preprocess_dir}/mobile_launched_cleaned.csv'
    process_launched_data(launched_input_path, launched_output_path)

    # Step 3: Visualize launched phones
    df_launched = pd.read_csv(launched_output_path)
    visualize_launched_phones(df_launched)

    # Step 4: Analyze mobile trends
    analyze_mobile_trends()
    
    print("Mobile data processing and analysis completed.")
    print('=' * 50)
    return

# Save Predicted File to CSV
def save_top_upcoming_brands(df, output_path):
    top_brands = df.sort_values('upcoming_score', ascending=False).head(10)
    top_brands.to_csv(output_path, index=False)

# This function can be called in the main.py file to execute the entire workflow.
if __name__ == "__main__":
    main()