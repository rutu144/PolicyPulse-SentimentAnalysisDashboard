# import pandas as pd
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# import re
# import numpy as np

# # Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')

# # Preprocessing function
# def preprocess_text(text):
#     text = text.lower()
#     text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
#     text = re.sub(r'@\w+|\#', '', text)
#     text = re.sub(r'[^\w\s]', '', text)
#     tokens = word_tokenize(text)
#     stop_words = set(stopwords.words('english'))
#     tokens = [word for word in tokens if word not in stop_words]
#     stemmer = PorterStemmer()
#     tokens = [stemmer.stem(word) for word in tokens]
#     return ' '.join(tokens)

# # Load existing dummy dataset
# dummy_df = pd.read_csv('data/dummy/dummy_tweets.csv')

# # Preprocess existing dummy dataset
# dummy_df['cleaned_text'] = dummy_df['text'].apply(preprocess_text)
# dummy_df.to_csv('data/dummy/preprocessed_dummy_tweets.csv', index=False)

# # Load TweetEval datasets
# tweeteval_train = pd.read_csv('data/dummy/tweeteval_train.csv')
# tweeteval_val = pd.read_csv('data/dummy/tweeteval_val.csv')

# # Combine TweetEval train and validation sets
# tweeteval_df = pd.concat([tweeteval_train, tweeteval_val], ignore_index=True)

# # Preprocess TweetEval text
# tweeteval_df['cleaned_text'] = tweeteval_df['text'].apply(preprocess_text)

# # Assign policies randomly (50% GST, 50% Digital India)
# def assign_policy(text):
#     text = text.lower()
#     if any(keyword in text for keyword in ['gst', 'tax', 'filing', 'rates']):
#         return 'GST'
#     elif any(keyword in text for keyword in ['digital', 'internet', 'egovernance', 'rural']):
#         return 'Digital India'
#     else:
#         return np.random.choice(['GST', 'Digital India'])  # Fallback

# tweeteval_df['policy'] = tweeteval_df['text'].apply(assign_policy)

# # Ensure columns match: text, label, policy, cleaned_text
# tweeteval_df = tweeteval_df[['text', 'label', 'policy', 'cleaned_text']]

# # Sample 10,000 tweets to keep dataset manageable for hackathon
# tweeteval_sample = tweeteval_df.sample(n=5000, random_state=42)

# # Merge with existing dummy dataset
# combined_df = pd.concat([dummy_df, tweeteval_sample], ignore_index=True)

# # Save the upscaled dataset
# combined_df.to_csv('data/dummy/preprocessed_dummy_tweets.csv', index=False)

# print(f"Upscaled dataset saved with {len(combined_df)} rows.")
# print(combined_df.head())
# print("\nLabel distribution:")
# print(combined_df['label'].value_counts())
# print("\nPolicy distribution:")
# print(combined_df['policy'].value_counts())

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import numpy as np

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|\#', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

# Policy assignment function
def assign_policy(text):
    text = text.lower()
    gst_keywords = ['gst', 'tax', 'filing', 'rates', 'business', 'trader']
    digital_india_keywords = ['digital', 'internet', 'egovernance', 'rural', 'online']
    make_in_india_keywords = ['manufacturing', 'industry', 'makeinindia', 'production', 'factory']
    swachh_bharat_keywords = ['clean', 'sanitation', 'swachhbharat', 'hygiene', 'waste']
    if any(keyword in text for keyword in gst_keywords):
        return 'GST'
    elif any(keyword in text for keyword in digital_india_keywords):
        return 'Digital India'
    elif any(keyword in text for keyword in make_in_india_keywords):
        return 'Make in India'
    elif any(keyword in text for keyword in swachh_bharat_keywords):
        return 'Swachh Bharat'
    else:
        return np.random.choice(['GST', 'Digital India', 'Make in India', 'Swachh Bharat'], p=[0.25, 0.25, 0.25, 0.25])

# Load existing dummy dataset
dummy_df = pd.read_csv('data/dummy/dummy_tweets.csv')

# Preprocess existing dummy dataset
dummy_df['cleaned_text'] = dummy_df['text'].apply(preprocess_text)
dummy_df.to_csv('data/dummy/preprocessed_dummy_tweets.csv', index=False)

# Load TweetEval datasets
tweeteval_train = pd.read_csv('data/dummy/tweeteval_train.csv')
tweeteval_val = pd.read_csv('data/dummy/tweeteval_val.csv')

# Combine TweetEval train and validation sets
tweeteval_df = pd.concat([tweeteval_train, tweeteval_val], ignore_index=True)

# Preprocess TweetEval text
tweeteval_df['cleaned_text'] = tweeteval_df['text'].apply(preprocess_text)

# Assign policies
tweeteval_df['policy'] = tweeteval_df['text'].apply(assign_policy)

# Ensure columns match: text, label, policy, cleaned_text
tweeteval_df = tweeteval_df[['text', 'label', 'policy', 'cleaned_text']]

# Sample 10,000 tweets for hackathon
tweeteval_sample = tweeteval_df.sample(n=10000, random_state=42)

# Merge with existing dummy dataset
combined_df = pd.concat([dummy_df, tweeteval_sample], ignore_index=True)

# Save upscaled dataset
combined_df.to_csv('data/dummy/preprocessed_dummy_tweets.csv', index=False)

print(f"Upscaled dataset saved with {len(combined_df)} rows.")
print(combined_df.head())
print("\nLabel distribution:")
print(combined_df['label'].value_counts())
print("\nPolicy distribution:")
print(combined_df['policy'].value_counts())