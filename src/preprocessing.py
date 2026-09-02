import pandas as pd
from datasets import load_dataset
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm')

def load_and_filter_tweeteval():
    # Load TweetEval sentiment dataset
    dataset = load_dataset("tweet_eval", "sentiment")
    tweets = dataset['train']['text']
    labels = dataset['train']['label']
    
    # Policy-related keywords
    policy_keywords = ['GST', 'Digital India', 'Make in India', 'Aadhaar', 'Swachh Bharat']
    
    # Filter tweets containing policy keywords
    filtered_data = []
    for tweet, label in zip(tweets, labels):
        if any(keyword.lower() in tweet.lower() for keyword in policy_keywords):
            policy = next((k for k in policy_keywords if k.lower() in tweet.lower()), "Unknown")
            filtered_data.append({"text": tweet, "label": label, "policy": policy})
    
    df = pd.DataFrame(filtered_data)
    df.to_csv("data/processed/filtered_tweeteval.csv", index=False)
    return df

def preprocess_text(text):
    # Remove URLs, mentions, hashtags, emojis
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize and remove stopwords
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stop_words]
    
    # Lemmatization
    doc = nlp(" ".join(tokens))
    tokens = [token.lemma_ for token in doc]
    
    return " ".join(tokens)

def preprocess_dataset():
    df = pd.read_csv("data/processed/filtered_tweeteval.csv")
    df['cleaned_text'] = df['text'].apply(preprocess_text)
    df.to_csv("data/processed/preprocessed_tweeteval.csv", index=False)
    return df

if __name__ == "__main__":
    # Load and filter TweetEval
    df = load_and_filter_tweeteval()
    print(f"Filtered {len(df)} policy-related tweets.")
    
    # Preprocess the dataset
    df_processed = preprocess_dataset()
    print("Preprocessing complete. Saved to data/processed/preprocessed_tweeteval.csv")