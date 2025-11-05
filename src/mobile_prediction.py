import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def _safe_read_csv(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)

def _ensure_output_dir(path):
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

def _safe_mode(series, default='Unknown'):
    s = series.dropna()
    if s.empty:
        return default
    m = s.mode()
    return m.iloc[0] if not m.empty else default

def process_mobile_trends(input_path, output_path):
    df = _safe_read_csv(input_path)

    # Safe numeric extraction for RAM and Storage
    if 'RAM' in df.columns:
        ram_extracted = df['RAM'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
        df['RAM_GB'] = pd.to_numeric(ram_extracted, errors='coerce')
    else:
        df['RAM_GB'] = np.nan

    if 'Internal Storage' in df.columns:
        stor_extracted = df['Internal Storage'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
        df['Storage_GB'] = pd.to_numeric(stor_extracted, errors='coerce')
    else:
        df['Storage_GB'] = np.nan

    # Normalize Price to numeric safely
    if 'Price' in df.columns:
        df['Price_numeric'] = pd.to_numeric(df['Price'], errors='coerce')
    else:
        df['Price_numeric'] = np.nan

    # Create price bins only when we have numeric prices
    bins = [0, 2000, 4000, 6000, 8000, 12000, float("inf")]
    labels = ["0-2K(Low)", "2K-4K(Low)", "4K-6K(Mid)", "6K-8K(Mid)", "8K-12K(High)", ">=12K(High)"]
    if df['Price_numeric'].notna().any():
        df['Price Range'] = pd.cut(df['Price_numeric'], bins=bins, labels=labels)
    else:
        df['Price Range'] = pd.Series([np.nan] * len(df))

    # Group and aggregate with safe functions
    agg_dict = {
        "Spec Score": "mean",
        "Rating": "mean",
        "Price_numeric": "mean",
        "Price Range": lambda x: _safe_mode(x, default="Unknown"),
        "Processor Family": lambda x: _safe_mode(x, default="Unknown"),
        "RAM_GB": lambda x: _safe_mode(x, default=np.nan),
        "Storage_GB": lambda x: _safe_mode(x, default=np.nan),
    }

    # Ensure Brand Family exists to group by; if not, create Unknown group
    if 'Brand Family' not in df.columns:
        df['Brand Family'] = 'Unknown'

    trend_df = df.groupby("Brand Family").agg(agg_dict).reset_index()

    # Clean up numeric columns and formatting
    numeric_cols = ["Spec Score", "Rating", "Price_numeric"]
    for c in numeric_cols:
        if c in trend_df.columns:
            trend_df[c] = pd.to_numeric(trend_df[c], errors='coerce')

    if "Spec Score" in trend_df.columns:
        trend_df["Spec Score"] = trend_df["Spec Score"].round(2)
    if "Rating" in trend_df.columns:
        trend_df["Rating"] = trend_df["Rating"].round(2)
    if "Price_numeric" in trend_df.columns:
        trend_df = trend_df.rename(columns={"Price_numeric": "Price"})
        # Format price where present, otherwise keep NaN
        trend_df["Price"] = trend_df["Price"].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "")

    # Ensure output dir and save
    _ensure_output_dir(output_path)
    trend_df = trend_df.sort_values(by="Spec Score", ascending=False, na_position='last')
    trend_df.to_csv(output_path, index=False)

    return trend_df

def visualize_trends(trend_df, title="Trends in Mobile Phones by Brand Family", save_path=None):
    if trend_df is None or trend_df.empty:
        print("No trend data to plot.")
        return
    plt.figure(figsize=(12, 6))
    try:
        sns.lineplot(data=trend_df, x="Brand Family", y="Spec Score", marker="o")
        plt.title(title)
        plt.xlabel("Brand Family")
        plt.ylabel("Specification Score")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        if save_path:
            _ensure_output_dir(save_path)
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        else:
            plt.show()
    except Exception as e:
        print("Plotting failed:", e)
    finally:
        plt.close()

def analyze_mobile_trends():
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    # Launched Phones
    launched_path = 'data/preprocess/mobile_launched_cleaned.csv'
    launched_output = os.path.join(processed_dir, 'brand_family_trends.csv')
    launched_trends = None
    try:
        launched_trends = process_mobile_trends(launched_path, launched_output)
        print("Brand family trends saved to", launched_output)
        print(launched_trends.head())
    except FileNotFoundError:
        print(f"Launched input file not found: {launched_path}")
    except Exception as e:
        print("Error processing launched trends:", e)
    print('=' * 50)

    # Upcoming Phones
    upcoming_path = 'data/preprocess/mobile_upcoming_cleaned.csv'
    upcoming_output = os.path.join(processed_dir, 'upcoming_brand_family_trends.csv')
    upcoming_trends = None
    try:
        upcoming_trends = process_mobile_trends(upcoming_path, upcoming_output)
        print("Upcoming and Rumored brand family trends saved to", upcoming_output)
        if upcoming_trends is not None:
            print("Top 10 Upcoming Brands by Spec Score:")
            print(upcoming_trends.head(10))
    except FileNotFoundError:
        print(f"Upcoming input file not found: {upcoming_path}")
    except Exception as e:
        print("Error processing upcoming trends:", e)
    print('=' * 50)

    # Visualize (save to file to avoid GUI blocking in headless environments)
    if upcoming_trends is not None and not upcoming_trends.empty:
        viz_path = os.path.join(processed_dir, 'upcoming_trends_spec_score.png')
        visualize_trends(upcoming_trends, title="Trends in Upcoming Mobile Phones by Brand Family", save_path=viz_path)

    print("Mobile trends analysis completed.")
    print('=' * 50)
    return launched_trends, upcoming_trends
