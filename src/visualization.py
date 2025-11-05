# ...existing code...
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def _ensure_output_dir(path):
    if not path:
        return
    os.makedirs(path, exist_ok=True)

def _save_or_show(fig_name, save_dir, show):
    if save_dir:
        _ensure_output_dir(save_dir)
        path = os.path.join(save_dir, fig_name)
        try:
            plt.savefig(path, dpi=150, bbox_inches='tight')
        except Exception:
            pass
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

def _plot_hist(df, col, title, xlabel, save_dir, show):
    if col not in df.columns or df[col].dropna().empty:
        return
    data = pd.to_numeric(df[col], errors='coerce').dropna()
    if data.empty:
        return
    plt.figure(figsize=(12, 6))
    sns.histplot(data, bins=30, kde=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    _save_or_show(f"{col.replace(' ', '_')}_hist.png", save_dir, show)

def _plot_count(df, col, title, xlabel, save_dir, show):
    if col not in df.columns or df[col].dropna().empty:
        return
    plt.figure(figsize=(14, 7))
    order = df[col].value_counts().index
    try:
        sns.countplot(data=df, x=col, order=order)
    except Exception:
        sns.countplot(data=df, x=col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    _save_or_show(f"{col.replace(' ', '_')}_count.png", save_dir, show)

def visualize_launched_phones(df_launched, save_dir='data/figures', show=False):
    if df_launched is None or df_launched.empty:
        print("No launched data to visualize.")
        return
    print(df_launched.head())
    print('=' * 50)

    _plot_hist(df_launched, 'Spec Score', 'Distribution of Specification Scores in Launched Phones', 'Specification Score', save_dir, show)
    _plot_hist(df_launched, 'Price', 'Distribution of Prices in Launched Phones', 'Price', save_dir, show)
    _plot_hist(df_launched, 'Rating', 'Distribution of Ratings in Launched Phones', 'Rating', save_dir, show)

    _plot_count(df_launched, 'Brand Family', 'Count of Launched Phones by Brand Family', 'Brand Family', save_dir, show)
    _plot_count(df_launched, 'Processor Family', 'Count of Launched Phones by Processor Family', 'Processor Family', save_dir, show)
    _plot_count(df_launched, 'RAM', 'Count of Launched Phones by RAM', 'RAM', save_dir, show)
    _plot_count(df_launched, 'Internal Storage', 'Count of Launched Phones by Internal Storage', 'Internal Storage', save_dir, show)
    _plot_count(df_launched, 'Battery Capacity Range', 'Count of Launched Phones by Battery Capacity Range', 'Battery Capacity Range', save_dir, show)

    print("Visualizations for launched phones completed.")
    print('=' * 50)

def visualize_upcoming_phones(df_upcoming_rumored, save_dir='data/figures', show=False):
    if df_upcoming_rumored is None or df_upcoming_rumored.empty:
        print("No upcoming/rumored data to visualize.")
        return
    print(df_upcoming_rumored.head())
    print('=' * 50)

    _plot_hist(df_upcoming_rumored, 'Spec Score', 'Distribution of Specification Scores in Upcoming and Rumored Phones', 'Specification Score', save_dir, show)
    _plot_hist(df_upcoming_rumored, 'Price', 'Distribution of Prices in Upcoming and Rumored Phones', 'Price', save_dir, show)
    _plot_hist(df_upcoming_rumored, 'Rating', 'Distribution of Ratings in Upcoming and Rumored Phones', 'Rating', save_dir, show)

    _plot_count(df_upcoming_rumored, 'Brand Family', 'Count of Upcoming and Rumored Phones by Brand Family', 'Brand Family', save_dir, show)
    _plot_count(df_upcoming_rumored, 'Processor Family', 'Count of Upcoming and Rumored Phones by Processor Family', 'Processor Family', save_dir, show)
    _plot_count(df_upcoming_rumored, 'RAM', 'Count of Upcoming and Rumored Phones by RAM', 'RAM', save_dir, show)
    _plot_count(df_upcoming_rumored, 'Internal Storage', 'Count of Upcoming and Rumored Phones by Internal Storage', 'Internal Storage', save_dir, show)
    _plot_count(df_upcoming_rumored, 'Battery Capacity Range', 'Count of Upcoming and Rumored Phones by Battery Capacity Range', 'Battery Capacity Range', save_dir, show)
    _plot_count(df_upcoming_rumored, 'Display Size Range', 'Count of Upcoming and Rumored Phones by Display Size Range', 'Display Size Range', save_dir, show)

    print("Visualizations for upcoming and rumored phones completed.")
    print('=' * 50)

def load_launched_data(path='data/preprocess/mobile_launched_cleaned.csv'):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)

def load_upcoming_data(path='data/preprocess/mobile_upcoming_cleaned.csv'):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)
