import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def visualize_launched_phones(df_launched):
    print(df_launched.head())
    print('=' * 50)

    # Distribution of Spec Scores
    plt.figure(figsize=(12, 6))
    sns.histplot(df_launched['Spec Score'], bins=30, kde=True)
    plt.title('Distribution of Specification Scores in Launched Phones')
    plt.xlabel('Specification Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Price Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df_launched['Price'], bins=30, kde=True)
    plt.title('Distribution of Prices in Launched Phones')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Rating Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df_launched['Rating'], bins=30, kde=True)
    plt.title('Distribution of Ratings in Launched Phones')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Brand Family Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_launched, x='Brand Family', order=df_launched['Brand Family'].value_counts().index)
    plt.title('Count of Launched Phones by Brand Family')
    plt.xlabel('Brand Family')
    plt.ylabel('Number of Phones Launched')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Processor Family Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_launched, x='Processor Family', order=df_launched['Processor Family'].value_counts().index)
    plt.title('Count of Launched Phones by Processor Family')
    plt.xlabel('Processor Family')
    plt.ylabel('Number of Phones Launched')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # RAM Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_launched, x='RAM', order=df_launched['RAM'].value_counts().index)
    plt.title('Count of Launched Phones by RAM')
    plt.xlabel('RAM')
    plt.ylabel('Number of Phones Launched')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Internal Storage Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_launched, x='Internal Storage', order=df_launched['Internal Storage'].value_counts().index)
    plt.title('Count of Launched Phones by Internal Storage')
    plt.xlabel('Internal Storage')
    plt.ylabel('Number of Phones Launched')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Battery Range Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_launched, x='Battery Capacity Range', order=df_launched['Battery Capacity Range'].value_counts().index)
    plt.title('Count of Launched Phones by Battery Capacity Range')
    plt.xlabel('Battery Capacity Range')
    plt.ylabel('Number of Phones Launched')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print("Visualizations for launched phones completed.")
    print('=' * 50)

def visualize_upcoming_phones(df_upcoming_rumored):
    print(df_upcoming_rumored.head())
    print('=' * 50)

    # Distribution of Spec Scores
    plt.figure(figsize=(12, 6))
    sns.histplot(df_upcoming_rumored['Spec Score'], bins=30, kde=True)
    plt.title('Distribution of Specification Scores in Upcoming and Rumored Phones')
    plt.xlabel('Specification Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Price Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df_upcoming_rumored['Price'], bins=30, kde=True)
    plt.title('Distribution of Prices in Upcoming and Rumored Phones')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Rating Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df_upcoming_rumored['Rating'], bins=30, kde=True)
    plt.title('Distribution of Ratings in Upcoming and Rumored Phones')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Brand Family Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_upcoming_rumored, x='Brand Family', order=df_upcoming_rumored['Brand Family'].value_counts().index)
    plt.title('Count of Upcoming and Rumored Phones by Brand Family')
    plt.xlabel('Brand Family')
    plt.ylabel('Number of Upcoming and Rumored Phones')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Processor Family Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_upcoming_rumored, x='Processor Family', order=df_upcoming_rumored['Processor Family'].value_counts().index)
    plt.title('Count of Upcoming and Rumored Phones by Processor Family')
    plt.xlabel('Processor Family')
    plt.ylabel('Number of Phones')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # RAM Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_upcoming_rumored, x='RAM', order=df_upcoming_rumored['RAM'].value_counts().index)
    plt.title('Count of Upcoming and Rumored Phones by RAM')
    plt.xlabel('RAM')
    plt.ylabel('Number of Phones')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Internal Storage Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_upcoming_rumored, x='Internal Storage', order=df_upcoming_rumored['Internal Storage'].value_counts().index)
    plt.title('Count of Upcoming and Rumored Phones by Internal Storage')
    plt.xlabel('Internal Storage')
    plt.ylabel('Number of Phones')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Battery Range Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_upcoming_rumored, x='Battery Capacity Range', order=df_upcoming_rumored['Battery Capacity Range'].value_counts().index)
    plt.title('Count of Upcoming and Rumored Phones by Battery Capacity Range')
    plt.xlabel('Battery Capacity Range')
    plt.ylabel('Number of Phones')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Display Size Range Distribution
    plt.figure(figsize=(14, 7))
    sns.countplot(data=df_upcoming_rumored, x='Display Size Range', order=df_upcoming_rumored['Display Size Range'].value_counts().index)
    plt.title('Count of Upcoming and Rumored Phones by Display Size Range')
    plt.xlabel('Display Size Range')
    plt.ylabel('Number of Phones')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("Visualizations for upcoming and rumored phones completed.")
    print('=' * 50)

def load_launched_data(path='data/preprocess/mobile_launched_cleaned.csv'):
    return pd.read_csv(path)

def load_upcoming_data(path='data/preprocess/mobile_upcoming_cleaned.csv'):
    return pd.read_csv(path)
