# ...existing code...
import pandas as pd
import re
import os

def _safe_read_csv(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)

def _ensure_output_dir(path):
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

def _first_match_in_list(text, choices):
    text = '' if pd.isna(text) else str(text)
    tl = text.lower()
    for fam in choices:
        if fam.lower() in tl:
            return fam
    return 'Unknown'

def _extract_first_number(text):
    if pd.isna(text):
        return None
    m = re.search(r'\d+\.?\d*', str(text))
    return float(m.group(0)) if m else None

def get_display_size_range(text):
    size = _extract_first_number(text)
    if size is None:
        return 'Unknown'
    if size < 5.0:
        return 'Less than 5 inch'
    if 5.0 <= size < 6.0:
        return '5 to 6 inch'
    if 6.0 <= size < 7.0:
        return '6 to 7 inch'
    return 'More than 7 inch'

def get_battery_capacity_range(text):
    if pd.isna(text):
        return 'Unknown'
    m = re.search(r'(\d{3,5})', str(text))
    if not m:
        return 'Unknown'
    try:
        capacity = int(m.group(1))
    except ValueError:
        return 'Unknown'
    if capacity < 3000:
        return 'Low (<3000mAh)'
    if 3000 <= capacity < 4000:
        return 'Medium (3000 to 4000mAh)'
    if 4000 <= capacity < 5000:
        return 'High (4000 to 5000mAh)'
    return 'Very High (>=5000mAh)'

def _safe_dropna(df, subset):
    cols = [c for c in subset if c in df.columns]
    if not cols:
        return df
    return df.dropna(subset=cols, how='any')

def process_launched_data(input_path='data/preprocess/mobile_launched.csv', output_path='data/preprocess/mobile_launched_cleaned.csv'):
    df_launched = _safe_read_csv(input_path)
    df_launched_cleaned = _safe_dropna(df_launched, ['Brand Name', 'Spec Score', 'Rating', 'Price', 'Processor Name', 'Image Preview'])

    brand_families = ['Alcatel', 'Apple', 'Google', 'Infinix', 'IQOO', 'Itel', 'Motorola',
                      'Nokia', 'OnePlus', 'Oppo', 'Poco', 'Realme', 'Samsung', 'Tecno', 'Vivo',
                      'Xiaomi', 'ZTE']
    df_launched_cleaned['Brand Family'] = df_launched_cleaned.get('Brand Name', pd.Series()).apply(lambda t: _first_match_in_list(t, brand_families) if not pd.isna(t) else 'Unknown')

    processor_families = ['Snapdragon', 'Dimensity', 'Helio', 'Exynos', 'MediaTek', 'Bionic', 'Tensor', 'Unisoc', 'Tiger', 'Intel', 'AMD', 'Qualcomm']
    df_launched_cleaned['Processor Family'] = df_launched_cleaned.get('Processor Name', pd.Series()).apply(lambda t: _first_match_in_list(t, processor_families) if not pd.isna(t) else 'Unknown')

    # Display Size Range
    if 'Display Size' in df_launched_cleaned.columns:
        df_launched_cleaned['Display Size Range'] = df_launched_cleaned['Display Size'].apply(get_display_size_range)
    else:
        df_launched_cleaned['Display Size Range'] = 'Unknown'

    # Battery Capacity Range
    if 'Battery Capacity' in df_launched_cleaned.columns:
        df_launched_cleaned['Battery Capacity Range'] = df_launched_cleaned['Battery Capacity'].apply(get_battery_capacity_range)
    else:
        df_launched_cleaned['Battery Capacity Range'] = 'Unknown'

    _ensure_output_dir(output_path)
    df_launched_cleaned.to_csv(output_path, index=False)
    return df_launched_cleaned

def process_upcoming_data(input_path='data/preprocess/mobile_upcoming_rumored.csv', output_path='data/preprocess/mobile_upcoming_cleaned.csv'):
    df_upcoming = _safe_read_csv(input_path)
    df_upcoming_cleaned = _safe_dropna(df_upcoming, ['Brand Name', 'Spec Score', 'Rating', 'Price', 'Processor Name', 'Image Preview'])

    brand_families = ['Alcatel', 'Apple', 'Google', 'Infinix', 'HTC', 'Honor', 'IQOO', 'Itel', 'Lava', 'Moondrop', 'Motorola',
                      'Nokia', 'Nubia', 'OnePlus', 'Oppo', 'Poco', 'Realme', 'Sharp', 'Samsung', 'Sony Xperia', 'Tecno', 'Tesla', 'Vivo',
                      'Xiaomi', 'ZTE']
    df_upcoming_cleaned['Brand Family'] = df_upcoming_cleaned.get('Brand Name', pd.Series()).apply(lambda t: _first_match_in_list(t, brand_families) if not pd.isna(t) else 'Unknown')

    processor_families = ['Snapdragon', 'Dimensity', 'Helio', 'Exynos', 'MediaTek', 'Bionic', 'Tensor', 'Unisoc', 'Tiger', 'Intel', 'AMD', 'Qualcomm', 'Apple', 'Xring']
    df_upcoming_cleaned['Processor Family'] = df_upcoming_cleaned.get('Processor Name', pd.Series()).apply(lambda t: _first_match_in_list(t, processor_families) if not pd.isna(t) else 'Unknown')

    if 'Display Size' in df_upcoming_cleaned.columns:
        df_upcoming_cleaned['Display Size Range'] = df_upcoming_cleaned['Display Size'].apply(get_display_size_range)
    else:
        df_upcoming_cleaned['Display Size Range'] = 'Unknown'

    if 'Battery Capacity' in df_upcoming_cleaned.columns:
        df_upcoming_cleaned['Battery Capacity Range'] = df_upcoming_cleaned['Battery Capacity'].apply(get_battery_capacity_range)
    else:
        df_upcoming_cleaned['Battery Capacity Range'] = 'Unknown'

    _ensure_output_dir(output_path)
    df_upcoming_cleaned.to_csv(output_path, index=False)
    return df_upcoming_cleaned
