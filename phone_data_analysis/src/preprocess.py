import pandas as pd
import numpy as np
import re
import os

def load_mobile_data(raw_path='data/raw/mobile.csv'):
    df_mobile = pd.read_csv(raw_path)
    return df_mobile

def rename_columns(df):
    df_rename = df.rename(columns={
        'Name': 'Brand Name',
        'Spec Score': 'Spec Score',
        'rating': 'Rating',
        'price': 'Price',
        'img': 'Image Preview',
        'tag': 'Tag',
        'sim': 'SIM / Network',
        'processor': 'Processor',
        'storage': 'Storage',
        'battery': 'Battery',
        'display': 'Display',
        'camera': 'Camera',
        'memoryExternal': 'Memory External',
        'version': 'OS Version',
        'fm': 'FM Radio',
    })
    return df_rename

def initial_cleaning(df):
    image_col = df['Image Preview']
    df_cleaned = df.drop(columns=['Image Preview'])
    df_cleaned['Image Preview'] = image_col
    df_cleaned = df_cleaned.drop(columns=['FM Radio'])
    df_cleaned = df_cleaned.replace(r'^\s*$', np.nan, regex=True)
    df_cleaned = df_cleaned.dropna(how='any')
    return df_cleaned

def standardize_and_fill(df):
    text_cols = ['Brand Name', 'Tag', 'SIM / Network', 'Processor', 'Storage', 'Battery', 'Display', 'Camera', 'Memory External', 'OS Version', 'Image Preview']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.lower()
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Spec Score'] = pd.to_numeric(df['Spec Score'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Spec Score'] = df['Spec Score'].fillna(df['Spec Score'].mean())
    df['Rating'] = df['Rating'].fillna(df['Rating'].mean())
    df['Price'] = df['Price'].fillna(df['Price'].mean())
    df['Battery'] = df['Battery'].fillna('Unknown')
    df['Storage'] = df['Storage'].fillna('Unknown')
    df['Processor'] = df['Processor'].fillna('Unknown')
    df['SIM / Network'] = df['SIM / Network'].fillna('Unknown')
    df['Display'] = df['Display'].fillna('Unknown')
    df['Camera'] = df['Camera'].fillna('Unknown')
    df['Memory External'] = df['Memory External'].fillna('Unknown')
    return df

def split_processor(df):
    df[['Processor Name', 'Processor Type', 'Processor Speed']] = df['Processor'].str.split(',', expand=True)
    df['Processor Name'] = df['Processor Name'].str.strip()
    df['Processor Type'] = df['Processor Type'].str.strip()
    df['Processor Speed'] = df['Processor Speed'].str.strip().str.lower().str.replace('GHz', '').str.strip() + ' GHz'
    df = df.drop(columns=['Processor'])
    return df

def split_sim_network(val):
    parts = [p.strip().lower() for p in str(val).split(',')]
    sim_type = None
    extra_feature = None
    if 'volte' in parts:
        volte_idx = parts.index('volte')
        sim_type = ', '.join(parts[:volte_idx + 1])
        extra_feature = ', '.join(parts[volte_idx + 1:]) if len(parts) > volte_idx + 1 else None
    else:
        sim_type = ', '.join(parts)
        extra_feature = None
    return pd.Series([sim_type, extra_feature])

def split_sim(df):
    df[['SIM Type', 'Extra Feature']] = df['SIM / Network'].apply(split_sim_network)
    df = df.drop(columns=['SIM / Network'])
    return df

def split_storage(df):
    df[['RAM', 'Internal Storage']] = df['Storage'].str.split(',', expand=True)
    df['RAM'] = df['RAM'].str.strip().str.lower()
    df['Internal Storage'] = df['Internal Storage'].str.strip().str.lower()
    df = df.drop(columns=['Storage'])
    return df

def extract_battery_capacity(battery):
    if pd.isna(battery):
        return None
    battery = str(battery).lower()
    match = re.search(r'(\d{3,5})\s*mah', battery)
    if match:
        capacity = match.group(1)
        watt_match = re.search(r'(\d{1,3})\s*w', battery)
        if watt_match:
            return f"{capacity}mAh {watt_match.group(1)}W"
        return f"{capacity}mAh"
    return None

def extract_battery_feature(battery):
    if pd.isna(battery):
        return 'Unknown'
    battery = str(battery).lower()
    if any(x in battery for x in ['fast', 'quick', 'turbo', 'super']):
        return 'Fast Charging'
    return 'Standard Charging'

def split_battery(df):
    df['Battery Capacity'] = df['Battery'].apply(extract_battery_capacity)
    df['Battery Feature'] = df['Battery'].apply(extract_battery_feature)
    return df

def split_display(display):
    display = str(display).lower()
    size_match = re.search(r'(\d+(\.\d+)?)\s*inch', display)
    size = f"{size_match.group(1)} inch" if size_match else None
    res_match = re.search(r'(\d{3,4}\s*x\s*\d{3,4}\s*px)', display)
    resolution = res_match.group(1).replace(' ', '') if res_match else None
    hz_match = re.search(r'(\d{2,3})\s*hz', display)
    if hz_match:
        resolution = f"{resolution}, {hz_match.group(1)} Hz" if resolution else f"{hz_match.group(1)} Hz"
    feature = 'with punch hole' if 'punch hole' in display else 'no punch hole'
    return pd.Series([size, resolution, feature])

def split_display_col(df):
    df[['Display Size', 'Display Resolution', 'Display Feature']] = df['Display'].apply(split_display)
    df = df.drop(columns=['Display'])
    return df

def clean_memory_external(df):
    df['Memory External'] = df['Memory External'].str.strip().str.lower().replace('yes', 'supported').replace('no', 'not supported')
    return df

def rearrange_columns(df):
    cols = ['Brand Name', 'Spec Score', 'Rating', 'Price',
            'Tag', 'Processor Name', 'Processor Type', 'Processor Speed',
            'RAM', 'Internal Storage',
            'Battery Capacity', 'Battery Feature',
            'SIM Type', 'Extra Feature',
            'Display Size', 'Display Resolution', 'Display Feature',
            'Memory External', 'OS Version', 'Camera', 'Image Preview']
    df = df[cols]
    return df

def categorize_by_tag(df):
    categories = {}
    for tag in df['Tag'].unique():
        categories[tag] = df[df['Tag'] == tag].copy()
    return categories

def save_categories(df, out_dir='data/preprocess'):
    launched_df = df[df['Tag'] == 'launched']
    upcoming_rumored_df = df[df['Tag'].isin(['upcoming', 'rumored'])]
    launched_path = os.path.join(out_dir, 'mobile_launched.csv')
    upcoming_path = os.path.join(out_dir, 'mobile_upcoming_rumored.csv')
    launched_df.to_csv(launched_path, index=False)
    upcoming_rumored_df.to_csv(upcoming_path, index=False)
    return launched_path, upcoming_path

def preprocess_mobile_data(raw_path='data/raw/mobile.csv', preprocess_dir='data/preprocess'):
    df_mobile = load_mobile_data(raw_path)
    df_rename = rename_columns(df_mobile)
    df_mobile_cleaned = initial_cleaning(df_rename)
    cleaned_path = os.path.join(preprocess_dir, 'mobile_cleaned.csv')
    df_mobile_cleaned.to_csv(cleaned_path, index=False)

    df_mobile = pd.read_csv(cleaned_path)
    df_mobile = standardize_and_fill(df_mobile)
    df_mobile = split_processor(df_mobile)
    df_mobile = split_sim(df_mobile)
    df_mobile = split_storage(df_mobile)
    df_mobile = split_battery(df_mobile)
    df_mobile = split_display_col(df_mobile)
    df_mobile = clean_memory_external(df_mobile)
    df_mobile = rearrange_columns(df_mobile)
    final_cleaned_path = os.path.join(preprocess_dir, 'mobile_final_cleaned.csv')
    df_mobile.to_csv(final_cleaned_path, index=False)

    df_mobile_cleaned = pd.read_csv(final_cleaned_path)
    save_categories(df_mobile_cleaned, preprocess_dir)

    return df_mobile_cleaned

# Example usage in main.py:
# from preprocess import preprocess_mobile_data
# df = preprocess_mobile_data()
