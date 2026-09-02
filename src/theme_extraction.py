import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

nlp = spacy.load('en_core_web_sm')

def extract_keywords(texts, top_n=10):
    keywords = []
    for text in texts:
        doc = nlp(text)
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:
                keywords.append(chunk.text.lower())
    keyword_counts = Counter(keywords)
    return keyword_counts.most_common(top_n)

def extract_topics(texts, n_topics=3, n_words=5):
    if len(texts) < 2:  # Check for small dataset
        return ["Topic modeling skipped: dataset too small"]
    
    try:
        # Use more lenient min_df for small datasets
        vectorizer = CountVectorizer(max_df=0.95, min_df=1, stop_words='english')
        X = vectorizer.fit_transform(texts)
        
        # Check if any terms remain after vectorization
        if X.shape[1] == 0:
            return ["No valid terms found for topic modeling"]
        
        # Apply LDA
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(X)
        
        # Get top words per topic
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]]
            topics.append(f"Topic {topic_idx + 1}: {', '.join(top_words)}")
        return topics
    except Exception as e:
        return [f"Topic modeling failed: {str(e)}"]

def extract_themes(df, policy=None):
    if policy:
        texts = df[df['policy'] == policy]['cleaned_text'].tolist()
    else:
        texts = df['cleaned_text'].tolist()
    
    keywords = extract_keywords(texts)
    topics = extract_topics(texts)
    
    return {"keywords": keywords, "topics": topics}

if __name__ == "__main__":
    # Test with preprocessed dummy data
    df = pd.read_csv("data/dummy/preprocessed_dummy_tweets.csv")
    themes = extract_themes(df, policy="GST")
    print("GST Themes:")
    print("Keywords:", themes['keywords'])
    print("Topics:", themes['topics'])