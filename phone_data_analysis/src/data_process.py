import pandas as pd
import numpy as np
import re

def process_launched_data(input_path='data/preprocess/mobile_launched.csv', output_path='data/preprocess/mobile_launched_cleaned.csv'):
    df_launched = pd.read_csv(input_path)
    df_launched_cleaned = df_launched.dropna(subset=['Brand Name', 'Spec Score', 'Rating', 'Price', 'Processor Name', 'Image Preview'])

    brand_families = ['Alcatel', 'Apple', 'Google', 'Infinix', 'IQOO', 'Itel', 'Motorola', 
                      'Nokia', 'OnePlus', 'Oppo', 'Poco', 'Realme', 'Samsung', 'Tecno', 'Vivo', 
                      'Xiaomi', 'ZTE']
    def get_brand_family(text):
        for fam in brand_families:
            if fam.lower() in str(text).lower():
                return fam
        return 'Unknown'
    df_launched_cleaned.insert(
        df_launched_cleaned.columns.get_loc('Brand Name') + 1,
        'Brand Family',
        df_launched_cleaned['Brand Name'].apply(get_brand_family)
    )

    processor_families = ['Snapdragon', 'Dimensity', 'Helio', 'Exynos', 'MediaTek', 'Bionic', 'Tensor', 'Unisoc', 'Tiger', 'Intel', 'AMD', 'Qualcomm']
    def get_processor_family(text):
        for fam in processor_families:
            if fam.lower() in str(text).lower():
                return fam
        return 'Unknown'
    df_launched_cleaned.insert(
        df_launched_cleaned.columns.get_loc('Processor Name') + 1,
        'Processor Family',
        df_launched_cleaned['Processor Name'].apply(get_processor_family)
    )

    def get_display_size_range(text):
        if 'inch' in str(text).lower():
            size = re.findall(r'\d+\.?\d*', str(text))
            if size:
                size = float(size[0])
                if size < 5.0:
                    return 'Less than 5 inch'
                elif 5.0 <= size < 6.0:
                    return '5 to 6 inch'
                elif 6.0 <= size < 7.0:
                    return '6 to 7 inch'
                else:
                    return 'More than 7 inch'
        return 'Unknown'
    df_launched_cleaned.insert(
        df_launched_cleaned.columns.get_loc('Display Size') + 1,
        'Display Size Range',
        df_launched_cleaned['Display Size'].apply(get_display_size_range)
    )

    def get_battery_capacity_range(text):
        if 'mah' in str(text).lower():
            capacity = re.findall(r'\d+', str(text))
            if capacity:
                capacity = int(capacity[0])
                if capacity < 3000:
                    return 'Low (<3000mAh)'
                elif 3000 <= capacity < 4000:
                    return 'Medium (3000 to 4000mAh)'
                elif 4000 <= capacity < 5000:
                    return 'High (4000 to 5000mAh)'
                else:
                    return 'Very High (>=5000mAh)'
        return 'Unknown'
    df_launched_cleaned.insert(
        df_launched_cleaned.columns.get_loc('Battery Capacity') + 1,
        'Battery Capacity Range',
        df_launched_cleaned['Battery Capacity'].apply(get_battery_capacity_range)
    )

    df_launched_cleaned.to_csv(output_path, index=False)
    return df_launched_cleaned

def process_upcoming_data(input_path='data/preprocess/mobile_upcoming_rumored.csv', output_path='data/preprocess/mobile_upcoming_cleaned.csv'):
    df_upcoming = pd.read_csv(input_path)
    df_upcoming_cleaned = df_upcoming.dropna(subset=['Brand Name', 'Spec Score', 'Rating', 'Price', 'Processor Name', 'Image Preview'])

    brand_families = ['Alcatel', 'Apple', 'Google', 'Infinix', 'HTC', 'Honor', 'IQOO', 'Itel', 'Lava', 'Moondrop', 'Motorola', 
                      'Nokia', 'Nubia', 'OnePlus', 'Oppo', 'Poco', 'Realme', 'Sharp', 'Samsung', 'Sony Xperia', 'Tecno', 'Tesla', 'Vivo', 
                      'Xiaomi', 'ZTE']
    def get_brand_family(text):
        for fam in brand_families:
            if fam.lower() in str(text).lower():
                return fam
        return 'Unknown'
    df_upcoming_cleaned.insert(
        df_upcoming_cleaned.columns.get_loc('Brand Name') + 1,
        'Brand Family',
        df_upcoming_cleaned['Brand Name'].apply(get_brand_family)
    )

    processor_families = ['Snapdragon', 'Dimensity', 'Helio', 'Exynos', 'MediaTek', 'Bionic', 'Tensor', 'Unisoc', 'Tiger', 'Intel', 'AMD', 'Qualcomm', 'Apple', 'Xring']
    def get_processor_family(text):
        for fam in processor_families:
            if fam.lower() in str(text).lower():
                return fam
        return 'Unknown'
    df_upcoming_cleaned.insert(
        df_upcoming_cleaned.columns.get_loc('Processor Name') + 1,
        'Processor Family',
        df_upcoming_cleaned['Processor Name'].apply(get_processor_family)
    )

    def get_display_size_range(text):
        if 'inch' in str(text).lower():
            size = re.findall(r'\d+\.?\d*', str(text))
            if size:
                size = float(size[0])
                if size < 5.0:
                    return 'Less than 5 inch'
                elif 5.0 <= size < 6.0:
                    return '5 to 6 inch'
                elif 6.0 <= size < 7.0:
                    return '6 to 7 inch'
                else:
                    return 'More than 7 inch'
        return 'Unknown'
    df_upcoming_cleaned.insert(
        df_upcoming_cleaned.columns.get_loc('Display Size') + 1,
        'Display Size Range',
        df_upcoming_cleaned['Display Size'].apply(get_display_size_range)
    )

    def get_battery_capacity_range(text):
        if 'mah' in str(text).lower():
            capacity = re.findall(r'\d+', str(text))
            if capacity:
                capacity = int(capacity[0])
                if capacity < 3000:
                    return 'Low (<3000mAh)'
                elif 3000 <= capacity < 4000:
                    return 'Medium (3000 to 4000mAh)'
                elif 4000 <= capacity < 5000:
                    return 'High (4000 to 5000mAh)'
                else:
                    return 'Very High (>=5000mAh)'
        return 'Unknown'
    df_upcoming_cleaned.insert(
        df_upcoming_cleaned.columns.get_loc('Battery Capacity') + 1,
        'Battery Capacity Range',
        df_upcoming_cleaned['Battery Capacity'].apply(get_battery_capacity_range)
    )

    df_upcoming_cleaned.to_csv(output_path, index=False)
    return df_upcoming_cleaned
