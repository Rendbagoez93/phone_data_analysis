import pandas as pd


from src.preprocess import preprocess_mobile_data
from src.data_process import process_launched_data
from src.visualization import visualize_launched_phones
from src.mobile_prediction import analyze_mobile_trends

def main():
    raw_path = 'data/raw/mobile.csv'
    preprocess_dir = 'data/preprocess'
    try:
        preprocess_mobile_data(raw_path, preprocess_dir)
        print("Preprocessing completed.")
    except Exception as e:
        print("Preprocess failed:", e)
        return

    launched_input_path = f'{preprocess_dir}/mobile_launched.csv'
    launched_output_path = f'{preprocess_dir}/mobile_launched_cleaned.csv'
    try:
        process_launched_data(launched_input_path, launched_output_path)
        print("Launched data processing completed.")
    except Exception as e:
        print("Processing launched data failed:", e)

    # Visualize launched phones if cleaned file exists
    try:
        df_launched = pd.read_csv(launched_output_path)
        if not df_launched.empty:
            visualize_launched_phones(df_launched)
    except FileNotFoundError:
        print(f"Launched cleaned file not found: {launched_output_path}")
    except Exception as e:
        print("Visualization failed:", e)

    # Analyze mobile trends and capture returned trends
    try:
        launched_trends, upcoming_trends = analyze_mobile_trends()
    except Exception as e:
        print("Trend analysis failed:", e)
        launched_trends, upcoming_trends = None, None

    # Save top upcoming brands by Spec Score if available
    try:
        if upcoming_trends is not None and 'Spec Score' in upcoming_trends.columns:
            top_path = 'data/processed/top_upcoming_brands_by_spec_score.csv'
            top_brands = upcoming_trends.sort_values('Spec Score', ascending=False).head(10)
            top_brands.to_csv(top_path, index=False)
            print("Top upcoming brands saved to", top_path)
    except Exception as e:
        print("Saving top upcoming brands failed:", e)

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