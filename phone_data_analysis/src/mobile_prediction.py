import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def process_mobile_trends(input_path, output_path):
    df = pd.read_csv(input_path)

    # Extract numeric values from storage fields
    df["RAM_GB"] = df["RAM"].str.extract(r"(\d+)").astype(float)
    df["Storage_GB"] = df["Internal Storage"].str.extract(r"(\d+)").astype(float)

    # Create price bins
    bins = [0, 2000, 4000, 6000, 8000, 12000, float("inf")]
    labels = ["0-2K(Low)", "2K-4K(Low)", "4K-6K(Mid)", "6K-8K(Mid)", "8K-12K(High)", "12K-25K(High)"]
    df["Price Range"] = pd.cut(df["Price"], bins=bins, labels=labels)

    trend_df = df.groupby("Brand Family").agg({
        "Spec Score": "mean",
        "Rating": "mean",
        "Price": "mean",
        "Price Range": lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown",
        "Processor Family": lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown",
        "RAM_GB": lambda x: x.mode().iloc[0] if not x.mode().empty else None,
        "Storage_GB": lambda x: x.mode().iloc[0] if not x.mode().empty else None
    }).reset_index()

    numeric_cols = ["Spec Score", "Rating"]
    trend_df[numeric_cols] = trend_df[numeric_cols].round(2)
    trend_df["Price"] = trend_df["Price"].apply(lambda x: f"{x:,.2f}")
    trend_df = trend_df.sort_values(by="Spec Score", ascending=False)
    trend_df.to_csv(output_path, index=False)
    return trend_df

def visualize_trends(trend_df, title="Trends in Mobile Phones by Brand Family"):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=trend_df, x="Brand Family", y="Spec Score", marker="o")
    plt.title(title)
    plt.xlabel("Brand Family")
    plt.ylabel("Specification Score")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analyze_mobile_trends():
    # Launched Phones
    launched_path = 'data/preprocess/mobile_launched_cleaned.csv'
    launched_output = 'data/processed/brand_family_trends.csv'
    launched_trends = process_mobile_trends(launched_path, launched_output)
    print("Brand family trends saved to", launched_output)
    print(launched_trends.head())
    print('=' * 50)

    # Upcoming Phones
    upcoming_path = 'data/preprocess/mobile_upcoming_cleaned.csv'
    upcoming_output = 'data/processed/upcoming_brand_family_trends.csv'
    upcoming_trends = process_mobile_trends(upcoming_path, upcoming_output)
    print("Upcoming and Rumored brand family trends saved to", upcoming_output)
    print("Top 10 Upcoming Brands by Spec Score:")
    print(upcoming_trends.head(10))
    print('=' * 50)

    # Visualize
    visualize_trends(upcoming_trends, title="Trends in Upcoming Mobile Phones by Brand Family")

    print("Mobile trends analysis completed.")
    print('=' * 50)
    return launched_trends, upcoming_trends

# To connect with main.py, you can import and call analyze_mobile_trends()
# Example usage in main.py:
# from mobile_prediction import analyze_mobile_trends
# analyze_mobile_trends()
