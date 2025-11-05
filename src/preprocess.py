import pandas as pd
import numpy as np
import re
import os

def load_mobile_data(raw_path='data/raw/mobile.csv'):
    if not os.path.isfile(raw_path):
        raise FileNotFoundError(f"Raw file not found: {raw_path}")
    df_mobile = pd.read_csv(raw_path)
    return df_mobile

def rename_columns(df):
    # Rename columns that actually exist in the input
    col_map = {
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
    }
    existing_map = {k: v for k, v in col_map.items() if k in df.columns}
    return df.rename(columns=existing_map)

def initial_cleaning(df):
    # Work on a copy to avoid chained-assignment issues
    df = df.copy()
    # Preserve Image Preview content if present
    if 'Image Preview' in df.columns:
        image_col = df['Image Preview']
    # Drop FM Radio if present
    if 'FM Radio' in df.columns:
        df = df.drop(columns=['FM Radio'])
    # Replace blank-only strings with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    # Determine essential columns to keep rows for (at least these must be present)
    required = []
    for col in ['Brand Name', 'Price', 'Spec Score', 'Rating', 'Tag']:
        if col in df.columns:
            required.append(col)
    if required:
        df = df.dropna(subset=required, how='any')
    # Restore Image Preview position/content if it existed
    if 'Image Preview' in locals():
        df['Image Preview'] = image_col.reindex(df.index)
    return df

def standardize_and_fill(df):
    df = df.copy()
    # Text columns to normalize (do not lowercase Image Preview to keep URLs)
    text_cols = ['Brand Name', 'Tag', 'SIM / Network', 'Processor', 'Storage', 'Battery', 'Display', 'Camera', 'Memory External', 'OS Version']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    # Numeric conversions with safe defaults
    if 'Price' in df.columns:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        if df['Price'].notna().any():
            df['Price'] = df['Price'].fillna(df['Price'].mean())
    if 'Spec Score' in df.columns:
        df['Spec Score'] = pd.to_numeric(df['Spec Score'], errors='coerce')
        if df['Spec Score'].notna().any():
            df['Spec Score'] = df['Spec Score'].fillna(df['Spec Score'].mean())
    if 'Rating' in df.columns:
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        if df['Rating'].notna().any():
            df['Rating'] = df['Rating'].fillna(df['Rating'].mean())
    # Fill common text columns with Unknown if missing
    for col in ['Battery', 'Storage', 'Processor', 'SIM / Network', 'Display', 'Camera', 'Memory External', 'OS Version']:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
    return df

def split_processor(df):
    if 'Processor' not in df.columns:
        return df
    df = df.copy()
    # split into up to 3 parts; handle variable lengths safely
    parts = df['Processor'].astype(str).str.split(',', n=2)
    df['Processor Name'] = parts.str[0].str.strip().replace('nan', np.nan)
    df['Processor Type'] = parts.str[1].str.strip().replace('nan', np.nan)
    speed = parts.str[2].str.strip().replace('nan', np.nan)
    # normalize speed: remove non-numeric/period and ghz, then append ' GHz' if value found
    def norm_speed(s):
        if pd.isna(s):
            return np.nan
        s = s.lower()
        s = re.sub(r'ghz', '', s)
        s = re.sub(r'[^0-9\.]', '', s)
        return (s + ' GHz') if s else np.nan
    df['Processor Speed'] = speed.apply(norm_speed)
    df = df.drop(columns=['Processor'])
    return df

def split_sim_network(val):
    try:
        parts = [p.strip().lower() for p in str(val).split(',') if p.strip() != '']
    except Exception:
        parts = []
    sim_type = None
    extra_feature = None
    if 'volte' in parts:
        volte_idx = parts.index('volte')
        sim_type = ', '.join(parts[:volte_idx + 1]) if parts[:volte_idx + 1] else None
        extra_feature = ', '.join(parts[volte_idx + 1:]) if len(parts) > volte_idx + 1 else None
    else:
        sim_type = ', '.join(parts) if parts else None
        extra_feature = None
    return pd.Series([sim_type, extra_feature])

def split_sim(df):
    if 'SIM / Network' not in df.columns:
        return df
    df = df.copy()
    df[['SIM Type', 'Extra Feature']] = df['SIM / Network'].apply(split_sim_network)
    df = df.drop(columns=['SIM / Network'])
    return df

def split_storage(df):
    if 'Storage' not in df.columns:
        return df
    df = df.copy()
    # split into up to 2 parts (RAM, Internal Storage)
    parts = df['Storage'].astype(str).str.split(',', n=1)
    df['RAM'] = parts.str[0].str.strip().str.lower().replace('nan', np.nan)
    df['Internal Storage'] = parts.str[1].str.strip().str.lower().replace('nan', np.nan)
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
    if any(x in battery for x in ['fast', 'quick', 'turbo', 'super', 'warp']):
        return 'Fast Charging'
    return 'Standard Charging'

def split_battery(df):
    if 'Battery' not in df.columns:
        return df
    df = df.copy()
    df['Battery Capacity'] = df['Battery'].apply(extract_battery_capacity)
    df['Battery Feature'] = df['Battery'].apply(extract_battery_feature)
    # keep original Battery column removed to avoid redundancy
    df = df.drop(columns=['Battery'])
    return df

def split_display(display):
    display = '' if pd.isna(display) else str(display).lower()
    size_match = re.search(r'(\d+(\.\d+)?)\s*inch', display)
    size = f"{size_match.group(1)} inch" if size_match else None
    res_match = re.search(r'(\d{3,4})\s*[x×]\s*(\d{3,4})\s*(?:px)?', display)
    resolution = None
    if res_match:
        resolution = f"{res_match.group(1)}x{res_match.group(2)}"
    hz_match = re.search(r'(\d{2,3})\s*hz', display)
    if hz_match:
        hz = f"{hz_match.group(1)} Hz"
        resolution = f"{resolution}, {hz}" if resolution else hz
    feature = 'with punch hole' if 'punch hole' in display else 'no punch hole'
    return pd.Series([size, resolution, feature])

def split_display_col(df):
    if 'Display' not in df.columns:
        return df
    df = df.copy()
    df[['Display Size', 'Display Resolution', 'Display Feature']] = df['Display'].apply(split_display)
    df = df.drop(columns=['Display'])
    return df

def clean_memory_external(df):
    if 'Memory External' not in df.columns:
        return df
    df = df.copy()
    vals = df['Memory External'].astype(str).str.strip().str.lower()
    vals = vals.replace({'yes': 'supported', 'y': 'supported', 'true': 'supported', 'no': 'not supported', 'n': 'not supported', 'false': 'not supported'})
    vals = vals.where(~vals.isin(['nan', 'none', 'none', 'unknown']), other='unknown')
    df['Memory External'] = vals
    return df

def rearrange_columns(df):
    preferred = ['Brand Name', 'Spec Score', 'Rating', 'Price',
                'Tag', 'Processor Name', 'Processor Type', 'Processor Speed',
                'RAM', 'Internal Storage',
                'Battery Capacity', 'Battery Feature',
                'SIM Type', 'Extra Feature',
                'Display Size', 'Display Resolution', 'Display Feature',
                'Memory External', 'OS Version', 'Camera', 'Image Preview']
    # keep only columns that exist and preserve their order
    cols = [c for c in preferred if c in df.columns]
    # append any remaining columns at the end to avoid data loss
    remaining = [c for c in df.columns if c not in cols]
    df = df[cols + remaining]
    return df

def categorize_by_tag(df):
    if 'Tag' not in df.columns:
        return {}
    categories = {}
    for tag in df['Tag'].astype(str).str.lower().unique():
        categories[tag] = df[df['Tag'].astype(str).str.lower() == tag].copy()
    return categories

def save_categories(df, out_dir='data/preprocess'):
    os.makedirs(out_dir, exist_ok=True)
    if 'Tag' not in df.columns:
        return None, None
    df = df.copy()
    df['Tag'] = df['Tag'].astype(str).str.lower()
    launched_df = df[df['Tag'] == 'launched']
    upcoming_rumored_df = df[df['Tag'].isin(['upcoming', 'rumored'])]
    launched_path = os.path.join(out_dir, 'mobile_launched.csv')
    upcoming_path = os.path.join(out_dir, 'mobile_upcoming_rumored.csv')
    launched_df.to_csv(launched_path, index=False)
    upcoming_rumored_df.to_csv(upcoming_path, index=False)
    return launched_path, upcoming_path

def preprocess_mobile_data(raw_path='data/raw/mobile.csv', preprocess_dir='data/preprocess'):
    os.makedirs(preprocess_dir, exist_ok=True)
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